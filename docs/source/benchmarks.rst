Benchmarks
==========

All benchmarks created on a standard notebook:

- OS: Linux Ubuntu 16.04.2 LTS (xenial)
- Python: 3.5.2
- Hardware: x86_64, Intel(R) Core(TM) i7-6560U CPU @ 2.20GHz, 4 CPUs, Mem 16Gb

MySQL/MariaDB
-------------

Database created with following command in MySQL/MariaDB as root:

.. code:: sql

    CREATE DATABASE mydatabase CHARACTER SET utf8 COLLATE utf8_general_ci;

User created with following command in MySQL/MariaDB:

.. code:: sql

    GRANT ALL PRIVILEGES ON pyctd.* TO 'pyctd_user'@'%' IDENTIFIED BY 'pyctd_passwd';
    FLUSH PRIVILEGES;

Import of CTD data executed with:

.. code:: python

    import pyctd
    pyctd.set_mysql_connection()
    pyctd.update()
    
- CPU times: user 2h 2min 20s, sys: 37.7 s, total: 2h 2min 58s

