# -*- coding: utf-8 -*-

"""

PyCTD is tested on both Python2.7 and Python3

.. warning:: PyCTD is not thoroughly tested on Windows.

Installation
------------

.. code-block:: bash

    pip install pyctd
"""

from . import manager
from .manager.database import update
from .manager.database import set_connection, set_mysql_connection
from .manager.query import QueryManager as query

__all__ = ['update', 'query', 'set_connection', 'set_mysql_connection']

__version__ = '0.5.6'

__title__ = 'PyCTD'
__description__ = 'Importing and querying CTD'
__url__ = 'https://github.com/cebel/pyctd'

__author__ = 'Christian Ebeling'
__email__ = 'christian.ebeling@scai.fraunhofer.de'

__license__ = 'Apache 2.0 License'
__copyright__ = 'Copyright (c) 2017 Christian Ebeling, Fraunhofer Institute for Algorithms and Scientific Computing SCAI, Schloss Birlinghoven, 53754 Sankt Augustin, Germany'