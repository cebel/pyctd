# -*- coding: utf-8 -*-

"""
This file contains a listing of the default CTD URLs.
"""
import os

from ..constants import PYCTD_DIR, PYCTD_DATA_DIR

DEFAULT_SQLITE_DATABASE_NAME = 'pyctd.db'
DEFAULT_SQLITE_TEST_DATABASE_NAME = 'pyctd_test.db'
DEFAULT_DATABASE_LOCATION = os.path.join(PYCTD_DATA_DIR, DEFAULT_SQLITE_DATABASE_NAME)
DEFAULT_TEST_DATABASE_LOCATION = os.path.join(PYCTD_DATA_DIR, DEFAULT_SQLITE_TEST_DATABASE_NAME)

url_base = "http://ctdbase.org/reports/"

sqlalchemy_connection_string_default = 'sqlite:///' + DEFAULT_DATABASE_LOCATION
sqlalchemy_connection_string_4_tests = 'sqlite:///' + DEFAULT_SQLITE_TEST_DATABASE_NAME

sqlalchemy_connection_string_4_mysql = 'mysql+pymysql://pyctd:pyctd@localhost/pyctd?charset=utf8'
sqlalchemy_connection_string_4_mysql_tests = 'mysql+pymysql://pyctd:pyctd@localhost/pyctd_test?charset=utf8'

value_delimiter = '\|'

TABLE_PREFIX = 'pyctd_'

config_file_path = os.path.join(PYCTD_DIR, 'config.ini')
