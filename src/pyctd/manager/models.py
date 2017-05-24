# -*- coding: utf-8 -*-
"""SQLAlchemy database models in this module describes all tables the database and 
fits the description in the table_conf module

.. image:: _static/models/all.png
    :target: _images/all.png
"""

from sqlalchemy import Column, ForeignKey, Integer, String, Text, REAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from .defaults import TABLE_PREFIX

Base = declarative_base()


def foreign_key_to(table_name):
    """Creates a standard foreign key to a table in the database
    
    :param table_name: name of the table without TABLE_PREFIX
    :type table_name: str
    :return: foreign key column 
    :rtype: sqlalchemy.Column
    """
    foreign_column = TABLE_PREFIX + table_name + '.id'
    return Column(Integer, ForeignKey(foreign_column))


class Pathway(Base):
    """Pathway vocabulary
    
    `CTD link <http://ctdbase.org/downloads/#allpathways>`_
    """
    table_suffix = "pathway"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    pathway_name = Column(String(255))
    pathway_id = Column(String(255))

    def __repr__(self):
        return self.pathway_name


class Action(Base):
    """Chemical–gene interaction types"""
    table_suffix = "action"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    type_name = Column(String(255))
    code = Column(String(255))
    description = Column(String(255))
    parent_code = Column(String(255))

    def __repr__(self):
        return self.type_name


class Chemical(Base):
    """Chemical vocabulary

    .. image:: _static/models/chemical.png
        :target: _images/chemical.png

    reference:
       - `CTD Help: Chemicals <http://ctdbase.org/help/chemDetailHelp.jsp>`_

    """
    table_suffix = "chemical"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    chemical_name = Column(String(255), index=True)
    chemical_id = Column(String(255), index=True)
    cas_rn = Column(String(255), index=True)
    definition = Column(Text)
    inchi = Column(Text)
    isomeric_smiles = Column(Text)

    parent_ids = relationship("ChemicalParentid", back_populates="chemical")
    tree_numbers = relationship("ChemicalTreenumber", back_populates="chemical")
    parent_tree_numbers = relationship("ChemicalParenttreenumber", back_populates="chemical")
    drugbank_ids = relationship("ChemicalDrugbank", back_populates="chemical")
    synonyms = relationship("ChemicalSynonym", back_populates="chemical")

    def __repr__(self):
        return self.chemical_name


class ChemicalParentid(Base):
    """Parent IDs of Chemical vocabulary"""
    table_suffix = "chemical__parent_id"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    chemical__id = foreign_key_to('chemical')
    parent_id = Column(String(255))

    chemical = relationship(Chemical, back_populates="parent_ids")

    def __repr__(self):
        return self.parent_id


class ChemicalTreenumber(Base):
    """Tree numbers of Chemical vocabulary"""
    table_suffix = "chemical__tree_number"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    chemical__id = foreign_key_to('chemical')
    tree_number = Column(String(255))

    chemical = relationship(Chemical, back_populates="tree_numbers")

    def __repr__(self):
        return self.tree_number


class ChemicalParenttreenumber(Base):
    """Parent tree numbers of Chemical vocabulary"""
    table_suffix = "chemical__parent_tree_number"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    chemical__id = foreign_key_to('chemical')
    parent_tree_number = Column(String(255))

    chemical = relationship(Chemical, back_populates="parent_tree_numbers")

    def __repr__(self):
        return self.parent_tree_number


class ChemicalDrugbank(Base):
    """DrugBank identifiers to Chemical vocabulary"""
    table_suffix = "chemical__drugbank_id"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    chemical__id = foreign_key_to('chemical')
    drugbank_id = Column(String(255))

    chemical = relationship(Chemical, back_populates="drugbank_ids")

    def __repr__(self):
        return self.drugbank_id


class ChemicalSynonym(Base):
    """Synonymy to Chemical vocabulary"""
    table_suffix = "chemical__synonym"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    chemical__id = foreign_key_to('chemical')
    synonym = Column(Text)

    chemical = relationship(Chemical, back_populates="synonyms")

    def __repr__(self):
        return self.synonym


