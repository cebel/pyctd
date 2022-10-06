# -*- coding: utf-8 -*-

"""PyCTD loads all CTD content in the database. Content is available via functions."""

from codecs import ignore_errors
import configparser
import gzip
import io
import logging
import os
import re
import sys
import time
from configparser import RawConfigParser
from .table import Table
from typing import List, Dict
from .table_conf import OneToManyConfig

import numpy as np
import pandas as pd
from requests.compat import urlparse
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import reflection
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import sqltypes

from . import defaults
from . import models
from . import table_conf
from .table import get_table_configurations
from .table import Table
from ..constants import PYCTD_DATA_DIR, PYCTD_DIR, bcolors

if sys.version_info[0] == 3:
    from urllib.request import urlretrieve
else:
    from urllib import urlretrieve

log = logging.getLogger(__name__)

alchemy_pandas_dytpe_mapper = {
    sqltypes.Text: np.unicode_,
    sqltypes.String: np.unicode_,
    sqltypes.Integer: np.float64,
    sqltypes.REAL: np.double,
    sqltypes.BigInteger: 'Int64',
}


def get_connection_string(connection=None):
    """return SQLAlchemy connection string if it is set

    :param connection: get the SQLAlchemy connection string #TODO
    :rtype: str
    """
    if not connection:
        config = configparser.ConfigParser()
        cfp = defaults.config_file_path
        if os.path.exists(cfp):
            log.info('fetch database configuration from %s', cfp)
            config.read(cfp)
            connection = config['database']['sqlalchemy_connection_string']
            log.info('load connection string from %s: %s', cfp, connection)
        else:
            with open(cfp, 'w') as config_file:
                connection = defaults.sqlalchemy_connection_string_default
                config['database'] = {
                    'sqlalchemy_connection_string': connection}
                config.write(config_file)
                log.info('create configuration file %s', cfp)

    return connection


class BaseDbManager(object):
    """Creates a connection to database and a persistient session using SQLAlchemy"""

    def __init__(self, connection=None, echo=False):
        """
        :param str connection: SQLAlchemy 
        :param bool echo: True or False for SQL output of SQLAlchemy engine
        """
        log.setLevel(logging.INFO)
        handler = logging.FileHandler(os.path.join(
            PYCTD_DIR, defaults.TABLE_PREFIX + 'database.log'))
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        log.addHandler(handler)

        try:
            self.connection = get_connection_string(connection)
            self.engine = create_engine(self.connection, echo=echo)
            self.inspector = reflection.Inspector.from_engine(self.engine)
            self.sessionmaker = sessionmaker(
                bind=self.engine, autoflush=False, expire_on_commit=False)
            self.session = scoped_session(self.sessionmaker)()
        except Exception as e:
            print(e)
            self.set_connection_string_by_user_input()
            self.__init__()

    def set_connection_string_by_user_input(self):
        """Prompts the user to input a connection string"""
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
            "[RETURN] for standard connection {}:\n".format(
                defaults.sqlalchemy_connection_string_default)
        )
        if not (user_connection or user_connection.strip()):
            user_connection = defaults.sqlalchemy_connection_string_default
        set_connection(user_connection.strip())

    def create_all(self, checkfirst=True):
        """Creates all tables from models in the database

        :param bool checkfirst: Check if tables already exists
        """
        log.info('creating tables in %s', self.engine.url)
        models.Base.metadata.create_all(self.engine, checkfirst=checkfirst)

    def drop_all(self):
        """Drops all tables in the database"""
        log.info('dropping tables in %s', self.engine.url)
        self.session.commit()
        models.Base.metadata.drop_all(self.engine)
        self.session.commit()


