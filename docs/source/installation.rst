Installation
============

System requirements
-------------------

Because of the rich content of CTD `PyCTD` will create more than 230 million rows (04-28-017) with ~14 GiB of disk
storage (depending on the used RDMS).

Tests were performed on *Ubuntu 16.04, 4 x Intel Core i7-6560U CPU @ 2.20Ghz* with
*16 GiB of RAM*. In general PyCTD should work also on other systems like Windows, other Linux distributions or Mac OS.

.. _rdbms:

Supported Databases
-------------------

`PyCTD` uses `SQLAlchemy <http://sqlalchemy.readthedocs.io>`_ to cover a wide spectrum of RDMSs
(relational database management system). We reccomend MySQL or MariaDB for best performance. If you cannot install
software on your system, SQLite - which needs no further installation - also works.

The following RDMSs are supported by SQLAlchemy:

1. Firebird
2. Microsoft SQL Server
3. MySQL / `MariaDB <https://mariadb.org/>`_
4. Oracle
5. PostgreSQL
6. SQLite
7. Sybase

Install Software
----------------

:code:`pyctd` provides a simple API so bioinformaticians and scientists with limited programming knowledge can easily
use it to interface with CTD between chemical–gene/protein interactions, chemical–disease and gene–disease
relationships.

Easiest
~~~~~~~
Download the latest stable code from `PyPI <https://pypi.python.org/pypi/pyctd>`_ with:

.. code-block:: sh

   $ python3 -m pip install pyctd

Get the Latest
~~~~~~~~~~~~~~~
Download the most recent code from `GitHub <https://github.com/cebel/pyctd>`_ with:

.. code-block:: sh

   $ python3 -m pip install git+https://github.com/pyctd/pyctd.git

For Developers
~~~~~~~~~~~~~~
Clone the repository from `GitHub <https://github.com/cebel/pyctd>`_ and install in editable mode with:

.. code-block:: sh

   $ git clone https://github.com/pyctd/pyctd.git
   $ cd pyctd
   $ python3 -m pip install -e .

MySQL/MariaDB setup
~~~~~~~~~~~~~~~~~~~
Log in MySQL as root user and create a new database, create a user, assign the rights and flush privileges.

.. code-block:: mysql

    CREATE DATABASE pyctd CHARACTER SET utf8 COLLATE utf8_general_ci;
    GRANT ALL PRIVILEGES ON pyctd.* TO 'pyctd_user'@'%' IDENTIFIED BY 'pyctd_passwd';
    FLUSH PRIVILEGES;

Start a python shell and set the MySQL configuration. If you have not changed anything in the SQL statements ...

.. code-block:: python

    >>> import pyctd
    >>> pyctd.set_mysql_connection()

If you have used you own settings, please adapt the following command to you requirements.

.. code-block:: python

    >>> import pyctd
    >>> pyctd.set_mysql_connection()
    >>> pyctd.set_mysql_connection(host='localhost', user='pyctd_user', passwd='pyctd_passwd', db='pyctd')

Updating
~~~~~~~~
The updating process will download the files provided by the CTD on the
`download page <http://ctdbase.org/downloads/>`_

.. warning:: Please note the download needs 1.5 GB and the update takes ~2 hours (depending on your system)

.. code-block:: python

    >>> import pyctd
    >>> pyctd.update()


Changing database configuration
-------------------------------
Following functions allow to change the connection to you RDBMS (relational database management system). Next
time you will use :code:`pyctd` by default this connection will be used.

To set a new MySQL/MariaDB connection ...

.. code-block:: python

    import pyctd
    pyctd.set_mysql_connection()
    pyctd.set_mysql_connection(host='localhost', user='pyctd_user', password='pyctd_passwd', db='pyctd')

To set connection to other database systems use the `pyctd.set_connection` function.

For more information about connection strings go to
the `SQLAlchemy documentation <http://docs.sqlalchemy.org/en/latest/core/engines.html>`_.

Examples for valid connection strings are:

- mysql+pymysql://user:passwd@localhost/database?charset=utf8
- postgresql://scott:tiger@localhost/mydatabase
- mssql+pyodbc://user:passwd@database
- oracle://user:passwd@127.0.0.1:1521/database
- Linux: sqlite:////absolute/path/to/database.db
- Windows: sqlite:///C:\\path\\to\\database.db

.. code-block:: python

    import pyctd
    pyctd.set_connection('oracle://user:passwd@127.0.0.1:1521/database')
