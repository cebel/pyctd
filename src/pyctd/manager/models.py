# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Table, UniqueConstraint
from sqlalchemy import Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy.schema import UniqueConstraint

Base = declarative_base()

TABLE_PREFIX = 'pyctd_'


def foreign_key_to(table_name):
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
    casrn = Column(String(255))
    definition = Column(Text)
    parent_ids = Column(String(255))
    tree_numbers = Column(Text)
    parent_tree_numbers = Column(Text)

    def __repr__(self):
        return self.chemical_name


class ChemicalDrugbank(Base):
    __tablename__ = TABLE_PREFIX + "chemical__drugbank"
    id = Column(Integer, primary_key=True)

    chemical__id = foreign_key_to('chemical')
    drugbank_id = Column(Integer)


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
    inference_score = Column(Float)
    chemical__id = foreign_key_to('chemical')
    disease__id = foreign_key_to('disease')


class ChemicalDiseaseOmim(Base):
    __tablename__ = TABLE_PREFIX + "chemical__disease__omim"
    id = Column(Integer, primary_key=True)

    chemical__disease__id = foreign_key_to('chemical__disease')
    omim_id = Column(Integer)


class ChemPathwayEnriched(Base):
    __tablename__ = TABLE_PREFIX + "chem_pathway_enriched"
    id = Column(Integer, primary_key=True)

    pathway_name = Column(String(255))
    pathway_id = Column(Text)
    p_value = Column(String(255))
    corrected_p_value = Column(String(255))
    target_match_qty = Column(Text)
    target_total_qty = Column(Text)
    background_match_qty = Column(Text)
    background_total_qty = Column(Integer)
    chemical__id = foreign_key_to('chemical')

    def __repr__(self):
        return self.pathway_name


class ChemGeneIxn(Base):
    __tablename__ = TABLE_PREFIX + "chem_gene_ixn"
    id = Column(Integer, primary_key=True)

    gene_forms = Column(Text)
    organism = Column(String(255))
    organism_id = Column(Integer)
    interaction = Column(Text)
    chemical__id = foreign_key_to('chemical')
    gene__id = foreign_key_to('gene')

    def __repr__(self):
        return self.interaction


class ChemGeneIxnGeneForm(Base):
    __tablename__ = TABLE_PREFIX + "chem_gene_ixn__gene_form"
    id = Column(Integer, primary_key=True)

    chem_gene_ixn__id = foreign_key_to('chem_gene_ixn')
    gene_form = Column(String(255))

    def __repr__(self):
        return self.gene_form


class ChemGeneIxnInteractionAction(Base):
    __tablename__ = TABLE_PREFIX + "chem_gene_ixn_interaction_action"
    id = Column(Integer, primary_key=True)

    chem_gene_ixn__id = foreign_key_to('chem_gene_ixn')
    interaction = Column(String(255))
    action = Column(String(255))

    def __repr__(self):
        return '{}:{}'.format(self.interaction)


class ChemGeneIxnPubmed(Base):
    __tablename__ = TABLE_PREFIX + "chem_gene_ixn__pubmed"
    id = Column(Integer, primary_key=True)

    chem_gene_ixn__id = foreign_key_to('chem_gene_ixn')
    pubmed_id = Column(Integer)

    def __repr__(self):
        return self.pubmed_id


class ChemGoEnriched(Base):
    __tablename__ = TABLE_PREFIX + "chem_go_enriched"
    id = Column(Integer, primary_key=True)

    ontology = Column(String(255))
    go_term_name = Column(String(255))
    go_term_id = Column(String(255))
    highest_go_level = Column(Integer)
    p_value = Column(String(255))
    corrected_p_value = Column(String(255))
    target_match_qty = Column(String(255))
    target_total_qty = Column(Text)
    background_match_qty = Column(Text)
    background_total_qty = Column(Integer)
    chemical__id = foreign_key_to('chemical')

    def __repr__(self):
        return self.go_term_name


class ChemicalDiseasePubmed(Base):
    __tablename__ = TABLE_PREFIX + "chemical__disease__pubmed"
    id = Column(Integer, primary_key=True)

    chemical__disease__id = foreign_key_to('chemical__disease')
    pubmed_id = Column(Integer)

    def __repr__(self):
        return self.pubmed_id


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
    stressor_agent_id = Column(String(255))
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
    disease_name = Column(String(255))
    disease_id = Column(String(255))
    phenotype_name = Column(String(255))
    phenotype_id = Column(String(255))
    reference = Column(Integer)


class GeneDisease(Base):
    __tablename__ = TABLE_PREFIX + "gene__disease"
    id = Column(Integer, primary_key=True)

    direct_evidence = Column(String(255))
    inference_chemical_name = Column(String(255))
    inference_score = Column(Float)
    omim_ids = Column(String(255))
    gene__id = foreign_key_to('gene')
    disease__id = foreign_key_to('disease')


class GeneDiseasePubmed(Base):
    __tablename__ = TABLE_PREFIX + "gene__disease__pubmed"
    id = Column(Integer, primary_key=True)

    gene__disease__id = foreign_key_to('gene__disease')
    pubmed_id = Column(Integer)

    def __repr__(self):
        return self.pubmed_id


class GenePathway(Base):
    __tablename__ = TABLE_PREFIX + "gene_pathway"
    id = Column(Integer, primary_key=True)

    pathway_name = Column(String(255))
    pathway_id = Column(Text)
    gene__id = foreign_key_to('gene')

    def __repr__(self):
        return self.pathway_name