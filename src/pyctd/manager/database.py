# -*- coding: utf-8 -*-
"""
Under the hood, PyBEL caches namespace and annotation files for quick recall on later use. The user doesn't need to
enable this option, but can specifiy a specific database location if they choose.
"""

import logging
import pandas as pd
import io
import gzip
import configparser
import numpy as np

import requests
from ..constants import PYCTD_DATA_DIR, PYCTD_DIR

import os
import re
import urllib.parse

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine import reflection

from . import defaults
from . import models
from . import table_conf

log = logging.getLogger(__name__)


class Table:

    def __init__(self, name, conf):
        self.name = name
        self.columns_in_file_expected = [x[0] for x in conf['columns']]
        self.columns_in_db = [x[1] for x in conf['columns']]
        self.columns_dict = dict(conf['columns'])
        self.file_name = conf['file_name']
        self.one_to_many = ()
        if 'one_to_many' in conf:
            self.one_to_many = conf['one_to_many']


class BaseDbManager:

    """Creates a connection to database and a persistient session using SQLAlchemy"""

    def __init__(self, connection=None, echo=False):
        log = logging.getLogger(__name__)
        log.setLevel(logging.INFO)
        
        handler = logging.FileHandler(os.path.join(PYCTD_DIR, models.TABLE_PREFIX + 'database.log'))
        handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        log.addHandler(handler)
                
        self.connection = self.get_connection_string(connection)
        self.engine = create_engine(self.connection, echo=echo)
        self.database = self.engine.dialect._get_default_schema_name(self.engine)
        
        self.inspector = reflection.Inspector.from_engine(self.engine)
        
        self.sessionmaker = sessionmaker(bind=self.engine, autoflush=False, expire_on_commit=False)
        self.session = scoped_session(self.sessionmaker)()
        self.drop_database()
        self.create_database()

    @staticmethod
    def get_connection_string(connection=None):
        if not connection:
            config_file_path = os.path.join(PYCTD_DIR,'config.ini')
            config = configparser.ConfigParser()
            
            if os.path.exists(config_file_path):
                log.info('fetch database configuration from {}'.format(config_file_path))
                config.read(config_file_path)
                connection = config['database']['sqlalchemy_connection_string']
                log.info('load connection string from {}: {}'.format(config_file_path,connection))
            else:
                with open(config_file_path, 'w') as config_file:
                    connection = defaults.sqlalchemy_connection_string
                    config['database'] = {'sqlalchemy_connection_string':connection}
                    config.write(config_file)
                    log.info('create configuration file {}'.format(config_file_path))
        return connection

    def create_database(self, checkfirst=True):
        log.info('create tables in {}'.format(self.database))
        models.Base.metadata.create_all(self.engine, checkfirst=checkfirst)

    def drop_database(self):
        models.Base.metadata.drop_all(self.engine)


