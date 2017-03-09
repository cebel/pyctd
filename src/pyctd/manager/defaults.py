# -*- coding: utf-8 -*-

"""
This file contains a listing of the default CTD URLs.
"""
from .table_conf import tables

url_base = "http://ctdbase.org/reports/"

sqlalchemy_connection_string = 'mysql+pymysql://pyctd:pyctd@localhost/pyctd2?charset=utf8'

urls = [url_base + tables[table]['file_name'] for table in tables]

value_delimiter = '|'