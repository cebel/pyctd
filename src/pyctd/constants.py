# -*- coding: utf-8 -*-

import os

PYCTD_DIR = os.path.expanduser('~/.pyctd')
if not os.path.exists(PYCTD_DIR):
    os.mkdir(PYCTD_DIR)

PYCTD_DATA_DIR = os.path.join(PYCTD_DIR, 'data')
if not os.path.exists(PYCTD_DATA_DIR):
    os.mkdir(PYCTD_DATA_DIR)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'