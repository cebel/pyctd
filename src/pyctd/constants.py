# -*- coding: utf-8 -*-

import os

PYCTD_DIR = os.path.expanduser('~/.pyctd')
if not os.path.exists(PYCTD_DIR):
    os.mkdir(PYCTD_DIR)

PYCTD_DATA_DIR = os.path.join(PYCTD_DIR, 'data')
if not os.path.exists(PYCTD_DATA_DIR):
    os.mkdir(PYCTD_DATA_DIR)


