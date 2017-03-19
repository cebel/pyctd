# -*- coding: utf-8 -*-
"""SQLAlchemy database models in this module describes all tables the database and 
fits the description in the table_conf module"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, Text, REAL
from sqlalchemy.ext.declarative import declarative_base
from .defaults import TABLE_PREFIX
from sqlalchemy.orm import relationship

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
    __tablename__ = TABLE_PREFIX + "pathway"
    id = Column(Integer, primary_key=True)

    pathway_name = Column(String(255))
    pathway_id = Column(String(255))

    def __repr__(self):
        return self.pathway_name


class Action(Base):
    """Chemical–gene interaction types"""
    __tablename__ = TABLE_PREFIX + "action"
    id = Column(Integer, primary_key=True)

    type_name = Column(String(255))
    code = Column(String(255))
    description = Column(String(255))
    parent_code = Column(String(255))

    def __repr__(self):
        return self.type_name


class Chemical(Base):
    """Chemical vocabulary"""
    __tablename__ = TABLE_PREFIX + "chemical"
    id = Column(Integer, primary_key=True)

    chemical_name = Column(String(255), index=True)
    chemical_id = Column(String(255))
    cas_rn = Column(String(255))
    definition = Column(Text)

    parent_ids = relationship("ChemicalParentid", back_populates="chemical")
    tree_numbers = relationship("ChemicalTreenumber", back_populates="chemical")
    parent_tree_numbers = relationship("ChemicalParenttreenumber", back_populates="chemical")
    drugbank_ids = relationship("ChemicalDrugbank", back_populates="chemical")
    synonyms = relationship("ChemicalSynonym", back_populates="chemical")

    def __repr__(self):
        return self.chemical_name


class ChemicalParentid(Base):
    """Parent IDs of Chemical vocabulary"""
    __tablename__ = TABLE_PREFIX + "chemical__parent_id"
    id = Column(Integer, primary_key=True)

    chemical__id = foreign_key_to('chemical')
    parent_id = Column(String(255))

    chemical = relationship(Chemical, back_populates="parent_ids")

    def __repr__(self):
        return self.parent_id


class ChemicalTreenumber(Base):
    """Tree numbers of Chemical vocabulary"""
    __tablename__ = TABLE_PREFIX + "chemical__tree_number"
    id = Column(Integer, primary_key=True)

    chemical__id = foreign_key_to('chemical')
    tree_number = Column(String(255))

    chemical = relationship(Chemical, back_populates="tree_numbers")

    def __repr__(self):
        return self.tree_number


class ChemicalParenttreenumber(Base):
    """Parent tree numbers of Chemical vocabulary"""
    __tablename__ = TABLE_PREFIX + "chemical__parent_tree_number"
    id = Column(Integer, primary_key=True)

    chemical__id = foreign_key_to('chemical')
    parent_tree_number = Column(String(255))

    chemical = relationship(Chemical, back_populates="parent_tree_numbers")

    def __repr__(self):
        return self.parent_tree_number


class ChemicalDrugbank(Base):
    """DrugBank identifiers to Chemical vocabulary"""
    __tablename__ = TABLE_PREFIX + "chemical__drugbank_id"
    id = Column(Integer, primary_key=True)

    chemical__id = foreign_key_to('chemical')
    drugbank_id = Column(String(255))

    chemical = relationship(Chemical, back_populates="drugbank_ids")

    def __repr__(self):
        return self.drugbank_id


class ChemicalSynonym(Base):
    """Synonymy to Chemical vocabulary"""
    __tablename__ = TABLE_PREFIX + "chemical__synonym"
    id = Column(Integer, primary_key=True)

    chemical__id = foreign_key_to('chemical')
    synonym = Column(Text)

    chemical = relationship(Chemical, back_populates="synonyms")

    def __repr__(self):
        return self.synonym


class Disease(Base):
    """Disease vocabulary (MEDIC)
    
    reference:
        - `CTD structure <http://ctdbase.org/downloads/#alldiseases>`_
        - `CTD description <http://ctdbase.org/help/diseaseDetailHelp.jsp>`_
    """
    __tablename__ = TABLE_PREFIX + "disease"
    id = Column(Integer, primary_key=True)

    disease_name = Column(String(255))
    disease_id = Column(String(255))
    definition = Column(Text)
    parent_ids = Column(String(255))
    tree_numbers = Column(Text)
    parent_tree_numbers = Column(Text)

    synonyms = relationship("DiseaseSynonym", back_populates="disease")
    alt_disease_ids = relationship("DiseaseAltdiseaseid", back_populates="disease")
    slim_mappings = relationship("DiseaseSlimmapping", back_populates="disease")

    def __repr__(self):
        return self.disease_name


class DiseaseSynonym(Base):
    """Synonyms to Disease vocabulary (MEDIC)
    
    reference:
        - `CTD <http://ctdbase.org/help/diseaseDetailHelp.jsp>`_
    """
    __tablename__ = TABLE_PREFIX + "disease__synonym"
    id = Column(Integer, primary_key=True)

    disease__id = foreign_key_to('disease')
    synonym = Column(String(255))

    disease = relationship(Disease, back_populates="synonyms")

    def __repr__(self):
        return self.synonym


class DiseaseAltdiseaseid(Base):
    """Alternative disease identifiers to Disease vocabulary (MEDIC)
    
    reference:
        - `CTD <http://ctdbase.org/help/diseaseDetailHelp.jsp>`_
    """
    __tablename__ = TABLE_PREFIX + "disease__alt_disease_id"
    id = Column(Integer, primary_key=True)

    disease__id = foreign_key_to('disease')
    alt_disease_id = Column(String(255))

    disease = relationship(Disease, back_populates="alt_disease_ids")

    def __repr__(self):
        return self.alt_disease_id


class DiseaseSlimmapping(Base):
    """MEDIC-Slim mappings to Disease vocabulary (MEDIC)
    
    reference:
        - `CTD <http://ctdbase.org/help/diseaseDetailHelp.jsp>`_
    """
    __tablename__ = TABLE_PREFIX + "disease__slim_mapping"
    id = Column(Integer, primary_key=True)

    disease__id = foreign_key_to('disease')
    slim_mapping = Column(String(255))

    disease = relationship(Disease, back_populates="slim_mappings")

    def __repr__(self):
        return self.slim_mapping


class Gene(Base):
    """Gene vocabulary

    reference:
        - `CTD <http://ctdbase.org/downloads/#allgenes>`_    
    """
    __tablename__ = TABLE_PREFIX + "gene"
    id = Column(Integer, primary_key=True)

    gene_symbol = Column(String(255), index=True)
    gene_name = Column(Text)
    gene_id = Column(Integer)

    alt_gene_ids = relationship("GeneAltGeneId", back_populates="gene")
    pharmgkb_ids = relationship("GenePharmgkb", back_populates="gene")
    uniprot_ids = relationship("GeneUniprot", back_populates="gene")
    biogrid_ids = relationship("GeneBiogrid", back_populates="gene")
    synonyms = relationship("GeneSynonym", back_populates="gene")

    def __repr__(self):
        return self.gene_name


class GeneAltGeneId(Base):
    """Alternative gene identifiers to Gene vocabulary
    
    reference:
        - `CTD <http://ctdbase.org/downloads/#allgenes>`_
    """
    __tablename__ = TABLE_PREFIX + "gene__alt_gene_id"
    id = Column(Integer, primary_key=True)

    gene__id = foreign_key_to('gene')
    alt_gene_id = Column(Integer)

    gene = relationship(Gene, back_populates="alt_gene_ids")

    def __repr__(self):
        return self.alt_gene_id


class GenePharmgkb(Base):
    """PharmGKB mapping to Gene vocabulary

    reference:
        - `CTD <http://ctdbase.org/downloads/#allgenes>`_
        - `PharmGKB <https://www.pharmgkb.org/>`_
    """
    __tablename__ = TABLE_PREFIX + "gene__pharmgkb_id"
    id = Column(Integer, primary_key=True)

    gene__id = foreign_key_to('gene')
    pharmgkb_id = Column(String(255))

    gene = relationship(Gene, back_populates="pharmgkb_ids")

    def __repr__(self):
        return self.pharmgkb_id


class GeneUniprot(Base):
    """UniProt mappings to Gene vocabulary

    reference:
        - `CTD <http://ctdbase.org/downloads/#allgenes>`_
        - `UniProt <http://www.uniprot.org/>`_    
    """
    __tablename__ = TABLE_PREFIX + "gene__uniprot_id"
    id = Column(Integer, primary_key=True)

    gene__id = foreign_key_to('gene')
    uniprot_id = Column(String(255))

    gene = relationship(Gene, back_populates="uniprot_ids")

    def __repr__(self):
        return self.uniprot_id


class GeneBiogrid(Base):
    """BioGRID mappings to Gene vocabulary
    
    reference:
        - `CTD <http://ctdbase.org/downloads/#allgenes>`_
        - `BioGRID <https://thebiogrid.org/>`_
    """
    __tablename__ = TABLE_PREFIX + "gene__biogrid_id"
    id = Column(Integer, primary_key=True)

    gene__id = foreign_key_to('gene')
    biogrid_id = Column(Integer)

    gene = relationship(Gene, back_populates="biogrid_ids")

    def __repr__(self):
        return self.biogrid_id


class GeneSynonym(Base):
    """Synonyms to Gene vocabulary
    
    reference:
        - `CTD <http://ctdbase.org/downloads/#allgenes>`_
    """
    __tablename__ = TABLE_PREFIX + "gene__synonym"
    id = Column(Integer, primary_key=True)

    gene__id = foreign_key_to('gene')
    synonym = Column(Text)

    gene = relationship(Gene, back_populates="synonyms")

    def __repr__(self):
        return self.synonym


class ChemicalDisease(Base):
    """Chemical–disease associations
    
    reference:
        - `CTD <http://ctdbase.org/downloads/#cd>`_ 
    """
    __tablename__ = TABLE_PREFIX + "chemical__disease"
    id = Column(Integer, primary_key=True)

    direct_evidence = Column(String(255))
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
        - `CTD <http://ctdbase.org/downloads/#cd>`_
    """
    __tablename__ = TABLE_PREFIX + "chemical__disease__omim_id"
    id = Column(Integer, primary_key=True)

    chemical__disease__id = foreign_key_to('chemical__disease')
    omim_id = Column(Integer)


