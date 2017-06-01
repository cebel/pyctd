PyCTD |stable_build| |stable_documentation| |pypi_license|
==========================================================

`PyBEL <http://pyctd.readthedocs.io>`_ is software library developed by the
`Department of Bioinformatics <https://www.scai.fraunhofer.de/en/business-research-areas/bioinformatics.html>`_
at the Fraunhofer Institute for Algorithms and Scientific Computing
`SCAI <https://www.scai.fraunhofer.de/en.html>`_
to access and query data provided by the `Comparative Toxicogenomics Database <http://ctdbase.org>`_.
For more in for information about CTD go to
`this section in the documentation <http://pyctd.readthedocs.io/en/latest/ctd.html>`_.

This development is supported by following `IMI <https://www.imi.europa.eu/>`_ projects:
- `AETIONOMY <http://www.aetionomy.eu/>`_ and
- `PHAGO <http://www.phago.eu/>`_.

.. image:: http://www.imi.europa.eu/webfm_send/1714
   :width: 150 px
   :target: http://www.imi.europa.eu

.. image:: http://www.aetionomy.eu/content/dam/scai/AETIONOMY/Logo-Aetionomy.png
   :width: 150 px
   :target: http://www.aetionomy.eu/en/vision.html

.. image:: https://www.scai.fraunhofer.de/content/dam/scai/scai_logo.svg
   :width: 150 px
   :target: https://www.scai.fraunhofer.de/en/business-research-areas/bioinformatics.html

Getting Started
---------------

This is a quick start tutorial for impatient.

Installation
~~~~~~~~~~~~

PyCTD can be installed with `pip <https://pip.pypa.io/en/stable/>`_.

.. code-block:: bash

    pip install pyctd

If you fail because you have no rights to install use superuser (sudo on Linux before the commend) or ...

.. code-block:: bash

    pip install --user pyctd

If you want to make sure you are installing this under python3 use ...

.. code-block:: bash

    python3 -m pip install pyctd

SQLite
~~~~~~

.. note:: If you want to use SQLite as your database system, because you ...

    - have no possibility to use RDMSs like MySQL/MariaDB
    - just test pyctd, but don't want to spend time in setting up a database
    skip the next *MySQL/MariaDB setup* section. But in general we recommend MySQL or MariaDB as your RDBMS.

If you don't know what all that means skip the section *MySQL/MariaDB setup*.

Don't worry! You can always later change the configuration. For more information about
changing database system later go to
`Changing database configuration <http://pyctd.readthedocs.io/en/latest/installation.html#changing-database-configuration>`_
in the documentation on readthedocs.

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

    import pyctd
    pyctd.set_mysql_connection()
    pyctd.set_mysql_connection(host='localhost', user='pyctd_user', passwd='pyctd_passwd', db='pyctd')

Updating
~~~~~~~~

The updating process will download the files provided by the CTD team on the
`download page <http://ctdbase.org/downloads/>`_

.. warning:: Please note that download files needs 1,5Gb of disk space and the update takes ~2h (depending on your system)

.. code-block:: python

    import pyctd
    pyctd.update()

Test a query function
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> query = pyctd.query()
    >>> results =query.get_chem_gene_interaction_actions(gene_name='APP', interaction_action='meman%', limit=1)
    >>> first_result = r
    >>> r.chemical
    Memantine
    >>> r.pubmed_ids
    [21290839]
    >>> r.chemical.drugbank_ids
    [DB014043]


Installation
------------

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
Comparative Toxicogenomics Database (CTD)
- `CTD website http://ctdbase.org/`_
- `All CTD publications <http://ctdbase.org/about/publications/#ctdpubs>`_
- `CTD download page <http://ctdbase.org/downloads/>`_

PyCTD
- Documented on `Read the Docs <http://pyctd.readthedocs.io/>`_
- Versioned on `GitHub <https://github.com/cebel/pyctd>`_
- Tested on `Travis CI <https://travis-ci.org/cebel/pyctd>`_
- Distributed by `PyPI <https://pypi.python.org/pypi/pyctd>`_
- Chat on `Gitter <https://gitter.im/pyctd/Lobby>`_

.. |stable_build| image:: https://travis-ci.org/cebel/pyctd.svg?branch=master
    :target: https://travis-ci.org/cebel/pyctd
    :alt: Stable Build Status

.. |stable_documentation| image:: https://readthedocs.org/projects/pyctd/badge/?version=latest
    :target: http://pyctd.readthedocs.io/en/latest/
    :alt: Development Documentation Status

.. |pypi_license| image:: https://img.shields.io/pypi/l/PyCTD.svg
    :alt: Apache 2.0 License