# -*- coding: utf-8 -*-

from .database import BaseDbManager
from . import models
from sqlalchemy import distinct
from pandas import read_sql


class QueryManager(BaseDbManager):
    """Query interface to database."""

    def _limit_and_df(self, query, limit, as_df=False):
        """adds a limit (limit==None := no limit) to any query and allow a return as pandas.DataFrame

        :param bool as_df: if is set to True results return as pandas.DataFrame
        :param `sqlalchemy.orm.query.Query` query: SQL Alchemy query 
        :param int limit: maximum number of results
        :return: query result of pyctd.manager.models.XY objects
        """
        if limit:
            query = query.limit(limit)

        if as_df:
            results = read_sql(query.statement, self.engine)
        else:
            results = query.all()

        return results

    def _join_gene(self, query, gene_name, gene_symbol, gene_id):
        """helper function to add a query join to Gene model

        :param `sqlalchemy.orm.query.Query` query: SQL Alchemy query 
        :param str gene_name: gene name
        :param str gene_symbol: gene symbol
        :param int gene_id: NCBI Gene identifier
        :return: `sqlalchemy.orm.query.Query` object
        """
        if gene_name or gene_symbol:
            query = query.join(models.Gene)

            if gene_symbol:
                query = query.filter(models.Gene.gene_symbol.like(gene_symbol))

            if gene_name:
                query = query.filter(models.Gene.gene_name.like(gene_name))

            if gene_id:
                query = query.filter(models.Gene.gene_id.like(gene_id))

        return query

    def _join_chemical(self, query, cas_rn, chemical_id, chemical_name, chemical_definition):
        """helper function to add a query join to Chemical model
        
        :param `sqlalchemy.orm.query.Query` query: SQL Alchemy query 
        :param cas_rn: 
        :param chemical_id: 
        :param chemical_name: 
        :param chemical_definition: 
        :return: `sqlalchemy.orm.query.Query` object 
        """
        if cas_rn or chemical_id or chemical_name or chemical_definition:
            query = query.join(models.Chemical)

            if cas_rn:
                query = query.filter(models.Chemical.cas_rn.like(cas_rn))

            if chemical_id:
                query = query.filter(models.Chemical.chemical_id == chemical_id)

            if chemical_name:
                query = query.filter(models.Chemical.chemical_name.like(chemical_name))

            if chemical_definition:
                query = query.filter(models.Chemical.definition.like(chemical_definition))

        return query

    def _join_disease(self, query, disease_definition, disease_id, disease_name):
        """helper function to add a query join to Disease model
        
        :param `sqlalchemy.orm.query.Query` query: SQL Alchemy query 
        :param disease_definition: 
        :param disease_id: 
        :param disease_name: 
        :return: `sqlalchemy.orm.query.Query` object
        """
        if disease_definition or disease_id or disease_name:
            query = query.join(models.Disease)

            if disease_definition:
                query = query.filter(models.Disease.definition.like(disease_definition))

            if disease_id:
                query = query.filter(models.Disease.disease_id == disease_id)

            if disease_name:
                query = query.filter(models.Disease.disease_name.like(disease_name))

        return query

    def _join_pathway(self, query, pathway_id, pathway_name):
        """helper function to add a query join to Pathway model
        
        :param `sqlalchemy.orm.query.Query` query: SQL Alchemy query  
        :param str pathway_id: pathway identifier
        :param str pathway_name: pathway name
        :return: `sqlalchemy.orm.query.Query` object
        """
        if pathway_id or pathway_name:
            if pathway_id:
                query = query.filter(models.Pathway.pathway_id.like(pathway_id))
            if pathway_name:
                query = query.filter(models.Pathway.pathway_name.like(pathway_name))
        return query

    def get_disease(self, disease_name=None, disease_id=None, definition=None, parent_ids=None, tree_numbers=None,
                    parent_tree_numbers=None, slim_mapping=None, synonym=None, alt_disease_id=None, limit=None,
                    as_df=False):
        """
        Get diseases

        :param bool as_df: if set to True result returns as `pandas.DataFrame`
        :param int limit: maximum number of results
        :param str disease_name: disease name
        :param str disease_id: disease identifier
        :param str definition: definition of disease
        :param str parent_ids: parent identifiers, delimiter |
        :param str tree_numbers: tree numbers, delimiter |
        :param str parent_tree_numbers: parent tree numbers, delimiter
        :param str slim_mapping:  term derived from the MeSH tree structure for the “Diseases” [C] branch, \
        that classifies MEDIC diseases into high-level categories
        :param str synonym: disease synonyms
        :param str alt_disease_id: alternative disease identifiers
        :return: list of :class:`pyctd.manager.models.Disease` object


        .. seealso::

            :class:`pyctd.manager.models.Disease`

        .. todo::
            normalize parent_ids, tree_numbers and parent_tree_numbers in :class:`pyctd.manager.models.Disease`
        """
        q = self.session.query(models.Disease)
        if disease_name:
            q = q.filter(models.Disease.disease_name.like(disease_name))
        if disease_id:
            q = q.filter(models.Disease.disease_id == disease_id)
        if definition:
            q = q.filter(models.Disease.definition.like(definition))
        if parent_ids:
            q = q.filter(models.Disease.parent_ids.like(parent_ids))
        if tree_numbers:
            q = q.filter(models.Disease.tree_numbers.like(tree_numbers))
        if parent_tree_numbers:
            q = q.filter(models.Disease.parent_tree_numbers.like(parent_tree_numbers))
        if slim_mapping:
            q = q.join(models.DiseaseSlimmapping).filter(models.DiseaseSlimmapping.slim_mapping.like(slim_mapping))
        if synonym:
            q = q.join(models.DiseaseSynonym).filter(models.DiseaseSynonym.synonym.like(synonym))
        if alt_disease_id:
            q = q.join(models.DiseaseAltdiseaseid).filter(models.DiseaseAltdiseaseid.alt_disease_id == alt_disease_id)

        return self._limit_and_df(q, limit, as_df)

    def get_gene(self, gene_name=None, gene_symbol=None, gene_id=None, synonym=None, uniprot_id=None,
                 pharmgkb_id=None, biogrid_id=None, alt_gene_id=None, limit=None, as_df=False):
        """Get genes

        :param bool as_df: if set to True result returns as `pandas.DataFrame`
        :param alt_gene_id: 
        :param str gene_name: gene name
        :param str gene_symbol: gene symbol
        :param int gene_id: NCBI Gene identifier
        :param str synonym: Synonym
        :param str uniprot_id: UniProt primary accession number
        :param str pharmgkb_id: PharmGKB identifier 
        :param int biogrid_id: BioGRID identifier
        :param int limit: maximum of results 
        :return: list of :class:`pyctd.manager.models.Gene` objects

        .. seealso::

            :class:`pyctd.manager.models.Gene`
        """
        q = self.session.query(models.Gene)
        if gene_symbol:
            q = q.filter(models.Gene.gene_symbol.like(gene_symbol))
        if gene_name:
            q = q.filter(models.Gene.gene_name.like(gene_name))
        if gene_id:
            q = q.filter(models.Gene.gene_id.like(gene_id))
        if synonym:
            q = q.join(models.GeneSynonym).filter(models.GeneSynonym.synonym == synonym)
        if uniprot_id:
            q = q.join(models.GeneUniprot).filter(models.GeneUniprot.uniprot_id == uniprot_id)
        if pharmgkb_id:
            q = q.join(models.GenePharmgkb).filter(models.GenePharmgkb.pharmgkb_id == pharmgkb_id)
        if biogrid_id:
            q = q.join(models.GeneBiogrid).filter(models.GeneBiogrid.biogrid_id == biogrid_id)
        if alt_gene_id:
            q = q.join(models.GeneAltGeneId.alt_gene_id == alt_gene_id)

        return self._limit_and_df(q, limit, as_df)

    def get_pathway(self, pathway_name=None, pathway_id=None, limit=None, as_df=False):
        """Get pathway

        .. note::
            Format of pathway_id is KEGG:X* or REACTOME:X* . X* stands for a sequence of digits

        :param bool as_df: if set to True result returns as `pandas.DataFrame`
        :param str pathway_name: pathway name
        :param str pathway_id: KEGG or REACTOME identifier
        :param int limit: maximum number of results
        :return: list of :class:`pyctd.manager.models.Pathway` objects

        .. seealso::

            :class:`pyctd.manager.models.Pathway`
        """
        q = self.session.query(models.Pathway)
        if pathway_name:
            q = q.filter(models.Pathway.pathway_name.like(pathway_name))
        if pathway_id:
            q = q.filter(models.Pathway.pathway_name.like(pathway_id))

        return self._limit_and_df(q, limit, as_df)

    def get_chemical(self, chemical_name=None, chemical_id=None, cas_rn=None, drugbank_id=None, parent_id=None,
                     parent_tree_number=None, tree_number=None, synonym=None, limit=None, as_df=False):
        """Get chemical

        :param bool as_df: if set to True result returns as `pandas.DataFrame`
        :param str chemical_name: chemical name
        :param str chemical_id: cehmical identifier 
        :param str cas_rn: CAS registry number
        :param str drugbank_id: DrugBank identifier 
        :param str parent_id: identifiers of the parent terms
        :param str parent_tree_number: identifiers of the parent nodes
        :param str tree_number: identifiers of the chemical's nodes
        :param str synonym: chemical synonym
        :param int limit: maximum number of results 
        :return: list of :class:`pyctd.manager.models.Chemical` objects
        

        .. seealso::

            :class:`pyctd.manager.models.Chemical`
        """
        q = self.session.query(models.Chemical)
        if chemical_name:
            q = q.filter(models.Chemical.chemical_name.like(chemical_name))
        if chemical_id:
            q = q.filter(models.Chemical.chemical_id == chemical_id)
        if cas_rn:
            q = q.filter(models.Chemical.cas_rn == cas_rn)
        if drugbank_id:
            q = q.join(models.ChemicalDrugbank).filter(models.ChemicalDrugbank.drugbank_id == drugbank_id)
        if parent_id:
            q = q.join(models.ChemicalParentid).filter(models.ChemicalParentid.parent_id == parent_id)
        if tree_number:
            q = q.join(models.ChemicalTreenumber) \
                .filter(models.ChemicalTreenumber.tree_number == tree_number)
        if parent_tree_number:
            q = q.join(models.ChemicalParenttreenumber) \
                .filter(models.ChemicalParenttreenumber.parent_tree_number == parent_tree_number)
        if synonym:
            q = q.join(models.ChemicalSynonym).filter(models.ChemicalSynonym.synonym.like(synonym))

        return self._limit_and_df(q, limit, as_df)

    def get_chem_gene_interaction_actions(self, gene_name=None, gene_symbol=None, gene_id=None, limit=None,
                                          cas_rn=None, chemical_id=None, chemical_name=None, organism_id=None,
                                          interaction_sentence=None, chemical_definition=None,
                                          gene_form=None, interaction_action=None, as_df=False):
        """
        Get all interactions for chemicals on a gene or biological entity (linked to this gene). 

        Chemicals can interact on different types of biological entities linked to a gene. A list of allowed
        entities linked to a gene can be retrieved via the attribute :attr:`~.gene_forms`.

        Interactions are classified by a combination of interaction ('affects', 'decreases', 'increases') 
        and actions ('activity', 'expression', ...  ). A complete list of all allowed
        interaction_actions can be retrieved via the attribute :attr:`~.interaction_actions`.

        :param bool as_df: if set to True result returns as `pandas.DataFrame`
        :param str interaction_sentence: sentence describing the interactions 
        :param int organism_id: NCBI TaxTree identifier
        :param str chemical_name: chemical name
        :param str chemical_id: chemical identifier
        :param str cas_rn: CAS registry number
        :param str chemical_definition:
        :param str gene_symbol: gene symbol
        :param str gene_name: gene name
        :param int gene_id: NCBI Gene identifier
        :param str gene_form: gene form
        :param str interaction_action: combination of interaction and actions
        :param int limit: maximum number of results
        :return: list of :class:`pyctd.manager.database.models.ChemGeneIxn` objects


        .. seealso::

            :class:`pyctd.manager.models.ChemGeneIxn` 

            which is linked to:
            :class:`pyctd.manager.models.Chemical`
            :class:`pyctd.manager.models.Gene`
            :class:`pyctd.manager.models.ChemGeneIxnPubmed`

            Available interaction_actions and gene_forms
            :func:`pyctd.manager.database.Query.interaction_actions`
            :func:`pyctd.manager.database.Query.gene_forms`

        """
        q = self.session.query(models.ChemGeneIxn)

        if organism_id:
            q = q.filter(models.ChemGeneIxn.organism_id == organism_id)

        if interaction_sentence:
            q = q.filter(models.ChemGeneIxn.interaction == interaction_sentence)

        if gene_form:
            q = q.join(models.ChemGeneIxnGeneForm).filter(models.ChemGeneIxnGeneForm.gene_form == gene_form)

        if interaction_action:
            q = q.join(models.ChemGeneIxnInteractionAction) \
                .filter(models.ChemGeneIxnInteractionAction.interaction_action.like(interaction_action))

        q = self._join_gene(query=q, gene_name=gene_name, gene_symbol=gene_symbol, gene_id=gene_id)

        q = self._join_chemical(query=q, cas_rn=cas_rn, chemical_id=chemical_id, chemical_name=chemical_name,
                                chemical_definition=chemical_definition)

        return self._limit_and_df(q, limit, as_df)

    @property
    def gene_forms(self):
        """
        :return: List of strings for all available gene forms
        :rtype: list of :class:`str`
        """
        q = self.session.query(distinct(models.ChemGeneIxnGeneForm.gene_form))
        return [x[0] for x in q.all()]

    @property
    def interaction_actions(self):
        """
        :return: List of strings for allowed interaction/actions combinations
        :rtype: list
        """
        r = self.session.query(distinct(models.ChemGeneIxnInteractionAction.interaction_action)).all()
        return [x[0] for x in r]

    @property
    def actions(self):
        """
        :return: List of strings for allowed actions
        :rtype: list
        """
        r = self.session.query(models.Action).all()
        return [x.type_name for x in r]

    @property
    def pathways(self):
        """
        :return: List of strings for pathways
        """
        return self.session.query(models.Pathway).all()

    def get_gene_disease(self, direct_evidence=None, inference_chemical_name=None, inference_score=None,
                         gene_name=None, gene_symbol=None, gene_id=None, disease_name=None, disease_id=None,
                         disease_definition=None, limit=None, as_df=False):
        """
        Get gene–disease associations 

        :param bool as_df: if set to True result returns as `pandas.DataFrame`
        :param int gene_id: gene identifier
        :param str gene_symbol: gene symbol
        :param str gene_name:  gene name
        :param str direct_evidence: direct evidence
        :param str inference_chemical_name: inference_chemical_name 
        :param float inference_score: inference score
        :param str inference_chemical_name: chemical name
        :param disease_name: disease name
        :param disease_id: disease identifier 
        :param disease_definition: disease definition 
        :param int limit: maximum number of results
        :return: list of :class:`pyctd.manager.database.models.GeneDisease` objects

        .. seealso::
            
            :class:`pyctd.manager.models.GeneDisease`

            which is linked to:
            :class:`pyctd.manager.models.Chemical`
            :class:`pyctd.manager.models.Gene`
        """
        q = self.session.query(models.GeneDisease)
        if direct_evidence:
            q = q.filter(models.GeneDisease.direct_evidence == direct_evidence)
        if inference_chemical_name:
            q = q.filter(models.GeneDisease.inference_chemical_name == inference_chemical_name)
        if inference_score:
            q = q.filter(models.GeneDisease.inference_score == inference_score)

        q = self._join_disease(query=q, disease_definition=disease_definition, disease_id=disease_id,
                               disease_name=disease_name)

        q = self._join_gene(q, gene_name=gene_name, gene_symbol=gene_symbol, gene_id=gene_id)

        return self._limit_and_df(q, limit, as_df)

    @property
    def direct_evidences(self):
        """
        :return: All available direct evidences for gene disease correlations
        :rtype: list
        """
        q = self.session.query(distinct(models.GeneDisease.direct_evidence))
        return q.all()

    def get_disease_pathways(self, disease_id=None, disease_name=None, pathway_id=None, pathway_name=None,
                             disease_definition=None, limit=None, as_df=False):
        """Get disease pathway link
        
        :param bool as_df: if set to True result returns as `pandas.DataFrame`
        :param disease_id: 
        :param disease_name: 
        :param pathway_id: 
        :param pathway_name: 
        :param int limit: maximum number of results
        :return: list of :class:`pyctd.manager.database.models.DiseasePathway` objects

        .. seealso::
            
            :class:`pyctd.manager.models.DiseasePathway`

            which is linked to:
            :class:`pyctd.manager.models.Disease`
            :class:`pyctd.manager.models.Pathway`
        """
        q = self.session.query(models.DiseasePathway)

        q = self._join_disease(query=q, disease_id=disease_id, disease_name=disease_name,
                               disease_definition=disease_definition)

        q = self._join_pathway(query=q, pathway_id=pathway_id, pathway_name=pathway_name)

        return self._limit_and_df(q, limit, as_df)

    def get_chemical_diseases(self, direct_evidence=None, inference_gene_symbol=None, inference_score=None,
                              inference_score_operator=None, cas_rn=None, chemical_name=None,
                              chemical_id=None, chemical_definition=None, disease_definition=None,
                              disease_id=None, disease_name=None, limit=None, as_df=False):
        """Get chemical–disease associations with inference gene
        
        :param bool as_df: if set to True result returns as `pandas.DataFrame`
        :param chemical_id: 
        :param disease_id: 
        :param disease_definition: 
        :param direct_evidence: direct evidence
        :param inference_gene_symbol: inference gene symbol
        :param inference_score: inference score 
        :param inference_score_operator: inference score operator
        :param disease_name: disease name 
        :param chemical_name: chemical name 
        :param int limit: maximum number of results
        :return: list of :class:`pyctd.manager.database.models.ChemicalDisease` objects
        
        .. seealso::
            
            :class:`pyctd.manager.models.ChemicalDisease`

            which is linked to:
            :class:`pyctd.manager.models.Disease`
            :class:`pyctd.manager.models.Chemical`
        """
        q = self.session.query(models.ChemicalDisease)
        if direct_evidence:
            q = q.filter(models.ChemicalDisease.direct_evidence.like(direct_evidence))
        if inference_gene_symbol:
            q = q.filter(models.ChemicalDisease.inference_gene_symbol.like(inference_gene_symbol))
        if inference_score:
            if inference_score_operator == ">":
                q = q.filter_by(models.ChemicalDisease.inference_score > inference_score)
            elif inference_score_operator == "<":
                q = q.filter_by(models.ChemicalDisease.inference_score > inference_score)

        q = self._join_chemical(q, cas_rn=cas_rn, chemical_id=chemical_id, chemical_name=chemical_name,
                                chemical_definition=chemical_definition)

        q = self._join_disease(q, disease_definition=disease_definition, disease_id=disease_id,
                               disease_name=disease_name)

        return self._limit_and_df(q, limit, as_df)

    def get_gene_pathways(self, gene_name=None, gene_symbol=None, gene_id=None, pathway_id=None,
                          pathway_name=None, limit=None, as_df=False):
        """Get gene pathway link
        
        :param bool as_df: if set to True result returns as `pandas.DataFrame`
        :param str gene_name: gene name 
        :param str gene_symbol: gene symbol
        :param int gene_id: NCBI Gene identifier
        :param pathway_id: 
        :param str pathway_name: pathway name
        :param int limit: maximum number of results
        :return: list of :class:`pyctd.manager.database.models.GenePathway` objects

        .. seealso::
            
            :class:`pyctd.manager.models.GenePathway`

            which is linked to:
            :class:`pyctd.manager.models.Gene`
            :class:`pyctd.manager.models.Pathway`
        """
        q = self.session.query(models.GenePathway)
        q = self._join_gene(q, gene_name=gene_name, gene_symbol=gene_symbol, gene_id=gene_id)
        q = self._join_pathway(q, pathway_id=pathway_id, pathway_name=pathway_name)

        return self._limit_and_df(q, limit, as_df)

    def get_go_enriched__by__chemical_name(self, chemical_name, limit=None, as_df=False):
        q = self.session.query(models.ChemGoEnriched) \
            .join(models.Chemical) \
            .filter(models.Chemical.chemical_name == chemical_name) \
            .order_by(models.ChemGoEnriched.highest_go_level.desc(), models.ChemGoEnriched.corrected_p_value)
        return self._limit_and_df(q, limit, as_df)

    def get_pathway_enriched__by__chemical_name(self, chemical_name, limit=None, as_df=False):
        q = self.session.query(models.ChemPathwayEnriched) \
            .join(models.Chemical) \
            .filter(models.Chemical.chemical_name == chemical_name) \
            .order_by(models.ChemPathwayEnriched.corrected_p_value)
        return self._limit_and_df(q, limit, as_df)

    def get_therapeutic_chemical__by__disease_name(self, disease_name, limit=None, as_df=False):
        """
        Get therapeutic chemical by disease name
        
        :param bool as_df: if set to True result returns as `pandas.DataFrame`
        :param int limit: maximum number of results
        :param str disease_name: disease name
        :return: therapeutic chemical
        :rtpye: list[models.ChemicalDisease]
        """
        q = self.session.query(models.ChemicalDisease) \
            .join(models.Disease) \
            .filter(models.Disease.disease_name == disease_name,
                    models.ChemicalDisease.direct_evidence == 'therapeutic')
        return self._limit_and_df(q, limit, as_df)

    def get_marker_chemical__by__disease_name(self, disease_name, limit=None, as_df=False):
        q = self.session.query(models.ChemicalDisease) \
            .join(models.Disease) \
            .filter(models.Disease.disease_name == disease_name,
                    models.ChemicalDisease.direct_evidence == 'marker/mechanism')
        return self._limit_and_df(q, limit, as_df)

    def get_chemical__by__disease(self, disease_name, limit=None, as_df=False):
        q = self.session.query(models.ChemicalDisease) \
            .join(models.Disease) \
            .filter(models.Disease.disease_name == disease_name) \
            .order_by(models.ChemicalDisease.inference_score.desc())
        return self._limit_and_df(q, limit, as_df)

    def get_action(self, limit=None, as_df=False):
        q = self.session.query(models.Action)
        return self._limit_and_df(q, limit, as_df)

    def get_exposure_event(self):
        pass
