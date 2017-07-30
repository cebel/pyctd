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

from . import manager
from .constants import PYCTD_DIR
from .manager.database import get_connection_string

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger('pyctd')
log.setLevel(logging.INFO)

fh_path = os.path.join(PYCTD_DIR, time.strftime('pyctd_%Y_%m_%d_%H_%M_%S.txt'))
fh = logging.FileHandler(fh_path)
fh.setLevel(logging.DEBUG)
log.addHandler(fh)


@click.group(help="PyCTD Command Line Utilities on {}".format(sys.executable))
@click.version_option()
def main():
    pass


@main.command()
@click.option('-c', '--connection', help='Connection string. Defaults to {}'.format(get_connection_string()))
@click.option('-f', '--force_download', is_flag=True, help='forces download; overwrites last download')
def update(connection, force_download):
    """Update the database"""
    manager.database.update(
        connection=connection,
        force_download=force_download
    )


@main.command()
@click.argument('connection')
def set_connnection(connection):
    """Set the SQLAlchemy connection string"""
    manager.database.set_connection(connection)


@main.command()
@click.option('-h', '--host', default='localhost')
@click.option('-u', '--user', default='pyctd_user')
@click.option('-p', '--password', default='pyctd_passwd')
@click.option('-d', '--db', default='pyctd')
@click.option('-c', '--charset', default='utf8')
def set_mysql(host, user, password, db, charset):
    """Set the SQLAlchemy connection string with MySQL settings"""
    manager.database.set_mysql_connection(
        host=host,
        user=user,
        password=password,
        db=db,
        charset=charset
    )


@main.command()
def get_connection():
    """Get the connection string"""
    click.echo(get_connection_string())


if __name__ == '__main__':
    main()