class Disease(Base):
    """Disease vocabulary (MEDIC)

    .. image:: _static/models/disease.png
        :target: _images/disease.png

    reference:
        - `CTD Disease vocabulary (MEDIC); structure <http://ctdbase.org/downloads/#alldiseases>`_
        - `CTD description disease <http://ctdbase.org/help/diseaseDetailHelp.jsp>`_
    """
    table_suffix = "disease"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    disease_name = Column(String(255))  #: Disease name (str)
    disease_id = Column(String(255))  #: MeSH or OMIM identifier (str)
    definition = Column(Text)  #: definition of disease (str)
    parent_ids = Column(String(255))  # TODO: have to be normalized
    """identifiers of the parent terms; '|'-delimited list"""
    tree_numbers = Column(Text)  # TODO: have to be normalized
    """identifiers of the disease's nodes; '|'-delimited list"""
    parent_tree_numbers = Column(Text)  # TODO: have to be normalized
    """identifiers of the parent nodes; '|'-delimited list"""

    synonyms = relationship("DiseaseSynonym", back_populates="disease")
    alt_disease_ids = relationship("DiseaseAltdiseaseid", back_populates="disease")
    slim_mappings = relationship("DiseaseSlimmapping", back_populates="disease")

    def __repr__(self):
        return self.disease_name


class DiseaseSynonym(Base):
    """Synonyms to Disease vocabulary (MEDIC)

    reference:
        - `CTD Disease synonym <http://ctdbase.org/downloads/#alldiseases>`_
    """
    table_suffix = "disease__synonym"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    disease__id = foreign_key_to('disease')
    synonym = Column(String(255))

    disease = relationship(Disease, back_populates="synonyms")

    def __repr__(self):
        return self.synonym


class DiseaseAltdiseaseid(Base):
    """Alternative disease identifiers to Disease vocabulary (MEDIC)

    reference:
        - `CTD Disease (alternative identifier) <http://ctdbase.org/downloads/#alldiseases>`_
    """
    table_suffix = "disease__alt_disease_id"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    disease__id = foreign_key_to('disease')
    alt_disease_id = Column(String(255))

    disease = relationship(Disease, back_populates="alt_disease_ids")

    def __repr__(self):
        return self.alt_disease_id


class DiseaseSlimmapping(Base):
    """MEDIC-Slim mappings to Disease vocabulary (MEDIC)

    reference:
        - `CTD MEDIC-Slim mappings <http://ctdbase.org/downloads/#alldiseases>`_
    """
    table_suffix = "disease__slim_mapping"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    disease__id = foreign_key_to('disease')
    slim_mapping = Column(String(255))

    disease = relationship(Disease, back_populates="slim_mappings")

    def __repr__(self):
        return self.slim_mapping


class Gene(Base):
    """Gene vocabulary

    .. image:: _static/models/gene.png
        :target: _images/gene.png

    reference:
        - `CTD Gene <http://ctdbase.org/downloads/#allgenes>`_
        - `CTD Help: Genes <http://ctdbase.org/help/geneDetailHelp.jsp>`_
        - `UniProt accession numbers <http://www.uniprot.org/help/accession_numbers>`_
    """
    table_suffix = "gene"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    gene_symbol = Column(String(255), index=True)  #: gene_symbol"""
    gene_name = Column(Text)  #: gene name
    gene_id = Column(Integer)  #: NCBI Gene identifier

    alt_gene_ids = relationship("GeneAltGeneId", back_populates="gene")  #: list of alternative NCBI Gene identifiers
    pharmgkb_ids = relationship("GenePharmgkb", back_populates="gene")  #: list of PharmGKB identifiers
    uniprot_ids = relationship("GeneUniprot", back_populates="gene")
    """`UniProt accession number <http://www.uniprot.org/help/accession_numbers>`_"""
    biogrid_ids = relationship("GeneBiogrid", back_populates="gene")  #: list of BioGRID identifier
    synonyms = relationship("GeneSynonym", back_populates="gene")  #: list of synonyms

    def __repr__(self):
        return self.gene_name


class GeneAltGeneId(Base):
    """Alternative gene identifiers to Gene vocabulary

    reference:
        - `CTD alternative NCBI Gene identifiers <http://ctdbase.org/downloads/#allgenes>`_
    """
    table_suffix = "gene__alt_gene_id"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    gene__id = foreign_key_to('gene')
    alt_gene_id = Column(Integer)

    gene = relationship(Gene, back_populates="alt_gene_ids")

    def __repr__(self):
        return str(self.alt_gene_id)


