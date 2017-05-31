# -*- coding: utf-8 -*-
"""PyCTD loads all CTD content in the database. Content is available via functions."""

import sys
if sys.version_info[0] == 3:
    from urllib.request import urlretrieve
    from requests.compat import urlparse
else:
    from urllib import urlretrieve
    from urlparse import urlparse

import logging
import pandas as pd
import io
import gzip
import configparser

from ..constants import PYCTD_DATA_DIR, PYCTD_DIR

import os
import re
from configparser import RawConfigParser
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine import reflection
from sqlalchemy.sql import sqltypes
import numpy as np

from . import defaults
from . import models
from . import table_conf
from .table import get_table_configurations
from ..constants import bcolors

log = logging.getLogger(__name__)

alchemy_pandas_dytpe_mapper = {
    sqltypes.Text: np.unicode,
    sqltypes.String: np.unicode,
    sqltypes.Integer: np.float,
    sqltypes.REAL: np.double
}


class BaseDbManager(object):
    """Creates a connection to database and a persistient session using SQLAlchemy"""

    def __init__(self, connection=None, echo=False):
        """
        :param str connection: SQLAlchemy 
        :param bool echo: True or False for SQL output of SQLAlchemy engine
        """
        log.setLevel(logging.INFO)
        
        handler = logging.FileHandler(os.path.join(PYCTD_DIR, defaults.TABLE_PREFIX + 'database.log'))
        handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        log.addHandler(handler)

        try:
            self.connection = self.get_connection_string(connection)
            self.engine = create_engine(self.connection, echo=echo)
            self.inspector = reflection.Inspector.from_engine(self.engine)
            self.sessionmaker = sessionmaker(bind=self.engine, autoflush=False, expire_on_commit=False)
            self.session = scoped_session(self.sessionmaker)()
        except:
            self.set_connection_string_by_user_input()
            self.__init__()

    def set_connection_string_by_user_input(self):
        user_connection = input(
            bcolors.WARNING + "\nFor any reason connection to " + bcolors.ENDC +
            bcolors.FAIL + "{}".format(self.connection) + bcolors.ENDC +
            bcolors.WARNING + " is not possible.\n\n" + bcolors.ENDC +
            "For more information about SQLAlchemy connection strings go to:\n" +
            "http://docs.sqlalchemy.org/en/latest/core/engines.html\n\n"
            "Please insert a valid connection string:\n" +
            bcolors.UNDERLINE + "Examples:\n\n" + bcolors.ENDC +
            "MySQL (recommended):\n" +
            bcolors.OKGREEN + "\tmysql+pymysql://user:passwd@localhost/database?charset=utf8\n" + bcolors.ENDC +
            "PostgreSQL:\n" +
            bcolors.OKGREEN + "\tpostgresql://scott:tiger@localhost/mydatabase\n" + bcolors.ENDC +
            "MsSQL (pyodbc have to be installed):\n" +
            bcolors.OKGREEN + "\tmssql+pyodbc://user:passwd@database\n" + bcolors.ENDC +
            "SQLite (always works):\n" +
            " - Linux:\n" +
            bcolors.OKGREEN + "\tsqlite:////absolute/path/to/database.db\n" + bcolors.ENDC +
            " - Windows:\n" +
            bcolors.OKGREEN + "\tsqlite:///C:\\path\\to\\database.db\n" + bcolors.ENDC +
            "Oracle:\n" +
            bcolors.OKGREEN + "\toracle://user:passwd@127.0.0.1:1521/database\n\n" + bcolors.ENDC +
            "[RETURN] for standard connection {}:\n".format(defaults.sqlalchemy_connection_string_default)
        )
        if not (user_connection or user_connection.strip()):
            user_connection = defaults.sqlalchemy_connection_string_default
        set_connection(user_connection.strip())

    @staticmethod
    def get_connection_string(connection=None):
        """return sqlalchemy connection string if it is set
        
        :param connection: get the SQLAlchemy connection string #TODO
        :return: 
        """
        if not connection:
            config = configparser.ConfigParser()
            cfp = defaults.config_file_path
            if os.path.exists(cfp):
                log.info('fetch database configuration from {}'.format(cfp))
                config.read(cfp)
                connection = config['database']['sqlalchemy_connection_string']
                log.info('load connection string from {}: {}'.format(cfp, connection))
            else:
                with open(cfp, 'w') as config_file:
                    connection = defaults.sqlalchemy_connection_string_default
                    config['database'] = {'sqlalchemy_connection_string': connection}
                    config.write(config_file)
                    log.info('create configuration file {}'.format(cfp))
        return connection

    def _create_tables(self, checkfirst=True):
        """creates all tables from models in your database
        
        :param checkfirst: True or False check if tables already exists
        :type checkfirst: bool
        :return: 
        """
        log.info('create tables in {}'.format(self.engine.url))
        models.Base.metadata.create_all(self.engine, checkfirst=checkfirst)

    def _drop_tables(self):
        """drops all tables in the database

        :return: 
        """
        log.info('drop tables in {}'.format(self.engine.url))
        self.session.commit()
        models.Base.metadata.drop_all(self.engine)
        self.session.commit()