class ChemicalDiseasePubmedid(Base):
    """PubMed Literature references to Chemical–disease associations
    
    reference:
        - `CTD <http://ctdbase.org/downloads/#cd>`_
    """
    __tablename__ = TABLE_PREFIX + "chemical__disease__pubmed_id"
    id = Column(Integer, primary_key=True)

    chemical__disease__id = foreign_key_to('chemical__disease')
    pubmed_id = Column(Integer)


class ChemPathwayEnriched(Base):
    """Chemical–pathway enriched associations
    
    reference:
        - `CTD <http://ctdbase.org/downloads/#chempathwaysenriched>`_
    """
    __tablename__ = TABLE_PREFIX + "chem__pathway_enriched"
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
    
    reference:
        - `CTD <http://ctdbase.org/downloads/#cg>`_
    """

    __tablename__ = TABLE_PREFIX + "chem_gene_ixn"
    id = Column(Integer, primary_key=True)

    organism_id = Column(Integer)
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
        - `CTD <http://ctdbase.org/downloads/#cg>`_
    """

    __tablename__ = TABLE_PREFIX + "chem_gene_ixn__gene_form"
    id = Column(Integer, primary_key=True)

    chem_gene_ixn__id = foreign_key_to('chem_gene_ixn')
    gene_form = Column(String(255))

    def __repr__(self):
        return self.gene_form