class GenePharmgkb(Base):
    """PharmGKB mapping to Gene vocabulary

    reference:
        - `CTD PharmGKBIDs <http://ctdbase.org/downloads/#allgenes>`_
        - `PharmGKB <https://www.pharmgkb.org/>`_
    """
    table_suffix = "gene__pharmgkb_id"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    gene__id = foreign_key_to('gene')
    pharmgkb_id = Column(String(255))

    gene = relationship(Gene, back_populates="pharmgkb_ids")

    def __repr__(self):
        return self.pharmgkb_id


class GeneUniprot(Base):
    """UniProt mappings to Gene vocabulary

    reference:
        - `CTD UniProt <http://ctdbase.org/downloads/#allgenes>`_
        - `UniProt <http://www.uniprot.org/>`_
    """
    table_suffix = "gene__uniprot_id"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    gene__id = foreign_key_to('gene')
    uniprot_id = Column(String(255))

    gene = relationship(Gene, back_populates="uniprot_ids")

    def __repr__(self):
        return self.uniprot_id


class GeneBiogrid(Base):
    """BioGRID mappings to Gene vocabulary

    reference:
        - `CTD BioGRID <http://ctdbase.org/downloads/#allgenes>`_
        - `BioGRID <https://thebiogrid.org/>`_
    """
    table_suffix = "gene__biogrid_id"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    gene__id = foreign_key_to('gene')
    biogrid_id = Column(Integer)

    gene = relationship(Gene, back_populates="biogrid_ids")

    def __repr__(self):
        return str(self.biogrid_id)


class GeneSynonym(Base):
    """Synonyms to Gene vocabulary

    reference:
        - `CTD Synonyms <http://ctdbase.org/downloads/#allgenes>`_
    """
    table_suffix = "gene__synonym"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    gene__id = foreign_key_to('gene')
    synonym = Column(Text)

    gene = relationship(Gene, back_populates="synonyms")

    def __repr__(self):
        return self.synonym


class ChemicalDisease(Base):
    """Chemical–disease associations

    .. image:: _static/models/chemicalDisease.png
        :target: _images/chemicalDisease.png

    reference:
        - `CTD Chemical–disease associations <http://ctdbase.org/downloads/#cd>`_
    """
    table_suffix = "chemical__disease"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    direct_evidence = Column(String(255), index=True)
    inference_gene_symbol = Column(String(255))
    inference_score = Column(REAL)
    chemical__id = foreign_key_to('chemical')
    disease__id = foreign_key_to('disease')

    chemical = relationship('Chemical')
    disease = relationship('Disease')

    omim_ids = relationship('ChemicalDiseaseOmim')
    pubmed_ids = relationship('ChemicalDiseasePubmedid')

    def __repr__(self):
        return '{} : {} [gene: {}, score: {}]'.format(
            self.chemical,
            self.disease,
            self.inference_gene_symbol,
            self.inference_score
        )


class ChemicalDiseaseOmim(Base):
    """Online Mendelian Inheritance in Man (OMIM) mappings to Chemical–disease associations

    reference:
        - `CTD OMIM <http://ctdbase.org/downloads/#cd>`_
    """
    table_suffix = "chemical__disease__omim_id"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    chemical__disease__id = foreign_key_to('chemical__disease')
    omim_id = Column(Integer)


class ChemicalDiseasePubmedid(Base):
    """PubMed Literature references to Chemical–disease associations

    reference:
        - `CTD PubMed <http://ctdbase.org/downloads/#cd>`_
    """
    table_suffix = "chemical__disease__pubmed_id"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    chemical__disease__id = foreign_key_to('chemical__disease')
    pubmed_id = Column(Integer)


class ChemPathwayEnriched(Base):
    """Chemical–pathway enriched associations

    reference:
        - `CTD Chemical–pathway enriched associations <http://ctdbase.org/downloads/#chempathwaysenriched>`_
    """
    table_suffix = "chem__pathway_enriched"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    p_value = Column(REAL)
    corrected_p_value = Column(REAL)
    target_match_qty = Column(Integer)
    target_total_qty = Column(Integer)
    background_match_qty = Column(Integer)
    background_total_qty = Column(Integer)
    chemical__id = foreign_key_to('chemical')
    pathway__id = foreign_key_to('pathway')

    chemical = relationship('Chemical')
    pathway = relationship('Pathway')

    def __repr__(self):
        return 'chemical: {}; pathway: {}; corrected p-value: {}'.format(
            self.chemical,
            self.pathway,
            self.corrected_p_value
        )


