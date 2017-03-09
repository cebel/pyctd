"""

PyCTD is tested on both Python3

.. warning:: PyCTD is not thoroughly tested on Windows.

Installation
------------

.. code-block:: sh

   $ git clone https://github.com/cebel/pyctd.git
   $ cd pyctd
   $ pip3 install -e .
"""

from .manager.database import update

__all__ = ['update']

__version__ = '0.0.2'

__title__ = 'PyCTD'
__description__ = 'Importing and querying CTD'
__url__ = 'https://github.com/cebel/pyctd'

__author__ = 'Christian Ebeling, Charles Tapley Hoyt, Andrej Konotopez'
__email__ = 'christian.ebeling@scai.fraunhofer.de'

__license__ = 'Apache 2.0 License'
__copyright__ = 'Copyright (c) 2016 Christian Ebeling, Charles Tapley Hoyt, Andrej Konotopez'