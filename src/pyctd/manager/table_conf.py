# -*- coding: utf-8 -*-
from collections import OrderedDict
import re


def standard_db_name(file_column_name):
    """return a standard name
    :param file_column_name: name of column in file
    :type file_column_name: str
    """
    standard_name = file_column_name
    found = re.findall("((IDs)|(ID)|([A-Z][a-z]+)|([A-Z]{2,}))", file_column_name)
    if len(found):
        standard_name = '_'.join([x[0].lower() for x in found])
    return standard_name

domains_to_map = ('chemical', 'pathway', 'gene', 'disease')

tables = OrderedDict([
    ("pathway", {
        "file_name": 'CTD_pathways.tsv.gz',
        "columns": [
            'PathwayName',
            'PathwayID',
        ],
        "domain_id_column": ('PathwayID', 'pathway_id')
    }),

    ("gene", {
        "file_name": 'CTD_genes.tsv.gz',
        "columns": [
            'GeneSymbol',
            'GeneName',
            'GeneID'
        ],
        "one_to_many": (
            ('AltGeneIDs', 'alt_gene_id'),
            ('Synonyms', 'synonym'),
            ('BioGRIDIDs', 'biogrid_id'),
            ('PharmGKBIDs', 'pharmgkb_id'),
            ('UniProtIDs', 'uniprot_id')
        ),
        "domain_id_column": ('GeneID', 'gene_id')
    }),

    ("disease", {
        "file_name": 'CTD_diseases.tsv.gz',
        "columns": [
            'DiseaseName',
            'DiseaseID',
            'Definition',
            'ParentIDs',
            'TreeNumbers',
            'ParentTreeNumbers'
        ],
        "one_to_many": (
            ("AltDiseaseIDs", 'alt_disease_id'),
            ('Synonyms', 'synonym'),
            ('SlimMappings', "slim_mapping")
        ),
        "domain_id_column": ('DiseaseID', 'disease_id')
    }),

    ("exposure_event", {
        "file_name": 'CTD_exposure_events.tsv.gz',
        "columns": [
            ('stressoragentname', 'stressor_agent_name'),
            ('stressoragentid', 'stressor_agent_id'),
            ('numberofreceptors', 'number_of_receptors'),
            ('receptordescription', 'receptor_description'),
            ('receptornotes', 'receptor_notes'),
            ('studylocation', 'study_location'),
            ('assaymediums', 'assay_mediums'),
            ('assayedtermname', 'assayed_term_name'),
            ('assayedtermid', 'assayed_term_id'),
            ('assaylevel', 'assay_level'),
            ('assayunitsofmeasurement', 'assay_units_of_measurement'),
            ('assaymeasurementstatistic', 'assay_measurement_statistic'),
            ('assaynotes', 'assay_notes'),
            ('outcomerelationship', 'outcome_relationship'),
            ('diseasename', 'disease_name'),
            ('diseaseid', 'disease_id'),
            ('phenotypename', 'phenotype_name'),
            ('phenotypeid', 'phenotype_id'),
            'reference',
        ]
    }),

    ("disease__pathway", {
        "file_name": 'CTD_diseases_pathways.tsv.gz',
        "columns": [
            'DiseaseID',
            'PathwayID',
            'InferenceGeneSymbol'
        ],
    }),

    ("gene_pathway", {
        "file_name": 'CTD_genes_pathways.tsv.gz',
        "columns": [
            'GeneID',
            'PathwayID'
        ],
    }),

    ("gene_disease", {
        "file_name": 'CTD_genes_diseases.tsv.gz',
        "columns": [
            'GeneID',
            'DiseaseID',
            'DirectEvidence',
            'InferenceChemicalName',
            'InferenceScore',
            'OmimIDs',
            'PubMedIDs',
        ],
    }),

    ("chem_pathways_enriched", {
        "file_name": 'CTD_chem_pathways_enriched.tsv.gz',
        "columns": [
            'ChemicalID',
            'PathwayID',
            ('PValue', 'p_value'),
            'CorrectedPValue',
            'TargetMatchQty',
            'TargetTotalQty',
            'BackgroundMatchQty',
            'BackgroundTotalQty',
        ],
    }),

    ("chem_go_enriched", {
        "file_name": 'CTD_chem_go_enriched.tsv.gz',
        "columns": [
            'ChemicalID',
            'Ontology',
            'GOTermName',
            'GOTermID',
            'HighestGOLevel',
            ('PValue', 'p_value'),
            'CorrectedPValue',
            'TargetMatchQty',
            'TargetTotalQty',
            'BackgroundMatchQty',
            'BackgroundTotalQty'
        ],
    }),

    ("chemical_disease", {
        "file_name": 'CTD_chemicals_diseases.tsv.gz',
        "columns": [
            'ChemicalID',
            'DiseaseID',
            'DirectEvidence',
            'InferenceGeneSymbol',
            'InferenceScore',
            'OmimIDs',
            'PubMedIDs'
        ],
    }),

    ("action", {
        "file_name": 'CTD_chem_gene_ixn_types.tsv',
        "columns": [
            'TypeName',
            'Code',
            'Description',
            'ParentCode'
        ]
    }),

    ("chem_gene_ixn", {
        "file_name": 'CTD_chem_gene_ixns.tsv.gz',
        "columns": [
            'ChemicalName',
            'ChemicalID',
            'CasRN',
            'GeneSymbol',
            'GeneID',
            'GeneForms',
            'Organism',
            'OrganismID',
            'Interaction',
            'InteractionActions',
            'PubMedIDs'
        ]
    }),

    ("chemical", {
        "file_name": 'CTD_chemicals.tsv.gz',
        "columns": [
            'ChemicalName',
            'ChemicalID',
            'CasRN',
            'Definition',
            'ParentIDs',
            'TreeNumbers',
            'ParentTreeNumbers',
            'Synonyms',
            'DrugBankIDs'
        ],
        "domain_id_column": ('ChemicalID', 'chemical_id')
    })
])

for table_name in tables:
    cols = tables[table_name]['columns']
    for i in range(len(cols)):
        if isinstance(cols[i], str):
            cols[i] = (cols[i], standard_db_name(cols[i]))