class DbManager(BaseDbManager):
    mapper = {}

    def __init__(self, connection=None):
        """The definition cache manager takes care of storing BEL namespace and annotation files for later use.
        It uses SQLite by default for speed and lightness, but any database can be used wiht its SQLAlchemy interface.

        :param connection: custom database connection string
        :type connection: str
        :param echo: Whether or not echo the running sql code.
        :type echo: bool
        """

        BaseDbManager.__init__(self, connection=connection)
        self.tables = []
        for table_name, conf in table_conf.tables.items():
            table = Table(table_name, conf)
            self.tables.append(table)

    def db_import(self, urls=None):
        """Updates the CTD database
        
        :param urls: iterable of URL strings
        :type url: str
        :return: SQL Alchemy model instance, populated with data from URL
        :rtype: :class:`models.Namespace`
        """
        if urls is None:
            urls = defaults.urls

        log.info('Update CTD database from {}'.format(urls))

        self.download_urls(urls)

        self.import_data('chemical')

        # self.import_data()
        # self.optimize_data_types(exclude_columns=['gene_id', 'chemical_id'])
        # self.normalize_domain_info('gene', ['geneID'],['geneSymbol'])
        # self.normalize_domain_info('disease', ['diseaseID'],['diseaseName'])
        # self.normalize_domain_info('chemical', ['chemicalID'],['chemicalName', 'casRN'])
        # self.create_pubmedid_links()
        # self.create_interaction_links()
        # self.create_drugbank_links()
        # self.cast_gotermid_2_int()
        # self.set_indices()

    def get_mapper(self):
        if not self.mapper:
            for domain in table_conf.domains_to_map:
                tab_conf = table_conf.tables[domain]
                file_path = os.path.join(PYCTD_DATA_DIR, tab_conf['file_name'])
                column_index, column_name = self.get_index_of_column(tab_conf['domain_id_column'])

                self.mapper[domain] = pd.read_table(
                    file_path,
                    names=[column_name],
                    header=None,
                    usecols=[column_index],
                    comment='#',
                    index_col=False
                )
        return self.mapper

    def import_tables(self):
        # for table in self.tables:
        #     self.import_table(table)
        for i in [0, 2]:
            self.import_table(self.tables[i])

    def get_index_of_column(self, column, file_path):
        columns = self.get_column_names_from_file(file_path)
        if column in columns:
            return columns.index(column)

    def get_index_and_columns_order(self, columns_in_file_expected, columns_dict, file_path):
        use_columns_with_index = []
        column_names_in_db = []

        column_names_from_file = self.get_column_names_from_file(file_path)
        if not set(columns_in_file_expected).issubset(column_names_from_file):
            log.exception('{} columns are not a subset of columns {} in file {}'.format(
                columns_in_file_expected,
                column_names_from_file,
                file_path
                )
            )
        else:
            for index, column in enumerate(column_names_from_file):
                if column in columns_dict:
                    use_columns_with_index.append(index)
                    column_names_in_db.append(columns_dict[column])
        return use_columns_with_index, column_names_in_db

    def import_table(self, table):
        """
        Import tables
        """
        file_path = os.path.join(PYCTD_DATA_DIR, table.file_name)
        log.info('import CTD from file path {} data into table {}'.format(file_path, table.name))

        r = self.get_index_and_columns_order(
            table.columns_in_file_expected,
            table.columns_dict,
            file_path
        )
        use_columns_with_index, column_names_in_db = r

        table_name = models.TABLE_PREFIX + table.name

        self.import_table_in_db(file_path, use_columns_with_index, column_names_in_db, table_name)

        for column_in_file, column_in_one2many_table in table.one_to_many:

            o2m_column_index = self.get_index_of_column(column_in_file, file_path)

            self.import_one_to_many(file_path, [o2m_column_index], table.name, column_in_one2many_table)

    def import_one_to_many(self, file_path, use_columns_o2m_with_index, parent_table_name, column_in_one2many_table):

        chunks = pd.read_table(
            file_path,
            usecols=use_columns_o2m_with_index,
            header=None,
            comment='#',
            index_col=False,
            chunksize=100000)

        parent_id_column_name = parent_table_name + '__id'
        o2m_table_name = models.TABLE_PREFIX + parent_table_name + '__' + column_in_one2many_table
        column_index = use_columns_o2m_with_index[0]

        for chunk in chunks:
            child_values = []
            parent_id_values = []

            chunk.index += 1

            for parent_id, values in chunk.iterrows():
                if isinstance(values[column_index], str):
                    for value in values[column_index].split(defaults.value_delimiter):
                        parent_id_values.append(parent_id)
                        child_values.append(value.strip())

            df = pd.DataFrame({
                parent_id_column_name: parent_id_values,
                column_in_one2many_table: child_values
            })
            df.to_sql(name=o2m_table_name, if_exists='append', con=self.engine, index=False)

    def import_table_in_db(self, file_path, use_columns_with_index, column_names_in_db, table_name):
        chunks = pd.read_table(
            file_path,
            usecols=use_columns_with_index,
            names=column_names_in_db,
            header=None, comment='#',
            index_col=False,
            chunksize=1000000)

        for chunk in chunks:
            for domain in table_conf.domains_to_map:
                if domain + "_id" in column_names_in_db:
                    domain_dataframe = self.get_mapper()[domain]
                    domain_dataframe.join(chunk.set_index(domain + '_id'), on=domain + '_id', how='inner')
                    # join here now self.mapper[domain] with dataframe and delete domain_id column
                    pass

            chunk.index += 1
            chunk.to_sql(name=table_name, if_exists='append', con=self.engine, index_label='id')

    def get_column_names_from_file(self, file_path):
        """
        returns column names from CTD download file

        :param file_path: path to CTD download file
        :type: file_path: str
        """
        if file_path.endswith('.gz'):
            file_handler = io.TextIOWrapper(io.BufferedReader(gzip.open(file_path)))
        else:
            file_handler = open(file_path, 'r')

        fields_line = False
        with file_handler as file:
            for line in file:
                line = line.strip()
                if not fields_line and re.search('#\s*Fields\s*:$', line):
                    fields_line = True
                elif fields_line and not (line == '' or line == '#'):
                    return [column.strip() for column in line[1:].split("\t")]

    def download_urls(self, urls):
        """Downloads all CTD URLs if it not exists
    
        :param urls: iterable of URL of CTD
        """
        for url in urls:
            file_path = self.get_path_to_file_from_url(url)
            if not os.path.exists(file_path):
                log.info(('download {}').format(file_path))
                with open(file_path, "wb") as data_file:
                    response = requests.get(url)
                    logging.info("download {}".format(url))
                    data_file.write(response.content)

    def get_path_to_file_from_url(self, url):
        """standatd file p
        
        :param url: CTD download URL 
        :type url: str
        """
        file_name = urllib.parse.urlsplit(url).path.split('/')[-1]
        return os.path.join(PYCTD_DATA_DIR, file_name)

    def get_table_name(self, url_or_fileName):
        """return a standard table name from URL
        
        :param url_or_fileName: CTD file name or URL 
        :type url_or_fileName: str
        """
        file_name_prefix = url_or_fileName.split('/')[-1].split('.')[0].lower()
        table_name = '_'.join([(x[:-1] if x.endswith('s') else x) for x in [y for y in file_name_prefix.split('_')[1:]]])

        if table_name == "chem_gene_ixn_type":
            table_name = "action"

        table_name = models.TABLE_PREFIX + table_name

        return table_name

    def import_data(self, if_table_exists=False):
        """
        Import data from urls
        :param urls: iterable of urls strings
        :type urls: iterable of str
        """
        addtional_foreign_key_columns = {
            'gene': ['geneSymbol', 'geneID'],
            'disease': ['diseaseName', 'diseaseID'],
            'chemical': ['chemicalName', 'chemicalID', 'casRN']
            }

        existing_tables = self.inspector.get_table_names()
        imported_tables = []

        for file_name in defaults.file_names:
            file_path = os.path.join(PYCTD_DATA_DIR, file_name)
            table = self.get_table_name_from_url(file_name)
            log.info('import CTD from file path {} data into table {}'.format(file_path, table))

            if os.path.exists(file_path) and (table not in existing_tables or if_table_exists):
                columns = self.get_column_names_from_file(file_path)

                if table in existing_tables:
                    self.drop_table(table)
                chunks = pd.read_table(file_path, names=columns, comment='#', index_col=False, chunksize=1000000)

                for chunk in chunks:

                    # the addtional column is used later in normalize_domain_info method
                    for tab_afkc, cols_afkc in addtional_foreign_key_columns.items():
                        if not table == models.TABLE_PREFIX + tab_afkc:
                            if set(cols_afkc).issubset(set(columns)):
                                chunk[tab_afkc + "_id"] = 0

                    chunk.index += 1
                    chunk.to_sql(name=table, if_exists='append', con=self.engine, index_label='id')

                imported_tables.append(table)

        return imported_tables


    def drop_column(self, table, column):
        """drop table from database
        :param table: table name
        :type table: str
        :param column: column name
        :type column: str
        """
        self.drop_columns(table, (column,))

    def drop_columns(self, table, columns):
        """drop columns in table
        :param table: table name
        :type table: str
        :param columns: column names
        :type column: iterable of str
        """
        cols = ', '.join(["DROP `{}`".format(c) for c in columns])
        self.engine.execute("ALTER TABLE `%s` %s" % (table,cols))


    def get_column_names(self, table):
        return [col['name'] for col in self.inspector.get_columns(table)]

    def optimize_data_types(self, urls=None, tables=None, exclude_columns=None):
        """
        optimize the data type and size of all columns in all given tables
        optimize if table is not null
        NOT optimize: column is auto incremental
        Keep NULL attribute: column is designed to be NULL, not optimize to NOT NULL
        :param urls: list of URLs of data files
        :type urls: list
        """
        optimizedColumnTypes=[]

        if urls is None and tables is None:
            urls = defaults.urls

        if tables==None:
            tables = [self.get_table_name_from_url(x) for x in urls]

        for table in tables:
            if not self.engine.execute("SELECT * FROM `{}` LIMIT 1".format(table)): # if no entries available continue
                continue
            original_columns_dict = {}


            desc_columns = self.engine.execute("DESCRIBE {}".format(table)).fetchall()
            for column in desc_columns and column not in exclude_columns:
                columnName = column[0]
                columnType = column[1]
                original_columns_dict[columnName] = columnType
            analysis = self.analyse_table(table)

            changes = []
            for column in analysis.keys():
                if  self.get_column_information_schema(table, column)['EXTRA'] == '':
                    optimized_type = analysis[column]['Optimal_fieldtype']
                    changes.append("CHANGE `{}` `{}` {}".format(column, column, optimized_type))
                    optimizedColumnTypes +=[(table, column, optimized_type)]

            if changes:
                sql = "ALTER TABLE `{}` {} ".format(table, ','.join(changes))
                log.info('optimize table {} with SQL: {}'.format(table, sql))
                self.engine.execute(sql)

        return optimizedColumnTypes

    def get_column_information_schema(self,table, column):
        """
        :summary function which returns information_schema.COLUMNS as dictionary for one column
        :param table: table name
        :type table: str
        :param column: column name
        :type colum: str
        """
        sql = """SELECT * 
            FROM 
                information_schema.COLUMNS 
            WHERE 
                TABLE_SCHEMA ='{}' AND 
                TABLE_NAME = '{}' AND 
                COLUMN_NAME='{}'""".format(self.database, table, column)
        r = self.engine.execute(sql).fetchone()
        return dict(r.items())

    def analyse_table(self, table, max_number_enums=1000, maximal_length_of_one_enum=255):
        """analyse table and returns dict with columns names as keys and values is dictionary with following keys Field_name,Min_value,Max_value,Min_length,Max_length,Empties_or_zeros,Nulls,Avg_value_or_avg_length,Std,Optimal_fieldtype
        :param table: table name
        :type table: str
        """
        analyse_dict = {}

        sql = "SELECT * FROM `%s` PROCEDURE ANALYSE ()" % table
        result = self.engine.execute(sql)

        for row in result.fetchall():

            row_dict = dict(row.items())
            column = row_dict['Field_name'].decode('utf-8').split('.')[-1]

            add_to_analyse_dict = True
            row_dict['Optimal_fieldtype'] = row_dict['Optimal_fieldtype'].decode('utf-8')

            if row_dict['Optimal_fieldtype'].startswith('ENUM'):

                number_enums = len(row_dict['Optimal_fieldtype'].split("','"))
                max_length_of_one_enum = max([len(x) for x in row_dict['Optimal_fieldtype'][5:-2].split("','")])

                if number_enums < max_number_enums and max_length_of_one_enum < maximal_length_of_one_enum:
                    # Optimal_fieldtype could be a long list of integers stored before as string
                    # the general suggestion from MySQL is an ENUM, more sense makes INT
                    row_dict['Optimal_fieldtype'] = row_dict['Optimal_fieldtype']
                    onlyIntergers = re.search("^(ENUM\(('-?\d+(e\+\d{2})?'(,'-?\d+(e\+\d{2})?')+)\))", row_dict['Optimal_fieldtype'])
                    if onlyIntergers:
                        row_dict['Optimal_fieldtype'] = 'INT ' + row_dict['Optimal_fieldtype'][len(onlyIntergers.groups()[0]):]

                    # Optimal_fieldtype could be a long list of floats stored before as string
                    # the general suggestion from MySQL is an ENUM, more sense makes FLOAT
                    onlyFloats = re.search("^(ENUM\('-?\d+(\.\d+)?'(,'-?\d+(\.\d+)?')+\))", row_dict['Optimal_fieldtype'])
                    if onlyFloats and re.search("^ENUM\([^)]*'-?\d+\.\d+'[^)]*\)", row_dict['Optimal_fieldtype']):
                        row_dict['Optimal_fieldtype'] = 'FLOAT '+ row_dict['Optimal_fieldtype'][len(onlyFloats.groups()[0]):]

                    # Optimal_fieldtype could be a long list of 'date time' stored before as string
                    # the general suggestion from MySQL is an ENUM, more sense makes DATETIME
                    onlyDatetimes = re.search("^(ENUM\('[12]\d{3}-[01]\d-[0-3]\d +[012]\d:[0-5]\d:[0-5]\d.\d+'( *, *'[12]\d{3}-[01]\d-[0-3]\d +[012]\d:[0-5]\d:[0-5]\d.\d+')+\))", row_dict['Optimal_fieldtype'])
                    if onlyDatetimes:
                        row_dict['Optimal_fieldtype'] = 'DATETIME ' + row_dict['Optimal_fieldtype'][len(onlyDatetimes.groups()[0]):]
                else:
                    add_to_analyse_dict = False

            # Optimal_fieldtype could be a long list of date stored before as string
            # the general suggestion from MySQL is an ENUM, more sense makes DATE
            # TODO: check next 3 lines makes sense because it slows down the execution
            #foundSomethingElseThanDate = self.engine.execute("Select * from %s where %s not regexp '^[12][0-9]{3}-[01][0-9]-[0-3][0-9]$'" % (table,column))
            #if not foundSomethingElseThanDate:
            #    adict['Optimal_fieldtype'] = 'DATE'

            # Because of Float problems restrictions of digits before and after dot are deleted
            if row_dict['Optimal_fieldtype'].startswith('FLOAT'):
                row_dict['Optimal_fieldtype'] = re.sub("\(\d+,\d+\)","",row_dict['Optimal_fieldtype'])

            if add_to_analyse_dict:
                analyse_dict[column] = row_dict

        return analyse_dict

    def delete_meshPrefix_from_chemicalId(self):
        table = models.TABLE_PREFIX + "chemical"
        sql = "UPDATE `{}` SET chemicalID = trim(replace(chemicalID,'MESH:',''))".format(table)
        self.engine.execute(sql)

    def normalize_domain_info(self,domain,domain_columns, cols2delete = []):
        """normalize tables, find redundancies in other table and creates a foreign key to domain table
        :param domain_table: table name where should be linked to
        :type domain_table: str
        :param domain_columns: columns, requested to be in the table to create foreign key to domain_table
        :type domain_columns: list of column names
        :param cols2delete: delete this columns in table with foreign key
        :type cols2delete: list of str
        """
        domain_table = models.TABLE_PREFIX + domain
        domain_columnId_name = domain + "_id"
        columns_string = ",".join(domain_columns)

        sql_check4Zeros = "Select id from {} where {}=0 group by {}"
        sql_updateForeignTable = "UPDATE {} a INNER JOIN {} b USING ({}) SET a.{} = b.id"

        self.create_index(domain_table, domain_columns, unique=True)

        tables = []
        for t in self.engine.table_names():
            if t.startswith(models.TABLE_PREFIX) and t!=domain_table:
                tables.append(t)

        for table in tables:

            columns = self.get_column_names(table)
            domain_columns_in_table = True if set(domain_columns)-set(columns)==set() else False

            if domain_columns_in_table:
                log.info("normalize in {} columns {}".format(table,domain_columns))

                self.create_index(table, domain_columns)

                sql = sql_updateForeignTable.format(table, domain_table, columns_string, domain_columnId_name)
                self.engine.execute(sql)

                #TODO: NDRG3.L is not imported in gene tables

                self.create_index(table, domain_columnId_name)

                sql = sql_check4Zeros.format(table,domain_columnId_name,domain_columnId_name)
                missing_foreign_keys = self.engine.execute(sql)

                if missing_foreign_keys.rowcount < 2: #TODO: '== 0' is here needed instead '< 2'
                    self.drop_columns(table, domain_columns + cols2delete)

    def create_index(self, table, columns, unique=False, index_name=''):
        """create an index/unique on a table (with optional a specific name)
        :param table: table name
        :param columns: iterable of columns
        :param unique: TRUE if index should be unique
        :param index_name: optional index name 
        """
        if type(columns)==str:
            columns = [columns]

        columns_string = ",".join(columns)

        index_type = "INDEX"
        if unique==True:
            index_type = "UNIQUE"

        if not self.table_has_index(table, columns, unique):
            sql = "ALTER TABLE `{}` ADD {} {} ({})".format(table, index_type, index_name, columns_string)
            self.engine.execute(sql)
            return True
        return False


    def get_index_columns(self, table, unique=False):
        """returns a list of sets with used unique keys, schema {constraint_name:{set_of_column_names}}
        :param table: table name
        :type table: str
        :param unique: True or False for all unique/non-unique indexes
        :type unique: bool
        """
        indexes = dict()

        sql = "SHOW INDEXES FROM {}""".format(table)
        if unique:
            sql += ' WHERE Non_unique=0'

        r = self.engine.execute(sql)

        for row in r.fetchall():

            rowDict = dict(row.items())
            index_name = rowDict['Key_name']
            column = rowDict['Column_name']

            if index_name in indexes:
                indexes[index_name].update((column,))
            else:
                indexes[index_name] = set([column,])
        return indexes

    def table_has_index(self, table, columns, unique=False):
        """checks if a table has an index on columns
        :param table: table name
        :type table: str
        :param columns: iterable of column names
        :type columns: iterable of str
        """
        have_index = False

        indexes = self.get_index_columns(table, unique)

        if set(columns) in indexes.values():
            have_index = True

        return have_index

    def create_pubmedid_links(self):

        for table in self.engine.table_names():
            if 'pubMedIDs' in self.get_column_names(table):
                log.info("create PubMed Id links for table {}".format(table))

                pubmed_table = table + "_pubmed"
                table_id_name =  table[len(models.TABLE_PREFIX):] + "_id"

                chunk_size = 10**6
                number_of_rows = self.engine.execute('SELECT COUNT(*) FROM `{}`'.format(table)).fetchone()[0]
                number_of_chunks =  int(number_of_rows / chunk_size)

                self.drop_table(pubmed_table)

                for start in range(number_of_chunks+1):
                    r = self.engine.execute("""SELECT 
                        id, pubMedIDs from `{}`  
                        limit {},{}""".format(table, (start * chunk_size), chunk_size))

                    rows = []
                    for table_id, pubmed_ids in r.fetchall():
                        if pubmed_ids:
                            for pubmed_id in pubmed_ids.split("|"):
                                rows.append((table_id, int(pubmed_id.strip())))

                    data_frame = pd.DataFrame(rows, columns=(table_id_name, 'pubMedID'))
                    data_frame.to_sql(name=pubmed_table, con=self.engine, if_exists='append', index=False)
                self.drop_column(table, 'pubMedIDs')

    def drop_table(self, table):
        if self.engine.has_table(table):
            self.engine.execute("Drop table {}".format(table))

    def create_interaction_links(self):
        log.info("create interaction links")
        table = models.TABLE_PREFIX + "chem_gene_ixn"
        table_id_name = table+"_id"
        table_ia = table + '_interaction_action'

        sql = "SELECT id, interactionActions FROM {}".format(table)
        r = self.engine.execute(sql)

        id_interaction_action = []
        for table_id, interactionsactions in r.fetchall():
            for interaction, action in [x.split("^") for x in interactionsactions.split("|")]:
                id_interaction_action.append((table_id, interaction, action))

        columns = (table_id_name, 'interaction', 'action')
        data_frame = pd.DataFrame(id_interaction_action, columns=columns)
        data_frame.to_sql(name=table_ia, con=self.engine, if_exists='replace', index=False)

        self.optimize_data_types(tables=[table_ia,])
        self.drop_column(table, "interactionActions")

    def create_drugbank_links(self):
        log.info("create drugbank links")
        table_chem = models.TABLE_PREFIX + "chemical"
        table_id_name = "chemical_id"
        table_chem_db = table_chem + '_drugbank'

        sql = "SELECT id, drugBankIDs FROM {}".format(table_chem)
        r = self.engine.execute(sql)

        chemicalId_drugbank = []
        for chemical_id, drugbankids in r.fetchall():
            if drugbankids:
                for drugbankId in drugbankids.split("|"):
                    db_id = int(re.search("^DB0*(\d+)", drugbankId).group(1))
                    chemicalId_drugbank.append((chemical_id, db_id))

        columns = (table_id_name, 'drugBankID')
        data_frame = pd.DataFrame(chemicalId_drugbank, columns=columns, dtype=(np.int, np.int))
        data_frame.to_sql(name=table_chem_db, con=self.engine, if_exists='replace', index=False)

        self.optimize_data_types(tables=[table_chem_db,])
        self.drop_column(table_chem, "drugBankIDs")

    def cast_gotermid_2_int(self):
        table = models.TABLE_PREFIX + 'chem_go_enriched'
        sql_checkAllGo = "Select * from {} where NOT goTermID rlike '^GO:'".format(table)
        checkAllGo = self.engine.execute(sql_checkAllGo)
        if checkAllGo.rowcount == 0:
            self.engine.execute("UPDATE `{}` SET goTermID=substring(goTermID,4)".format(table))
            self.engine.execute("ALTER TABLE `{}` CHANGE `goTermID` `goTermID` INT UNSIGNED NOT NULL".format(table))

    def set_indices(self):
        idx_cols = ['pubMedID']
        idx_tab_cols = {
            'chemical':('chemicalID','chemicalName'),
            'chem_go_enriched':('goTermID')
            }

        tables = self.inspector.get_table_names()

        for table in tables:
            norm_table = table[len(models.TABLE_PREFIX):]
            columns = self.get_column_names(table)
            for column in columns:
                if column.endswith('_id') or column in idx_cols:
                    self.create_index(table, column)
                elif norm_table in idx_tab_cols:
                    for idx_col in idx_tab_cols[norm_table]:
                        self.create_index(table, idx_col)

        
                        
def update(connection=None, urls=None):
    """
    Updates CTD database if it's outdated
    :ToDo Not implemented until now: Because CTD database is updated monthly 
    whole database will be updated if files in data folder are older then 1 month

    :param connection: custom database connection string
    :type connection: str
    """

    DbManager(connection).db_import(urls)
