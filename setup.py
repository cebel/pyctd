#!/usr/bin/env python

import sys
import re
import os
from setuptools import setup, find_packages
import codecs

PACKAGES = find_packages(where='src')

INSTALL_REQUIRES = [
    'sqlalchemy',
    'pandas',
    'pymysql',
    'requests',
    'click',
]

if sys.version_info < (3,):
    INSTALL_REQUIRES.append('configparser')

ENTRY_POINTS = {
    'console_scripts': [
        'pyctd = pyctd.cli:main',
    ]
}

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """Build an absolute path from *parts* and return the contents of the resulting file. Assume UTF-8 encoding."""
    with codecs.open(os.path.join(HERE, *parts), 'rb', 'utf-8') as f:
        return f.read()

META_PATH = os.path.join('src', 'pyctd', '__init__.py')
META_FILE = read(META_PATH)


def find_meta(meta):
    """Extract __*meta*__ from META_FILE"""
    meta_match = re.search(
        r'^__{meta}__ = ["\']([^"\']*)["\']'.format(meta=meta),
        META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError('Unable to find __{meta}__ string'.format(meta=meta))

setup(
    name=find_meta('title'),
    version=find_meta('version'),
    url=find_meta('url'),
    author=find_meta('author'),
    author_email=find_meta('email'),
    maintainer='Christian Ebeling',
    maintainer_email=find_meta('email'),
    description=find_meta('description'),
    license=find_meta('license'),
    packages=PACKAGES,
    install_requires=INSTALL_REQUIRES,
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Database',
    ],
    entry_points=ENTRY_POINTS,
)
