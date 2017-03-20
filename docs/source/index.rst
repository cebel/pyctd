PyCTD Documentation
===================

.. image:: http://adaptsmart.eu/wp-content/uploads/2015/09/imi-logo.png
   :width: 200 px

.. image:: http://www.aetionomy.eu/content/dam/scai/AETIONOMY/Logo-Aetionomy.png
   :width: 200 px

.. image:: https://www.scai.fraunhofer.de/content/dam/scai/scai_logo.svg
   :width: 200 px

PyCTD is an easy to use python interface developed by the
`Department of Bioinformatics <https://www.scai.fraunhofer.de/en/business-research-areas/bioinformatics.html>`_
at the Fraunhofer Institute for Algorithms and Scientific Computing
`SCAI <https://www.scai.fraunhofer.de/en.html>`_
to the data provided by the Comparative Toxicogenomics Database
(`CTD <http://ctdbase.org>`_, see also `latest publication <https://www.ncbi.nlm.nih.gov/pubmed/27651457>`_
about CTD: Nucleic Acids Res. 2017 Jan 4;45(D1):D972-D978. doi: 10.1093/nar/gkw838. Epub 2016 Sep 19; authors:
Davis AP, Grondin CJ, Johnson RJ, Sciaky D, King BL, McMorran R, Wiegers J, Wiegers TC, Mattingly CJ).

CTD is a robust, publicly available database that aims to advance understanding about how environmental exposures
affect human health. It provides manually curated information about chemical–gene/protein interactions,
chemical–disease and gene–disease relationships.
These data are integrated with functional and pathway data to aid in development of hypotheses about the mechanisms
underlying environmentally influenced diseases.
The content of CTD and the use of PyCTD in combination with `PyBEL <https://pyctd.readthedocs.io/en/latest/>`_ supports
scientists in the `IMI <https://www.imi.europa.eu/>`_ funded project, `AETIONOMY <http://www.aetionomy.eu/>`_ ,
successfully in the approach to identify potential drugs in complex disease networks with several thousands of
relationships store in `BEL <http://openbel.org/>`_ statements.


:code:`pyctd` is a Python software package that parses data provided by CTD and stores these data in a database.
Because of the internal use of the Python SQL toolkit and Object Relational Mapper
`SQLAlchemy <https://www.sqlalchemy.org/>`_ it allows to store the data in several different relational
database management systems (RDBMS) like PostgreSQL, MySQL, Oracle, Microsoft SQL Server, SQLite and others.

:code:`pyctd` provides a simple API so bioinformaticians and scientists with limited programming knowledge can easily
use it to interface with CTD between chemical–gene/protein interactions, chemical–disease and gene–disease
relationships.

Donload with :code:`git clone https://github.com/cebel/pyctd.git`

Change to folder :code:`cd pyctd`

Install with pip :code:`pip install -e .`


.. toctree::
   :maxdepth: 2

   installation
   overview
   datamodel
   io
   cookbook
   commandline
   troubleshooting
   logging

.. toctree::
   :caption: Reference
   :name: reference

   parser
   manager
   utilities

.. toctree::
   :caption: Project
   :name: project

   roadmap
   technology

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
