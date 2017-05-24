PyCTD |develop_build| |develop_coverage| |develop_documentation|
================================================================
456
:code:`pyctd` is a Python software package that allows fast queries  and easy python access to CTD. It parses the
original files and stores the content in a database. Thanks to SQLAlchemy data can be stored in different RDBMS
(relational database management systems) like PostgreSQL, MySQL, Oracle, Microsoft SQL Server, SQLite and others.

Many functions in :code:`pyctd.query` allows a fast and easy access to many relations in CTD.


Requirements
------------

* SQLAlchemy
* Pandas

Installation
------------

|pypi_version| |python_versions| |pypi_license|


PyCTD can be installed easily from `PyPI <https://pypi.python.org/pypi/pyctd>`_ with the following code in
your favorite terminal:

.. code-block:: sh

   python3 -m pip install pyctd

See the `installation documentation <http://pyctd.readthedocs.io/en/latest/installation.html>`_ for more advanced
instructions. Also, check the change log at :code:`CHANGELOG.rst`.

CTD tools and licence (use of data)
-----------------------------------

CTD provides also many online `query interfaces <http://ctdbase.org/search/>`_ and
`tools to analyse data <http://ctdbase.org/tools/>`_ on their website.

Please be aware of the `CTD licence <http://ctdbase.org/about/legal.jsp>`_ which allows the use of data only for
research and educational purposes. Medical treatment decisions should not be made based on the information in CTD.

Any reproduction or use for commercial purpose is prohibited without the prior express written permission of the
MDI Biological Laboratory and NC State University.


Links
-----

- Specified by `CTD database http://ctdbase.org/`_
- Documented on `Read the Docs <http://pyctd.readthedocs.io/>`_
- Versioned on `GitHub <https://github.com/cebel/pyctd>`_
- Tested on `Travis CI <https://travis-ci.org/cebel/pyctd>`_
- Distributed by `PyPI <https://pypi.python.org/pypi/pyctd>`_