class ChemGeneIxnInteractionAction(Base):
    """Chemical–gene interactions actions
    
    reference:
        - `CTD <http://ctdbase.org/downloads/#cg>`_
    """

    __tablename__ = TABLE_PREFIX + "chem_gene_ixn__interaction_action"
    id = Column(Integer, primary_key=True)

    chem_gene_ixn__id = foreign_key_to('chem_gene_ixn')
    interaction_action = Column(String(255), index=True)

    def __repr__(self):
        return self.interaction_action


class ChemGeneIxnPubmed(Base):
    """Chemical–gene interactions PubMed links
    
    reference.
        - `CTD <http://ctdbase.org/downloads/#cg>`_
    """

    __tablename__ = TABLE_PREFIX + "chem_gene_ixn__pubmed_id"
    id = Column(Integer, primary_key=True)

    chem_gene_ixn__id = foreign_key_to('chem_gene_ixn')
    pubmed_id = Column(Integer)

    def __repr__(self):
        return str(self.pubmed_id)


class ChemGoEnriched(Base):
    """Chemical–GO enriched associations
    
    reference:
        - `CTD <http://ctdbase.org/downloads/#chemgoenriched>`_
    """

    __tablename__ = TABLE_PREFIX + "chem__go_enriched"
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
    
    reference:
        - `CTD <http://ctdbase.org/downloads/#diseasepathways>`_
    """
    __tablename__ = TABLE_PREFIX + "disease__pathway"
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
        - `CTD <http://ctdbase.org/downloads/#exposureevents>`_
    """
    __tablename__ = TABLE_PREFIX + "exposure_event"
    id = Column(Integer, primary_key=True)

    stressor_agent_name = Column(String(255))
    chemical__id = foreign_key_to('chemical')  # == stressor_agent_id
    number_of_receptors = Column(Integer)
    receptor_description = Column(String(255))
    receptor_notes = Column(String(255))
    study_location = Column(String(255))
    assay_mediums = Column(String(255))
    assayed_term_name = Column(String(255))
    assayed_term_id = Column(String(255))
    assay_level = Column(String(255))
    assay_units_of_measurement = Column(String(255))
    assay_measurement_statistic = Column(String(255))
    assay_notes = Column(Text)
    outcome_relationship = Column(String(255))
    disease__id = foreign_key_to('disease')
    phenotype_name = Column(String(255))
    phenotype_id = Column(String(255))
    reference = Column(Integer)

    chemical = relationship('Chemical')
    disease = relationship('Disease')