class DbManager(BaseDbManager):
    """Implements functions to upload CTD files into a database. Preferred SQL Alchemy database is MySQL with
    :mod:`pymysql`.
    """

    __mapper = {}

    pyctd_data_dir = PYCTD_DATA_DIR

    def __init__(self, connection=None):
        """
        :param str connection: custom database connection SQL Alchemy string
        """
        super(DbManager, self).__init__(connection=connection)
        self.tables: List[Table] = get_table_configurations()

    def db_import(self, urls=None, force_download=False):
        """Updates the CTD database

        1. downloads all files from CTD
        2. drops all tables in database
        3. creates all tables in database
        4. import all data from CTD files

        :param iter[str] urls: An iterable of URL strings
        :param bool force_download: force method to download
        """
        if not urls:
            urls = [
                defaults.url_base + table_conf.tables[model].file_name
                for model in table_conf.tables
            ]

        log.info('Update CTD database from %s', urls)

        self.drop_all()
        self.download_urls(urls=urls, force_download=force_download)
        self.create_all()
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

                file_path = os.path.join(
                    self.pyctd_data_dir, tab_conf.file_name)

                col_name_in_file, col_name_in_db = tab_conf.domain_id_column if isinstance(
                    tab_conf.domain_id_column, tuple) else ('', '')

                column_index = self.get_index_of_column(
                    col_name_in_file, file_path)

                df = pd.read_csv(
                    file_path,
                    names=[col_name_in_db],
                    header=None,
                    usecols=[column_index],
                    comment='#',
                    index_col=False,
                    dtype=self.get_dtypes(model),
                    sep="\t"
                )

                if domain == 'chemical':
                    df[col_name_in_db] = df[col_name_in_db].str.replace(
                        'MESH:', '').str.strip()

                df[domain + '__id'] = df.index + 1
                self.__mapper[domain] = df
        return self.__mapper

    def import_tables(self, only_tables=None, exclude_tables=None):
        """Imports all data in database tables

        :param set[str] only_tables: names of tables to be imported
        :param set[str] exclude_tables: names of tables to be excluded
        """
        for table in self.tables:
            if only_tables is not None and table.name not in only_tables:
                continue

            if exclude_tables is not None and table.name in exclude_tables:
                continue
            self.import_table(table)

    @classmethod
    def get_index_of_column(cls, column, file_path):
        """Get index of a specific column name in a CTD file

        :param column: 
        :param file_path: 
        :return: Optional[int]
        """
        columns = cls.get_column_names_from_file(file_path)
        if column in columns:
            return columns.index(column)

    @classmethod
    def get_index_and_columns_order(cls, columns_in_file_expected: List[str], columns_dict: Dict[str, str], file_path: str):
        """

        :param columns_in_file_expected: 
        :param columns_dict: 
        :param file_path: 
        :rtype: tuple[list,list]
        """
        use_columns_with_index = []
        column_names_in_db = []

        column_names_from_file = cls.get_column_names_from_file(file_path)
        print('column_names_from_file:\t',column_names_from_file)
        if not set(columns_in_file_expected).issubset(column_names_from_file):
            log.exception(
                '%s columns are not a subset of columns %s in file %s',
                columns_in_file_expected,
                column_names_from_file,
                file_path
            )
        else:
            for index, column in enumerate(column_names_from_file):
                if column in columns_dict:
                    use_columns_with_index.append(index)
                    column_names_in_db.append(columns_dict[column])
        return use_columns_with_index, column_names_in_db

    def import_table(self, table: Table):
        """import table by Table object

        :param `manager.table_conf.Table` table: Table object
        """
        file_path = os.path.join(self.pyctd_data_dir, table.file_name)
        log.info('importing %s data into table %s', file_path, table.name)
        table_import_timer = time.time()

        self.import_table_in_db(file_path, table)

        for one_to_many_config in table.one_to_many:
            o2m_column_index = self.get_index_of_column(
                one_to_many_config.values_col, file_path)

            if o2m_column_index:

                self.import_one_to_many(
                    file_path, o2m_column_index, table, one_to_many_config.id_col)

        log.info('done importing %s in %.2f seconds',
                 table.name, time.time() - table_import_timer)

    def import_one_to_many(self, file_path, o2m_column_index, parent_table, column_in_one2many_table):
        """

        :param file_path: 
        :param column_index: 
        :param parent_table:
        :param column_in_one2many_table: 
        """
        chunks = pd.read_csv(
            file_path,
            usecols=[o2m_column_index],
            header=None,
            comment='#',
            index_col=False,
            chunksize=1000000,
            dtype=self.get_dtypes(parent_table.model),
            sep="\t"
        )

        for chunk in chunks:
            child_values = []
            parent_id_values = []

            chunk.dropna(inplace=True)
            chunk.index += 1

            for parent_id, values in chunk.iterrows():
                entry = values[o2m_column_index]
                if not isinstance(entry, str):
                    entry = str(entry)
                for value in entry.split("|"):
                    parent_id_values.append(parent_id)
                    child_values.append(value.strip())

            parent_id_column_name = parent_table.name + '__id'
            o2m_table_name = defaults.TABLE_PREFIX + \
                parent_table.name + '__' + column_in_one2many_table

            pd.DataFrame({
                parent_id_column_name: parent_id_values,
                column_in_one2many_table: child_values
            }).to_sql(name=o2m_table_name, if_exists='append', con=self.engine, index=False)

    # TODO document get_dtypes
    @staticmethod
    def get_dtypes(sqlalchemy_model):
        """

        :param sqlalchemy_model:
        :rtype: dict
        """
        mapper = inspect(sqlalchemy_model)
        return {
            x.key: alchemy_pandas_dytpe_mapper[type(x.type)]
            for x in mapper.columns
            if x.key != 'id'
        }

    def import_table_in_db(self, file_path, table: Table):
        """Imports data from CTD file into database

        :param str file_path: path to file
        :param list[int] use_columns_with_index: list of column indices in file
        :param list[str] column_names_in_db: list of column names (have to fit to models except domain_id column name)
        :param table: `manager.table.Table` object
        """
        use_columns_with_index, column_names_in_db = self.get_index_and_columns_order(
            table.columns_in_file_expected,
            table.columns_dict,
            file_path
        )
        dtype=self.get_dtypes(table.model)
        print(use_columns_with_index, '\n', column_names_in_db,'\n', dtype)

        chunks = pd.read_csv(
            file_path,
            usecols=use_columns_with_index,
            names=column_names_in_db,
            header=None, comment='#',
            index_col=False,
            chunksize=1000000,
            dtype=dtype,
            sep="\t"
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
                        chunk = pd.merge(
                            chunk, self.mapper[domain], on=domain_id, how='left')
                        del chunk[domain_id]

            chunk.set_index('id', inplace=True)

            table_with_prefix = defaults.TABLE_PREFIX + table.name
            chunk.to_sql(name=table_with_prefix,
                         if_exists='append', con=self.engine)

        del chunks

    @staticmethod
    def get_column_names_from_file(file_path: str) -> List[str]:
        """returns column names from CTD download file

        :param str file_path: path to CTD download file
        """
        if file_path.endswith('.gz'):
            file_handler = io.TextIOWrapper(
                io.BufferedReader(gzip.open(file_path)))
        else:
            file_handler = open(file_path, 'r')

        fields_line = False
        with file_handler as file:
            for line in file:
                line = line.strip()
                if not fields_line and re.search(r'#\s*Fields\s*:$', line):
                    fields_line = True
                elif fields_line and not (line == '' or line == '#'):
                    return [column.strip() for column in line[1:].split("\t")]
        return []

    @classmethod
    def download_urls(cls, urls, force_download=False):
        """Downloads all CTD URLs that don't exist

        :param iter[str] urls: iterable of URL of CTD
        :param bool force_download: force method to download
        """
        for url in urls:
            file_path = cls.get_path_to_file_from_url(url)

            if os.path.exists(file_path) and not force_download:
                log.info('already downloaded %s to %s', url, file_path)
            else:
                log.info('downloading %s to %s', url, file_path)
                download_timer = time.time()
                urlretrieve(url, file_path)
                log.info('downloaded in %.2f seconds',
                         time.time() - download_timer)

    @classmethod
    def get_path_to_file_from_url(cls, url):
        """standard file path

        :param str url: CTD download URL
        :rtype: str
        """
        file_name = urlparse(url).path.split('/')[-1]
        return os.path.join(cls.pyctd_data_dir, file_name)


def update(connection=None, urls=None, force_download=False):
    """Updates CTD database

    :param iter[str] urls: list of urls to download
    :param str connection: custom database connection string
    :param bool force_download: force method to download
    """
    db = DbManager(connection)
    db.db_import(urls=urls, force_download=force_download)
    db.session.close()


def set_mysql_connection(host='localhost', user='pyctd_user', password='pyctd_passwd', db='pyctd', charset='utf8'):
    """Sets the connection using MySQL Parameters"""
    set_connection('mysql+pymysql://{user}:{passwd}@{host}/{db}?charset={charset}'.format(
        host=host,
        user=user,
        passwd=password,
        db=db,
        charset=charset)
    )


def set_test_connection():
    """Sets the connection with the default SQLite test database"""
    set_connection(defaults.DEFAULT_SQLITE_TEST_DATABASE_NAME)


def set_connection(connection=defaults.sqlalchemy_connection_string_default):
    """Set the connection string for SQLAlchemy

    :param str connection: SQLAlchemy connection string
    """
    cfp = defaults.config_file_path
    config = RawConfigParser()

    if not os.path.exists(cfp):
        with open(cfp, 'w') as config_file:
            config['database'] = {'sqlalchemy_connection_string': connection}
            config.write(config_file)
            log.info('create configuration file %s', cfp)
    else:
        config.read(cfp)
        config.set('database', 'sqlalchemy_connection_string', connection)
        with open(cfp, 'w') as configfile:
            config.write(configfile)
