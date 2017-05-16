Quick start
-----------

This guide helps you to quickly setup your system in several minutes. But running the database import process and
indexing takes still several hours.

.. note::
    If your colleague have already executed the import process (perhaps on a special database server)
    please request the connection data to use PyCTD without the need of running the update process.

Please make sure you have installed

1. `MariaDB <https://mariadb.org/>`_ or any other supported RDMS :ref:`rdbms`
2. `Python3 <https://www.python.org/downloads/>`_

Please note that you can also install with `pip` even if you are have no root rights on your machine.
Just add `--user` behind `install`.

.. code-block:: python

    python3 -m pip install pyctd

Make sure that you have access to a database with user name and correct permissions. Otherwise execute on the MariaDB
or MySQL console the flowing command as root. Replace user name, password and servername (here `localhost`) to
our needs:

.. code-block:: sql

    CREATE DATABASE `pyctd` CHARACTER SET utf8 COLLATE utf8_general_ci;
    CREATE USER 'pyctd_user'@'localhost' IDENTIFIED BY 'pyctd_passwd';
    GRANT ALL PRIVILEGES ON pytcd.* TO 'pyctd_user'@'localhost';
    FLUSH PRIVILEGES;

Import CTD data into database, but before change the SQLAlchemy connection string (line 2) to allow a connection
to the database. If you have used the default code block and don't have to change anything.

Start your python console:

.. code-block:: bash

    python3

Import the data:

.. code-block:: python

    import pyctd
    sqlalchemy_connection_string = 'mysql+pymysql://db_user:db_pwd@server_name/db_name?charset=utf8'
    pyctd.update(sqlalchemy_connection_string)

For examples how to query the database go to :class:`pyctd.manager.database.Query` or `Tutorial`