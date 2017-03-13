# -*- coding: utf-8 -*-
"""SQLAlchemy database models in this module describes all tables the database and 
fits the description in the table_conf module"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, Text, REAL
from sqlalchemy.ext.declarative import declarative_base
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
    __tablename__ = TABLE_PREFIX + "pathway"
    id = Column(Integer, primary_key=True)

    pathway_name = Column(String(255))
    pathway_id = Column(String(255))

    def __repr__(self):
        return self.pathway_name


class Action(Base):
    __tablename__ = TABLE_PREFIX + "action"
    id = Column(Integer, primary_key=True)

    type_name = Column(String(255))
    code = Column(String(255))
    description = Column(String(255))
    parent_code = Column(String(255))

    def __repr__(self):
        return self.type_name


class Chemical(Base):
    __tablename__ = TABLE_PREFIX + "chemical"
    id = Column(Integer, primary_key=True)

    chemical_name = Column(String(255))
    chemical_id = Column(String(255))
    cas_rn = Column(String(255))
    definition = Column(Text)

    def __repr__(self):
        return self.chemical_name


class ChemicalParentid(Base):
    __tablename__ = TABLE_PREFIX + "chemical__parent_id"
    id = Column(Integer, primary_key=True)

    chemical__id = foreign_key_to('chemical')
    parent_id = Column(String(255))


class ChemicalTreenumber(Base):
    __tablename__ = TABLE_PREFIX + "chemical__tree_number"
    id = Column(Integer, primary_key=True)

    chemical__id = foreign_key_to('chemical')
    tree_number = Column(String(255))


class ChemicalParenttreenumber(Base):
    __tablename__ = TABLE_PREFIX + "chemical__parent_tree_number"
    id = Column(Integer, primary_key=True)

    chemical__id = foreign_key_to('chemical')
    parent_tree_number = Column(String(255))


class ChemicalDrugbank(Base):
    __tablename__ = TABLE_PREFIX + "chemical__drugbank_id"
    id = Column(Integer, primary_key=True)

    chemical__id = foreign_key_to('chemical')
    drugbank_id = Column(String(255))


class ChemicalSynonym(Base):
    __tablename__ = TABLE_PREFIX + "chemical__synonym"
    id = Column(Integer, primary_key=True)

    chemical__id = foreign_key_to('chemical')
    synonym = Column(Text)


class Disease(Base):
    __tablename__ = TABLE_PREFIX + "disease"
    id = Column(Integer, primary_key=True)

    disease_name = Column(String(255))
    disease_id = Column(String(255))
    definition = Column(Text)
    parent_ids = Column(String(255))
    tree_numbers = Column(Text)
    parent_tree_numbers = Column(Text)

    def __repr__(self):
        return self.disease_name


class DiseaseSynonym(Base):
    __tablename__ = TABLE_PREFIX + "disease__synonym"
    id = Column(Integer, primary_key=True)

    disease__id = foreign_key_to('disease')
    synonym = Column(String(255))


class DiseaseAltdiseaseid(Base):
    __tablename__ = TABLE_PREFIX + "disease__alt_disease_id"
    id = Column(Integer, primary_key=True)

    disease__id = foreign_key_to('disease')
    alt_disease_id = Column(String(255))


class DiseaseSlimmapping(Base):
    __tablename__ = TABLE_PREFIX + "disease__slim_mapping"
    id = Column(Integer, primary_key=True)

    disease__id = foreign_key_to('disease')
    slim_mapping = Column(String(255))


class Gene(Base):
    __tablename__ = TABLE_PREFIX + "gene"
    id = Column(Integer, primary_key=True)

    gene_symbol = Column(String(255))
    gene_name = Column(Text)
    gene_id = Column(Integer)

    def __repr__(self):
        return self.gene_name


class GeneAltGeneId(Base):
    __tablename__ = TABLE_PREFIX + "gene__alt_gene_id"
    id = Column(Integer, primary_key=True)

    gene__id = foreign_key_to('gene')
    alt_gene_id = Column(Integer)


class GenePharmgkb(Base):
    __tablename__ = TABLE_PREFIX + "gene__pharmgkb_id"
    id = Column(Integer, primary_key=True)

    gene__id = foreign_key_to('gene')
    pharmgkb_id = Column(String(255))


class GeneUniprot(Base):
    __tablename__ = TABLE_PREFIX + "gene__uniprot_id"
    id = Column(Integer, primary_key=True)

    gene__id = foreign_key_to('gene')
    uniprot_id = Column(String(255))


class GeneBiogrid(Base):
    __tablename__ = TABLE_PREFIX + "gene__biogrid_id"
    id = Column(Integer, primary_key=True)

    gene__id = foreign_key_to('gene')
    biogrid_id = Column(Integer)


class GeneSynonym(Base):
    __tablename__ = TABLE_PREFIX + "gene__synonym"
    id = Column(Integer, primary_key=True)

    gene__id = foreign_key_to('gene')
    synonym = Column(Text)


class ChemicalDisease(Base):
    __tablename__ = TABLE_PREFIX + "chemical__disease"
    id = Column(Integer, primary_key=True)

    direct_evidence = Column(String(255))
    inference_gene_symbol = Column(String(255))
    inference_score = Column(REAL)
    chemical__id = foreign_key_to('chemical')
    disease__id = foreign_key_to('disease')


class ChemicalDiseaseOmim(Base):
    __tablename__ = TABLE_PREFIX + "chemical__disease__omim_id"
    id = Column(Integer, primary_key=True)

    chemical__disease__id = foreign_key_to('chemical__disease')
    omim_id = Column(Integer)


class ChemicalDiseasePubmedid(Base):
    __tablename__ = TABLE_PREFIX + "chemical__disease__pubmed_id"
    id = Column(Integer, primary_key=True)

    chemical__disease__id = foreign_key_to('chemical__disease')
    pubmed_id = Column(Integer)


class ChemPathwayEnriched(Base):
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


class ChemGeneIxn(Base):
    """Chemical–gene interactions"""

    __tablename__ = TABLE_PREFIX + "chem_gene_ixn"
    id = Column(Integer, primary_key=True)

    organism_id = Column(Integer)
    interaction = Column(Text)
    chemical__id = foreign_key_to('chemical')
    gene__id = foreign_key_to('gene')

    def __repr__(self):
        return self.interaction


class ChemGeneIxnGeneForm(Base):
    """Chemical–gene interactions gene forms"""

    __tablename__ = TABLE_PREFIX + "chem_gene_ixn__gene_form"
    id = Column(Integer, primary_key=True)

    chem_gene_ixn__id = foreign_key_to('chem_gene_ixn')
    gene_form = Column(String(255))

    def __repr__(self):
        return self.gene_form


class ChemGeneIxnInteractionAction(Base):
    """Chemical–gene interactions actions"""

    __tablename__ = TABLE_PREFIX + "chem_gene_ixn__interaction_action"
    id = Column(Integer, primary_key=True)

    chem_gene_ixn__id = foreign_key_to('chem_gene_ixn')
    interaction_action = Column(String(255))


class ChemGeneIxnPubmed(Base):
    """Chemical–gene interactions PubMed links"""

    __tablename__ = TABLE_PREFIX + "chem_gene_ixn__pubmed_id"
    id = Column(Integer, primary_key=True)

    chem_gene_ixn__id = foreign_key_to('chem_gene_ixn')
    pubmed_id = Column(Integer)

    def __repr__(self):
        return self.pubmed_id


class ChemGoEnriched(Base):
    """Chemical–GO enriched associations"""

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

    def __repr__(self):
        return self.go_term_name


class DiseasePathway(Base):
    __tablename__ = TABLE_PREFIX + "disease__pathway"
    id = Column(Integer, primary_key=True)

    pathway__id = foreign_key_to('pathway')
    disease__id = foreign_key_to('disease')
    inference_gene_symbol = Column(String(255))


class ExposureEvent(Base):
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


class GeneDisease(Base):
    __tablename__ = TABLE_PREFIX + "gene__disease"
    id = Column(Integer, primary_key=True)

    direct_evidence = Column(String(255))
    inference_chemical_name = Column(String(255))
    inference_score = Column(REAL)
    gene__id = foreign_key_to('gene')
    disease__id = foreign_key_to('disease')


class GeneDiseaseOmim(Base):
    __tablename__ = TABLE_PREFIX + "gene__disease__omim_id"
    id = Column(Integer, primary_key=True)

    gene__disease__id = foreign_key_to('gene__disease')
    omim_id = Column(Integer)


class GeneDiseasePubmed(Base):
    __tablename__ = TABLE_PREFIX + "gene__disease__pubmed_id"
    id = Column(Integer, primary_key=True)

    gene__disease__id = foreign_key_to('gene__disease')
    pubmed_id = Column(Integer)

    def __repr__(self):
        return self.pubmed_id


class GenePathway(Base):
    __tablename__ = TABLE_PREFIX + "gene__pathway"
    id = Column(Integer, primary_key=True)

    pathway__id = foreign_key_to('pathway')
    gene__id = foreign_key_to('gene')

    def __repr__(self):
        return self.pathway_name