class ChemGeneIxn(Base):
    """Chemical–gene interactions

    .. image:: _static/models/chemGeneIxn.png
        :target: _images/chemGeneIxn.png

    reference:
        - `CTD Chemical–gene interactions <http://ctdbase.org/downloads/#cg>`_
    """
    table_suffix = "chem_gene_ixn"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    organism_id = Column(Integer, index=True)
    interaction = Column(Text)
    chemical__id = foreign_key_to('chemical')
    gene__id = foreign_key_to('gene')

    chemical = relationship('Chemical')
    gene = relationship('Gene')

    gene_forms = relationship('ChemGeneIxnGeneForm')
    interaction_actions = relationship('ChemGeneIxnInteractionAction')
    pubmed_ids = relationship('ChemGeneIxnPubmed')

    def __repr__(self):
        return '{} -> {}; interaction: {}'.format(
            self.chemical,
            self.gene,
            self.interaction
        )


class ChemGeneIxnGeneForm(Base):
    """Gene forms of Chemical–gene interactions

    reference:
        - `CTD Gene forms of Chemical–gene interactions <http://ctdbase.org/downloads/#cg>`_
    """
    table_suffix = "chem_gene_ixn__gene_form"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    chem_gene_ixn__id = foreign_key_to('chem_gene_ixn')
    gene_form = Column(String(255), index=True)

    def __repr__(self):
        return self.gene_form


class ChemGeneIxnInteractionAction(Base):
    """Chemical–gene interactions actions

    reference:
        - `CTD Chemical–gene interactions actions <http://ctdbase.org/downloads/#cg>`_
    """
    table_suffix = "chem_gene_ixn__interaction_action"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    chem_gene_ixn__id = foreign_key_to('chem_gene_ixn')
    interaction_action = Column(String(255), index=True)

    def __repr__(self):
        return self.interaction_action


class ChemGeneIxnPubmed(Base):
    """Chemical–gene interactions PubMed links

    reference.
        - `CTD Chemical–gene interactions PubMed links <http://ctdbase.org/downloads/#cg>`_
    """
    table_suffix = "chem_gene_ixn__pubmed_id"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    chem_gene_ixn__id = foreign_key_to('chem_gene_ixn')
    pubmed_id = Column(Integer)

    def __repr__(self):
        return str(self.pubmed_id)


class ChemGoEnriched(Base):
    """Chemical–GO enriched associations

    reference:
        - `CTD Chemical–GO enriched associations <http://ctdbase.org/downloads/#chemgoenriched>`_
    """
    table_suffix = "chem__go_enriched"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    ontology = Column(String(255))
    go_term_name = Column(String(255))
    go_term_id = Column(String(255))
    highest_go_level = Column(Integer)
    p_value = Column(REAL)
    corrected_p_value = Column(REAL)
    target_match_qty = Column(Integer)
    target_total_qty = Column(Integer)
    background_match_qty = Column(Integer)
    background_total_qty = Column(Integer)
    chemical__id = foreign_key_to('chemical')

    chemical = relationship('Chemical')

    def __repr__(self):
        return '{} [corrected p-value:{}, highest GO level:{}]'.format(
            self.go_term_name,
            self.corrected_p_value,
            self.highest_go_level
        )


class DiseasePathway(Base):
    """Disease–pathway associations

    .. image:: _static/models/diseasePathway.png
        :target: _images/diseasePathway.png

    reference:
        - `CTD Disease–pathway associations <http://ctdbase.org/downloads/#diseasepathways>`_
    """
    table_suffix = "disease__pathway"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    pathway__id = foreign_key_to('pathway')
    disease__id = foreign_key_to('disease')
    inference_gene_symbol = Column(String(255))

    pathway = relationship('Pathway')
    disease = relationship('Disease')

    def __repr__(self):
        return 'pathway:{}; disease:{}; interference gene:{}'.format(
            self.pathway,
            self.disease,
            self.inference_gene_symbol
        )


