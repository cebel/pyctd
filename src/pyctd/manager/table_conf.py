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

# ALERT: All strings in 'columns' and 'domain_id_column' will be translate by def standard_db_name into
# (column_name_in_file, standard_column_name_in_db)
tables = OrderedDict([
    ("pathway", {
        "file_name": 'CTD_pathways.tsv.gz',
        "columns": [
            'PathwayName',
            'PathwayID',
        ],
        "domain_id_column": 'PathwayID'
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
        "domain_id_column": 'GeneID'
    }),

    ("chemical", {
        "file_name": 'CTD_chemicals.tsv.gz',
        "columns": [
            'ChemicalName',
            'ChemicalID',
            'CasRN',
            'Definition',
        ],
        "domain_id_column": 'ChemicalID',
        "one_to_many": (
            ('ParentIDs', 'parent_id'),
            ('TreeNumbers', 'tree_number'),
            ('ParentTreeNumbers', 'parent_tree_number'),
            ('Synonyms', 'synonym'),
            ('DrugBankIDs', 'drugbank_id')
        ),
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
        "domain_id_column": 'DiseaseID'
    }),

    ("exposure_event", {
        "file_name": 'CTD_exposure_events.tsv.gz',
        "columns": [
            #('exposurestressorname', 'chemical_name'),
            ('exposurestressorid', 'chemical_id'),
            ('stressorsourcecategory', 'stressor_source_category'),
            ('stressorsourcedetails', 'stressor_source_details'),
            ('numberofstressorsamples', 'number_of_stressor_samples'),
            ('stressornotes', 'stress_or_notes'),
            ('numberofreceptors', 'number_of_receptors'),
            'receptors',
            ('receptornotes', 'receptor_notes'),
            ('smokingstatus', 'smoking_status'),
            'age',
            ('ageunitsofmeasurement', 'age_units_of_measurement'),
            ('agequalifier', 'age_qualifier'),
            'sex',
            'race',
            'methods',
            ('detectionlimit', 'detection_limit'),
            ('detectionlimituom', 'detection_limit_uom'),
            ('detectionfrequency', 'detection_frequency'),
            'medium',
            ('exposuremarker', 'exposure_marker'),
            ('exposuremarkerid', 'exposure_marker_id'),
            ('markerlevel', 'marker_level'),
            ('markerunitsofmeasurement', 'marker_units_of_measurement'),
            ('markermeasurementstatistic', 'marker_measurement_statistic'),
            ('assaynotes', 'assay_notes'),
            ('studycountries', 'study_countries'),
            ('stateorprovince', 'state_or_province'),
            ('citytownregionarea', 'city_town_region_area'),
            ('exposureeventnotes', 'exposure_event_notes'),
            ('outcomerelationship', 'outcome_relationship'),
            #('diseasename', 'disease_name'),
            ('diseaseid', 'disease_id'),
            ('phenotypename', 'phenotype_name'),
            ('phenotypeid', 'phenotype_id'),
            ('phenotypeactiondegreetype', 'phenotype_action_degree_type'),
            'anatomy',
            ('exposureoutcomenotes', 'exposure_outcome_notes'),
            'reference',
            ('associatedstudytitles', 'associated_study_titles'),
            ('enrollmentstartyear', 'enrollment_start_year'),
            ('enrollmentendyear', 'enrollment_end_year'),
            ('studyfactors', 'study_factors')
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

    ("gene__pathway", {
        "file_name": 'CTD_genes_pathways.tsv.gz',
        "columns": [
            'GeneID',
            'PathwayID'
        ],
    }),

    ("chem__pathway_enriched", {
        "file_name": 'CTD_chem_pathways_enriched.tsv.gz',
        "columns": [
            'ChemicalID',
            'PathwayID',
            ('PValue', 'p_value'),
            ('CorrectedPValue', 'corrected_p_value'),
            'TargetMatchQty',
            'TargetTotalQty',
            'BackgroundMatchQty',
            'BackgroundTotalQty',
        ],
    }),

    ("chem__go_enriched", {
        "file_name": 'CTD_chem_go_enriched.tsv.gz',
        "columns": [
            'ChemicalID',
            'Ontology',
            ('GOTermName', 'go_term_name'),
            ('GOTermID', 'go_term_id'),
            ('HighestGOLevel', 'highest_go_level'),
            ('PValue', 'p_value'),
            ('CorrectedPValue', 'corrected_p_value'),
            'TargetMatchQty',
            'TargetTotalQty',
            'BackgroundMatchQty',
            'BackgroundTotalQty'
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
            'ChemicalID',
            'GeneID',
            'OrganismID',
            'Interaction',
        ],
        "one_to_many": (
            ('PubMedIDs', 'pubmed_id'),
            ('InteractionActions', 'interaction_action'),
            ('GeneForms', 'gene_form'),
        )
    }),

    ("chemical__disease", {
        "file_name": 'CTD_chemicals_diseases.tsv.gz',
        "columns": [
            'DirectEvidence',
            'InferenceGeneSymbol',
            'InferenceScore',
            'ChemicalID',
            'DiseaseID',
        ],
        "one_to_many": (
            ('PubMedIDs', 'pubmed_id'),
            ('OmimIDs', 'omim_id'),
        ),
    }),

    ("gene__disease", {
        "file_name": 'CTD_genes_diseases.tsv.gz',
        "columns": [
            'GeneID',
            'DiseaseID',
            'DirectEvidence',
            'InferenceChemicalName',
            'InferenceScore',
        ],
        "one_to_many": (
            ('PubMedIDs', 'pubmed_id'),
            ('OmimIDs', 'omim_id'),
        ),
    }),

])

for table_name in tables:
    cols = tables[table_name]['columns']
    for i in range(len(cols)):
        if isinstance(cols[i], str):
            cols[i] = (cols[i], standard_db_name(cols[i]))
    if 'domain_id_column' in tables[table_name]:
        d_id_col = tables[table_name]['domain_id_column']
        if isinstance(d_id_col, str):
            tables[table_name]['domain_id_column'] = (d_id_col, standard_db_name(d_id_col))


