# -*- coding: utf-8 -*-

"""
Module that contains the command line app

Why does this file exist, and why not put this in __main__?
You might be tempted to import things from __main__ later, but that will cause
problems--the code will get executed twice:
 - When you run `python -m pyctd` python will execute
   ``__main__.py`` as a script. That means there won't be any
   ``pyctd.__main__`` in ``sys.modules``.
 - When you import __main__ it will get executed again (as a module) because
   there's no ``pyctd.__main__`` in ``sys.modules``.
Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""

import logging
import os
import sys
import time

import click

from .constants import PYCTD_DIR
from .manager.database import update

log = logging.getLogger('pyctd')

formatter = logging.Formatter('%(name)s:%(levelname)s - %(message)s')
logging.basicConfig(format=formatter)

fh_path = os.path.join(PYCTD_DIR, time.strftime('pyctd_%Y_%m_%d_%H_%M_%S.txt'))
fh = logging.FileHandler(fh_path)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
log.addHandler(fh)


@click.group(help="PyCTD Command Line Utilities on {}".format(sys.executable))
@click.version_option()
def main():
    pass


@main.command()
@click.option('--path', help='path to folder with CTD file')
@click.option('--con', help='SQL Alchemy connection string')
def update():
    update()


@main.group(help="PyCTD help text")
def manage():
    pass

if __name__ == '__main__':
    main()
