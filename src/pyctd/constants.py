# -*- coding: utf-8 -*-

import os

PYCTD_DIR = os.path.expanduser('~/.pyctd')
if not os.path.exists(PYCTD_DIR):
    os.mkdir(PYCTD_DIR)

PYCTD_DATA_DIR = os.path.join(PYCTD_DIR, 'data')
if not os.path.exists(PYCTD_DATA_DIR):
    os.mkdir(PYCTD_DATA_DIR)

DEFAULT_SQLITE_DATABASE_NAME = 'pyctd.db'
DEFAULT_SQLITE_TEST_DATABASE_NAME = 'pyctd_test.db'
DEFAULT_DATABASE_LOCATION = os.path.join(PYCTD_DATA_DIR, DEFAULT_SQLITE_DATABASE_NAME)
DEFAULT_TEST_DATABASE_LOCATION = os.path.join(PYCTD_DATA_DIR, DEFAULT_SQLITE_TEST_DATABASE_NAME)