class GeneDisease(Base):
    """Gene–disease associations
    
    reference:
        - `CTD <http://ctdbase.org/downloads/#gd>`_
    """
    __tablename__ = TABLE_PREFIX + "gene__disease"
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
        - `CTD <http://ctdbase.org/downloads/#gd>`_
    """
    __tablename__ = TABLE_PREFIX + "gene__disease__omim_id"
    id = Column(Integer, primary_key=True)

    gene__disease__id = foreign_key_to('gene__disease')
    omim_id = Column(Integer)


class GeneDiseasePubmed(Base):
    """PubMed references to Gene–disease associations
    
    reference:
        - `CTD <http://ctdbase.org/downloads/#gd>`_
    """
    __tablename__ = TABLE_PREFIX + "gene__disease__pubmed_id"
    id = Column(Integer, primary_key=True)

    gene__disease__id = foreign_key_to('gene__disease')
    pubmed_id = Column(Integer)

    def __repr__(self):
        return self.pubmed_id


class GenePathway(Base):
    """Gene–pathway associations
    
    reference:
        - `CTD <http://ctdbase.org/downloads/#genepathways`_
    """
    __tablename__ = TABLE_PREFIX + "gene__pathway"
    id = Column(Integer, primary_key=True)

    pathway__id = foreign_key_to('pathway')
    gene__id = foreign_key_to('gene')

    pathway = relationship('Pathway')
    gene = relationship('Gene')

    def __repr__(self):
        return 'gene:{}; pathway:{}'.format(self.pathway, self.gene)
