# -*- coding: utf-8 -*-

"""
This file contains a listing of the default CTD URLs.
"""
from .table_conf import tables
from ..constants import DEFAULT_DATABASE_LOCATION, DEFAULT_SQLITE_TEST_DATABASE_NAME

url_base = "http://ctdbase.org/reports/"

sqlalchemy_connection_string_default = 'sqlite:///' + DEFAULT_DATABASE_LOCATION
sqlalchemy_connection_string_4_tests = 'sqlite:///' + DEFAULT_SQLITE_TEST_DATABASE_NAME

sqlalchemy_connection_string_4_mysql = 'mysql+pymysql://pyctd:pyctd@localhost/pyctd?charset=utf8'
sqlalchemy_connection_string_4_mysql_tests = 'mysql+pymysql://pyctd:pyctd@localhost/pyctd_test?charset=utf8'

urls = [url_base + tables[table]['file_name'] for table in tables]

value_delimiter = '\|'

TABLE_PREFIX = 'pyctd_'