class ExposureEvent(Base):
    """Exposure–event associations

    reference:
        - `CTD Exposure–event associations <http://ctdbase.org/downloads/#exposureevents>`_
    """
    table_suffix = "exposure_event"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    stressor_source_category = Column(String(255))
    stressor_source_details = Column(String(255))
    number_of_stressor_samples = Column(Integer)
    stress_or_notes = Column(String(255))
    number_of_receptors = Column(Integer)
    receptors = Column(String(255))
    receptor_notes = Column(String(255))
    smoking_status = Column(String(255))
    age = Column(String(255))
    age_units_of_measurement = Column(String(255))
    age_qualifier = Column(String(255))
    sex = Column(String(255))
    race = Column(String(255))
    methods = Column(String(255))
    detection_limit = Column(Text)
    detection_limit_uom = Column(String(255))
    detection_frequency = Column(String(255))
    medium = Column(String(255))
    exposure_marker = Column(String(255))
    exposure_marker_id = Column(String(255))
    marker_level = Column(String(255))
    marker_units_of_measurement = Column(String(255))
    marker_measurement_statistic = Column(String(255))
    assay_notes = Column(Text)
    study_countries = Column(Text)
    state_or_province = Column(Text)
    city_town_region_area = Column(String(255))
    exposure_event_notes = Column(String(255))
    outcome_relationship = Column(String(255))
    phenotype_name = Column(Text)
    phenotype_id = Column(String(255))
    phenotype_action_degree_type = Column(String(255))
    anatomy = Column(String(255))
    exposure_outcome_notes = Column(Text)
    reference = Column(Integer)
    associated_study_titles = Column(Text)
    enrollment_start_year = Column(Integer)
    enrollment_end_year = Column(Integer)
    study_factors = Column(String(255))

    disease__id = foreign_key_to('disease')
    chemical__id = foreign_key_to('chemical')

    chemical = relationship('Chemical')
    disease = relationship('Disease')


class GeneDisease(Base):
    """Gene–disease associations

    .. image:: _static/models/geneDisease.png
        :target: _images/geneDisease.png

    reference:
        - `CTD Gene–disease associations <http://ctdbase.org/downloads/#gd>`_
    """
    table_suffix = "gene__disease"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    direct_evidence = Column(String(255))
    inference_chemical_name = Column(String(255))
    inference_score = Column(REAL)
    gene__id = foreign_key_to('gene')
    disease__id = foreign_key_to('disease')

    gene = relationship('Gene')
    disease = relationship('Disease')

    omim_ids = relationship('GeneDiseaseOmim')
    pubmed_ids = relationship('GeneDiseasePubmed')

    def __repr__(self):
        return 'gene:{}; disease:{}; chemical:{}; evidence:{}'.format(
            self.gene,
            self.disease,
            self.inference_chemical_name,
            self.direct_evidence
        )


class GeneDiseaseOmim(Base):
    """Online Mendelian Inheritance in Man (OMIM) mappings to Gene–disease associations

    reference:
        - `CTD OMIM mappings to Gene–disease associations <http://ctdbase.org/downloads/#gd>`_
    """
    table_suffix = "gene__disease__omim_id"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    gene__disease__id = foreign_key_to('gene__disease')
    omim_id = Column(Integer)


class GeneDiseasePubmed(Base):
    """PubMed references to Gene–disease associations

    reference:
        - `CTD PubMed references to Gene–disease associations <http://ctdbase.org/downloads/#gd>`_
    """
    table_suffix = "gene__disease__pubmed_id"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    gene__disease__id = foreign_key_to('gene__disease')
    pubmed_id = Column(Integer)

    def __repr__(self):
        return self.pubmed_id


class GenePathway(Base):
    """Gene–pathway associations

    reference:
        - `CTD Gene–pathway associations <http://ctdbase.org/downloads/#genepathways>`_
    """
    table_suffix = "gene__pathway"
    __tablename__ = TABLE_PREFIX + table_suffix
    id = Column(Integer, primary_key=True)

    pathway__id = foreign_key_to('pathway')
    gene__id = foreign_key_to('gene')

    pathway = relationship('Pathway')
    gene = relationship('Gene')

    def __repr__(self):
        return 'gene:{}; pathway:{}'.format(self.gene, self.pathway)
