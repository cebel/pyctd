Query
=====

.. contents::

Examples
--------
For most of the string parameters you can use % as wildcard (please check the documentation below). All methods
have a parameter ``limit`` which allows to limit the number of results.

Methods
~~~~~~~
.. code-block:: python
    :linenos:

    import pyctd
    q = pyctd.query
    q.get_diseases(disease_id='MESH:D000544', definition='%degenerative%')
    q.get_genes(gene_symbol='TSP_15922', uniprot_id='E5T972')
    q.get_pathways(pathway_name='%bla')
    q.get_chemicals(chemical_name='Alz%')
    q.get_chem_gene_interaction_action(organism_id='9606', gene_symbol='APP')
    q.get_gene__diseases(limit=10)

Properties
~~~~~~~~~~
.. code-block:: python
    :linenos:

    >>> import pyctd
    >>> q = pyctd.query
    >>> q.gene_forms
    >>> q.interaction_actions
    >>> q.actions
    >>> q.pathways

Query Manager Reference
-----------------------
.. autoclass:: pyctd.manager.query.QueryManager
    :members: