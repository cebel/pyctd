Installation
============

System requirements
-------------------

Because of the rich content of CTD `PyCTD` will create more than 230 million rows (04-28-017) with ~14 GiB of disk
storage (depending on the used RDMS).

Tests were performed on *Ubuntu 16.04, 4 x Intel Core i7-6560U CPU @ 2.20Ghz* with
*16 GiB of RAM*. In general PyCTD should work also on other systems like Windows, other Linux distributions or Mac OS.

.. _rdbms:

Supported databases
-------------------

`PyCTD` uses `SQLAlchemy <http://sqlalchemy.readthedocs.io>`_ to cover a wide spectrum of RDMSs
(Relational database management system). For best performance MySQL or MariaDB is recommended. But if you have no
possibility to install software on your system SQLite - which needs no further
installation - also works. Following RDMSs are supported (by SQLAlchemy):

1. Firebird
2. Microsoft SQL Server
3. MySQL / `MariaDB <https://mariadb.org/>`_
4. Oracle
5. PostgreSQL
6. SQLite
7. Sybase

Setup of database configuration
-------------------------------

First time you import :code:`pyctd` in the python console it's time to configure our database configurations:



Install software
----------------

:code:`pyctd` provides a simple API so bioinformaticians and scientists with limited programming knowledge can easily
use it to interface with CTD between chemical–gene/protein interactions, chemical–disease and gene–disease
relationships.

Donload with :code:`git clone https://github.com/cebel/pyctd.git`

Change to folder :code:`cd pyctd`

Install with pip :code:`pip install -e .`


Changing database configuration
-------------------------------

Can can always change the configuration of your database system.