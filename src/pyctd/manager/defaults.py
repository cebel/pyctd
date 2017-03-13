# -*- coding: utf-8 -*-

"""
This file contains a listing of the default CTD URLs.
"""
from .table_conf import tables
import os
from ..constants import DEFAULT_CACHE_LOCATION

url_base = "http://ctdbase.org/reports/"

sqlalchemy_connection_string = 'mysql+pymysql://pyctd:pyctd@localhost/pyctd?charset=utf8'
# sqlalchemy_connection_string = 'sqlite:///' + DEFAULT_CACHE_LOCATION

urls = [url_base + tables[table]['file_name'] for table in tables]

value_delimiter = '\|'

TABLE_PREFIX = 'pyctd_'