class DbManager(BaseDbManager):
    __mapper = {}
    pyctd_data_dir = PYCTD_DATA_DIR

    def __init__(self, connection=None):
        """The DbManager implements all function to upload CTD files into the database. Prefered SQL Alchemy 
        database is MySQL with pymysql.
        
        :param connection: custom database connection SQL Alchemy string
        :type connection: str
        """

        super(DbManager, self).__init__(connection=connection)
        self.tables = get_table_configurations()

    def db_import(self, urls=None, force_download=False, add_inchis=True):
        """Updates the CTD database
        
        1. downloads all files from CTD
        2. drops all tables in database
        3. creates all tables in database
        4. import all data from CTD filess
        
        :param urls: iterable of URL strings
        :type urls: str
        :param force_download: force method to download
        :type: bool
        :return: SQL Alchemy model instance, populated with data from URL
        :rtype: :class:`models.Namespace`
        """
        if urls is None:
            urls = [defaults.url_base + table_conf.tables[model]['file_name'] for model in table_conf.tables]

        log.info('Update CTD database from {}'.format(urls))

        self._drop_tables()
        DbManager.download_urls(urls, force_download)
        self._create_tables()
        self.import_tables()
        self.session.close()

    @property
    def mapper(self):
        """returns a dictionary with keys of pyctd.manager.table_con.domains_to_map and pandas.DataFrame as values. 
        
        DataFrames column names:

        - domain_id (represents the domain identifier of e.g. chemical)
        - domain__id (represents the primary key in domain table)


        :return: dict of pandas DataFrames (keys:domain_name, values:DataFrame)
        :rtype: dict of pandas.DataFrame
        """
        if not self.__mapper:
            for model in table_conf.models_to_map:
                domain = model.table_suffix
                tab_conf = table_conf.tables[model]

                file_path = os.path.join(self.pyctd_data_dir, tab_conf['file_name'])

                col_name_in_file, col_name_in_db = tab_conf['domain_id_column']

                column_index = self.get_index_of_column(col_name_in_file, file_path)

                df = pd.read_table(
                    file_path,
                    names=[col_name_in_db],
                    header=None,
                    usecols=[column_index],
                    comment='#',
                    index_col=False,
                    dtype=self.get_dtypes(model)
                )

                if domain == 'chemical':
                    df[col_name_in_db] = df[col_name_in_db].str.replace('MESH:', '').str.strip()

                df[domain + '__id'] = df.index + 1
                self.__mapper[domain] = df
        return self.__mapper

    def import_tables(self, only_tables=(), exclude_tables=()):
        """Imports all data in database tables
        
        :param exclude_tables: iterable of tables to be excluded
        :param only_tables: iterable of tables to be imported
        :type only_tables: iterable of str
        :return: 
        """
        for table in self.tables:
            if (only_tables and table.name not in only_tables) or table.name in exclude_tables:
                continue
            self.import_table(table)

    def get_index_of_column(self, column, file_path):
        """Get index of a specific column name in a CTD file
        
        :param column: 
        :param file_path: 
        :return: int or None
        """
        columns = DbManager.get_column_names_from_file(file_path)
        if column in columns:
            return columns.index(column)

    def get_index_and_columns_order(self, columns_in_file_expected, columns_dict, file_path):
        """
        
        :param columns_in_file_expected: 
        :param columns_dict: 
        :param file_path: 
        :return: 
        """
        use_columns_with_index = []
        column_names_in_db = []

        column_names_from_file = DbManager.get_column_names_from_file(file_path)
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
        """import table by Table object
        
        :param `manager.table_conf.Table` table: Table object
        :return: 
        """
        file_path = os.path.join(self.pyctd_data_dir, table.file_name)
        log.info('import CTD from file path {} data into table {}'.format(file_path, table.name))

        r = self.get_index_and_columns_order(
            table.columns_in_file_expected,
            table.columns_dict,
            file_path
        )
        use_columns_with_index, column_names_in_db = r

        self.import_table_in_db(file_path, use_columns_with_index, column_names_in_db, table)

        for column_in_file, column_in_one2many_table in table.one_to_many:

            o2m_column_index = self.get_index_of_column(column_in_file, file_path)

            self.import_one_to_many(file_path, o2m_column_index, table, column_in_one2many_table)

    def import_one_to_many(self, file_path, column_index, parent_table, column_in_one2many_table):
        """
        
        :param file_path: 
        :param column_index: 
        :param parent_table_name: 
        :param column_in_one2many_table: 
        :return: 
        """
        chunks = pd.read_table(
            file_path,
            usecols=[column_index],
            header=None,
            comment='#',
            index_col=False,
            chunksize=1000000,
            dtype=self.get_dtypes(parent_table.model)
        )

        for chunk in chunks:
            child_values = []
            parent_id_values = []

            chunk.dropna(inplace=True)
            chunk.index += 1

            for parent_id, values in chunk.iterrows():
                entry = values[column_index]
                if not isinstance(entry, str):
                    entry = str(entry)
                for value in entry.split("|"):
                    parent_id_values.append(parent_id)
                    child_values.append(value.strip())

            parent_id_column_name = parent_table.name + '__id'
            o2m_table_name = defaults.TABLE_PREFIX + parent_table.name + '__' + column_in_one2many_table

            pd.DataFrame({
                parent_id_column_name: parent_id_values,
                column_in_one2many_table: child_values
            }).to_sql(name=o2m_table_name, if_exists='append', con=self.engine, index=False)


    def get_dtypes(self,sqlalchemy_model):
        mapper = inspect(sqlalchemy_model)
        dtypes = {x.key: alchemy_pandas_dytpe_mapper[type(x.type)] for x in mapper.columns if x.key != 'id'}
        return dtypes


    def import_table_in_db(self, file_path, use_columns_with_index, column_names_in_db, table):
        """Imports data from CTD file into database
        
        :param table: `manager.table.Table` object
        :param str file_path: path to file
        :param use_columns_with_index: list of column indices in file
        :type use_columns_with_index: list of int
        :param column_names_in_db: list of column names (have to fit to models except domain_id column name) 
        :type column_names_in_db: list of str
        :param dict pandas_dtypes: dictionary of pandas datatypse
        """
        chunks = pd.read_table(
            file_path,
            usecols=use_columns_with_index,
            names=column_names_in_db,
            header=None, comment='#',
            index_col=False,
            chunksize=1000000,
            dtype=self.get_dtypes(table.model)
        )

        for chunk in chunks:
            # this is an evil hack because CTD is not using the MESH prefix in this table
            if table.name == 'exposure_event':
                chunk.disease_id = 'MESH:' + chunk.disease_id

            chunk['id'] = chunk.index + 1

            if table.model not in table_conf.models_to_map:
                for model in table_conf.models_to_map:
                    domain = model.table_suffix
                    domain_id = domain + "_id"
                    if domain_id in column_names_in_db:
                        chunk = pd.merge(chunk, self.mapper[domain], on=domain_id, how='left')
                        del chunk[domain_id]

            chunk.set_index('id', inplace=True)

            table_with_prefix = defaults.TABLE_PREFIX + table.name
            chunk.to_sql(name=table_with_prefix, if_exists='append', con=self.engine)

        del chunks

    @staticmethod
    def get_column_names_from_file(file_path):
        """returns column names from CTD download file

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

    @staticmethod
    def download_urls(urls, force_download=False):
        """Downloads all CTD URLs if it not exists
    
        :param urls: iterable of URL of CTD
        :type urls: iterable
        :param force_download: force method to download
        :type force_download: bool
        """
        for url in urls:
            file_path = DbManager.get_path_to_file_from_url(url)
            if force_download or not os.path.exists(file_path):
                log.info('download {}'.format(file_path))
                urlretrieve(url, file_path)

    @staticmethod
    def get_path_to_file_from_url(url):
        """standard file path
        
        :param str url: CTD download URL 
        """
        file_name = urlparse(url).path.split('/')[-1]
        return os.path.join(DbManager.pyctd_data_dir, file_name)


def update(connection=None, urls=None, force_download=False):
    """Updates CTD database

    :param urls: list of urls to download
    :type urls: iterable
    :param connection: custom database connection string
    :type connection: str
    :param force_download: force method to download
    :type force_download: bool
    """

    db = DbManager(connection)
    db.db_import(urls, force_download)
    db.session.close()


def set_mysql_connection(host='localhost', user='pyctd_user', passwd='pyctd_passwd', db='pyctd', charset='utf8'):
    set_connection('mysql+pymysql://{user}:{passwd}@{host}/{db}?charset={charset}'
                   .format(host=host, user=user, passwd=passwd, db=db, charset=charset))


def set_test_connection():
    set_connection(defaults.DEFAULT_SQLITE_TEST_DATABASE_NAME)


def set_connection(connection=defaults.sqlalchemy_connection_string_default):
    """
    Set the connection string for sqlalchemy
    :param str connection: sqlalchemy connection string
    """
    cfp = defaults.config_file_path
    config = RawConfigParser()

    if not os.path.exists(cfp):
        with open(cfp, 'w') as config_file:
            config['database'] = {'sqlalchemy_connection_string': connection}
            config.write(config_file)
            log.info('create configuration file {}'.format(cfp))
    else:
        config.read(cfp)
        config.set('database', 'sqlalchemy_connection_string', connection)
        with open(cfp, 'w') as configfile:
            config.write(configfile)


