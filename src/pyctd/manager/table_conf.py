 # -*- coding: utf-8 -*-

import re
from collections import OrderedDict
from pydantic import BaseModel
from typing import List, Tuple, Optional, Union

from . import models

class OneToManyConfig(BaseModel):
    values_col: str
    id_col: str

class TableConfig(BaseModel):
    file_name: str
    columns: List[Union[str, Tuple[str,str]]]
    domain_id_column: Optional[Union[str, Tuple[str,str]]]
    one_to_many: Optional[Tuple[OneToManyConfig, ...]]


id_re = re.compile("((IDs)|(ID)|([A-Z][a-z]+)|([A-Z]{2,}))")


def standard_db_name(file_column_name: str) -> str:
    """return a standard name by following rules:
    1. find all regular expression partners ((IDs)|(ID)|([A-Z][a-z]+)|([A-Z]{2,}))
    2. lower very part and join again with _
    This method is only used if values in table[model]['columns'] are str

    :param str file_column_name: name of column in file
    :return: standard name
    :rtype: str
    """
    found = id_re.findall(file_column_name)

    if not found:
        return file_column_name

    return '_'.join(x[0].lower() for x in found)


models_to_map = (models.Chemical, models.Pathway, models.Gene, models.Disease)

# ALERT: All strings in 'columns' and 'domain_id_column' will be translate by def standard_db_name into
# (column_name_in_file, standard_column_name_in_db)
tables = OrderedDict([
    (models.Pathway, TableConfig(
        file_name= 'CTD_pathways.tsv.gz',
        columns= [
            'PathwayName',
            'PathwayID',
        ],
        one_to_many=None,
        domain_id_column= 'PathwayID'
    )),

    (models.Gene, TableConfig(
        file_name= 'CTD_genes.tsv.gz',
        columns= [
            'GeneSymbol',
            'GeneName',
            'GeneID'
        ],
        one_to_many= (
            OneToManyConfig(values_col='AltGeneIDs', id_col='alt_gene_id'),
            OneToManyConfig(values_col='Synonyms', id_col='synonym'),
            OneToManyConfig(values_col='BioGRIDIDs', id_col='biogrid_id'),
            OneToManyConfig(values_col='PharmGKBIDs', id_col='pharmgkb_id'),
            OneToManyConfig(values_col='UniProtIDs', id_col='uniprot_id')
        ),
<<<<<<< HEAD
        domain_id_column= 'GeneID'
    )),

    (models.Chemical, TableConfig(
        file_name= 'CTD_chemicals.tsv.gz',
        columns= [
=======
        "domain_id_column": 'GeneID'
    }),
    (models.Chemical, {
        "file_name": 'CTD_chemicals.tsv.gz',
        "columns": [
>>>>>>> c9180255fb28d233b9e4f4292e66ad47488fbe50
            'ChemicalName',
            'ChemicalID',
            'CasRN',
            'Definition',
        ],
<<<<<<< HEAD
        domain_id_column= 'ChemicalID',
        one_to_many= (
            OneToManyConfig(values_col='ParentIDs', id_col='parent_id'),
            OneToManyConfig(values_col='TreeNumbers', id_col='tree_number'),
            OneToManyConfig(values_col='ParentTreeNumbers', id_col='parent_tree_number'),
            OneToManyConfig(values_col='Synonyms', id_col='synonym'),
=======
        "domain_id_column": 'ChemicalID',
        "one_to_many": (
            ('ParentIDs', 'parent_id'),
            ('TreeNumbers', 'tree_number'),
            ('ParentTreeNumbers', 'parent_tree_number'),
            ('Synonyms', 'synonym'),
            #('DrugBankIDs', 'drugbank_id')
>>>>>>> c9180255fb28d233b9e4f4292e66ad47488fbe50
        ),
    )),

    (models.Disease, TableConfig(
        file_name= 'CTD_diseases.tsv.gz',
        columns= [
            'DiseaseName',
            'DiseaseID',
            'Definition',
            'ParentIDs',
            'TreeNumbers',
            'ParentTreeNumbers'
        ],
        one_to_many= (
            OneToManyConfig(values_col="AltDiseaseIDs", id_col='alt_disease_id'),
            OneToManyConfig(values_col='Synonyms', id_col='synonym'),
            OneToManyConfig(values_col='SlimMappings', id_col="slim_mapping")
        ),
        domain_id_column= 'DiseaseID'
    )),

    (models.ExposureEvent, TableConfig(
        file_name= 'CTD_exposure_events.tsv.gz',
        columns= [
            # ('exposurestressorname', 'chemical_name'),
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
            # ('diseasename', 'disease_name'),
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
        ],
        one_to_many=None,
        domain_id_column=None
    )),

    (models.DiseasePathway, TableConfig(
        file_name= 'CTD_diseases_pathways.tsv.gz',
        columns= [
            'DiseaseID',
            'PathwayID',
            'InferenceGeneSymbol'
        ],
        domain_id_column=None,
        one_to_many=None
    )),

    (models.GenePathway, TableConfig(
        file_name='CTD_genes_pathways.tsv.gz',
        columns= [
            'GeneID',
            'PathwayID'
        ],
        domain_id_column=None,
        one_to_many=None
    )),

    (models.ChemPathwayEnriched, TableConfig(
        file_name='CTD_chem_pathways_enriched.tsv.gz',
        columns=[
            'ChemicalID',
            'PathwayID',
            ('PValue', 'p_value'),
            ('CorrectedPValue', 'corrected_p_value'),
            'TargetMatchQty',
            'TargetTotalQty',
            'BackgroundMatchQty',
            'BackgroundTotalQty',
        ],
        domain_id_column=None,
        one_to_many=None
    )),

    (models.ChemGoEnriched, TableConfig(
        file_name='CTD_chem_go_enriched.tsv.gz',
        columns=[
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
        domain_id_column=None,
        one_to_many=None
    )),

    (models.Action, TableConfig(
        file_name='CTD_chem_gene_ixn_types.tsv',
        columns=[
            'TypeName',
            'Code',
            'Description',
            'ParentCode'
        ],
        domain_id_column=None,
        one_to_many=None
    )),

    (models.ChemGeneIxn, TableConfig(
        file_name='CTD_chem_gene_ixns.tsv.gz',
        columns=[
            'ChemicalID',
            'GeneID',
            'OrganismID',
            'Interaction',
        ],
        one_to_many=(
            OneToManyConfig(values_col='PubMedIDs',id_col= 'pubmed_id'),
            OneToManyConfig(values_col='InteractionActions', id_col='interaction_action'),
            OneToManyConfig(values_col='GeneForms', id_col='gene_form'),
        ),
        domain_id_column=None
    )),

    (models.ChemicalDisease, TableConfig(
        file_name= 'CTD_chemicals_diseases.tsv.gz',
        columns= [
            'DirectEvidence',
            'InferenceGeneSymbol',
            'InferenceScore',
            'ChemicalID',
            'DiseaseID',
        ],
        one_to_many= (
            OneToManyConfig(values_col='PubMedIDs', id_col='pubmed_id'),
            OneToManyConfig(values_col='OmimIDs', id_col='omim_id'),
        ),
        domain_id_column=None
    )),

    (models.GeneDisease, TableConfig(
        file_name='CTD_genes_diseases.tsv.gz',
        columns=[
            'GeneID',
            'DiseaseID',
            'DirectEvidence',
            'InferenceChemicalName',
            'InferenceScore',
        ],
        one_to_many=(
            OneToManyConfig(values_col='PubMedIDs', id_col='pubmed_id'),
            OneToManyConfig(values_col='OmimIDs', id_col='omim_id'),
        ),
        domain_id_column=None
    )),

])

for model in tables:

    tables[model].columns = [
        (column, standard_db_name(column)) if isinstance(column, str) else column
        for column in tables[model].columns
    ]

    if isinstance(tables[model].domain_id_column, str):
        d_id_col = str(tables[model].domain_id_column)
        if isinstance(d_id_col, str):
            tables[model].domain_id_column = (d_id_col, standard_db_name(d_id_col))
