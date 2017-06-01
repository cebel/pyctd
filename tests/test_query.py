# -*- coding: utf-8 -*-

import logging
import unittest
import os
from pyctd.manager.models import GeneAltGeneId, Pathway, DiseasePathway, Disease, Chemical, ChemGeneIxn, Gene,\
    ChemicalDisease, GeneDiseasePubmed, GeneDiseaseOmim, GeneDisease, ChemGeneIxnGeneForm, ChemGeneIxnPubmed, \
    ChemGeneIxnInteractionAction, ChemicalDiseasePubmedid, ChemicalDiseaseOmim, ChemicalSynonym, ChemicalDrugbank, \
    ChemicalTreenumber, ChemicalParentid, GeneUniprot, GeneSynonym, GenePharmgkb, GenePathway, GeneBiogrid, \
    DiseaseSynonym, DiseaseSlimmapping, DiseaseAltdiseaseid, Action, ChemGoEnriched, ChemicalParenttreenumber, \
    ChemPathwayEnriched, ExposureEvent
from pyctd.manager.defaults import DEFAULT_SQLITE_TEST_DATABASE_NAME

import pyctd
import shutil
from pyctd.manager import table_conf
from pyctd.manager.database import DbManager, BaseDbManager
from pyctd.manager.query import QueryManager
from pyctd.constants import PYCTD_DATA_DIR
from pyctd.manager.defaults import sqlalchemy_connection_string_4_tests

log = logging.getLogger(__name__)

dir_path = os.path.dirname(os.path.realpath(__file__))
test_data_location = "data"
connection = sqlalchemy_connection_string_4_tests

# test data folder
test_data_folder = os.path.join(PYCTD_DATA_DIR, 'tests')
if not os.path.exists(test_data_folder):
    os.mkdir(test_data_folder)

@staticmethod
def download_urls(dummy1, dummy2):
    """
    overwrites pyctd.manager.database.DbManager.download_urls in TestImport.setup
    :param dummy1: dummy parameter
    :param dummy2: dummy parameter
    """

    file_names = [x['file_name'] for x in list(table_conf.tables.values())]
    for file_name in file_names:
        test_file_path = os.path.join(dir_path, test_data_location, file_name)
        destination_path = os.path.join(test_data_folder, file_name)
        shutil.copy(test_file_path, destination_path)


class TestImport(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        DbManager.pyctd_data_dir = test_data_folder
        DbManager.download_urls = download_urls
        pyctd.update(connection=connection)
        cls.query = QueryManager(connection=connection)
        cls.session = BaseDbManager(connection=connection).session

    @classmethod
    def tearDownClass(cls):
        os.remove(DEFAULT_SQLITE_TEST_DATABASE_NAME)
        shutil.rmtree(test_data_folder)
        cls.session.close()

    def test_number_of_inserts(self):
        models = [
            (GeneAltGeneId, 6),
            (Pathway, 3),
            (DiseasePathway, 6),
            (Disease, 3),
            (Chemical, 3),
            (ChemGeneIxn, 6),
            (Gene, 3),
            (ChemicalDisease, 6),
            (GeneDiseasePubmed, 12),
            (GeneDiseaseOmim, 12),
            (GeneDisease, 6),
            (ChemGeneIxnGeneForm, 12),
            (ChemGeneIxnPubmed, 12),
            (ChemGeneIxnInteractionAction, 6),
            (ChemicalDiseasePubmedid, 12),
            (ChemicalDiseaseOmim, 12),
            (ChemicalSynonym, 6),
            (ChemicalDrugbank, 6),
            (ChemicalTreenumber, 6),
            (ChemicalParentid, 6),
            (GeneUniprot, 6),
            (GeneSynonym, 6),
            (GenePharmgkb, 6),
            (GenePathway, 6),
            (GeneBiogrid, 6),
            (DiseaseSynonym, 6),
            (DiseaseSlimmapping, 6),
            (DiseaseAltdiseaseid, 6),
            (Action, 3),
            (ChemGoEnriched, 3),
            (ChemicalParenttreenumber, 6),
            (ChemPathwayEnriched, 3),
            (ExposureEvent, 3)
        ]
        for model, num_of_results in models:
            self.assertEqual(num_of_results, self.session.query(model).count())

    def test_get_disease(self):
        r = self.query.get_disease(limit=1)[0]
        self.assertEqual([x.alt_disease_id for x in r.alt_disease_ids], ['AltDiseaseID1_1', 'AltDiseaseID1_2'])
        self.assertEqual(r.definition, 'Definition1')
        self.assertEqual(r.disease_id, 'DiseaseID1')
        self.assertEqual(r.disease_name, 'DiseaseName1')
        self.assertEqual(r.parent_ids, 'ParentID1_1|ParentID1_2')
        self.assertEqual(r.parent_tree_numbers, 'ParentTreeNumber1_1|ParentTreeNumber1_2')
        self.assertEqual([x.slim_mapping for x in r.slim_mappings], ['SlimMapping1_1', 'SlimMapping1_2'])
        self.assertEqual([x.synonym for x in r.synonyms], ['Synonym1_1', 'Synonym1_2'])
        self.assertEqual(r.tree_numbers, 'TreeNumber1_1|TreeNumber1_2')
        self.session.commit()

    def test_get_gene(self):
        r = self.query.get_gene(limit=1)[0]
        self.assertEqual([x.alt_gene_id for x in r.alt_gene_ids], [1, 2])
        self.assertEqual([x.biogrid_id for x in r.biogrid_ids], [1, 2])
        self.assertEqual(r.gene_id, 1)
        self.assertEqual(r.gene_name, 'GeneName1')
        self.assertEqual(r.gene_symbol, 'GeneSymbol1')
        self.assertEqual([x.pharmgkb_id for x in r.pharmgkb_ids], ['PharmGKBID1_1', 'PharmGKBID1_2'])
        self.assertEqual([x.synonym for x in r.synonyms] ,['Synonym1_1', 'Synonym1_2'])
        self.assertEqual([x.uniprot_id for x in r.uniprot_ids], ['UniProtID1_1', 'UniProtID1_2'])
        self.session.commit()

    def test_get_pathway(self):
        r = self.query.get_pathway()[0]
        self.assertEqual(r.pathway_id, 'PathwayID1')
        self.assertEqual(r.pathway_name, 'PathwayName1')
        self.session.commit()

    def test_get_chemicals(self):
        chemical = self.query.get_chemical()[0]
        self.assertEqual(chemical.chemical_id, 'ChemicalID1')
        self.assertEqual(chemical.chemical_name, 'ChemicalName1')
        self.assertEqual(chemical.cas_rn, 'CasRN1')
        self.session.commit()

    def test_get_chem_gene_interaction_actions(self):
        r = self.query.get_chem_gene_interaction_actions()[0]
        #self.assertEqual()

    def test_gene_forms(self):
        r = self.query.gene_forms
        self.assertEqual(r, ['GeneForm1_1',
                                'GeneForm1_2',
                                'GeneForm2_1',
                                'GeneForm2_2',
                                'GeneForm3_1',
                                'GeneForm3_2'])

    def test_interaction_actions(self):
        result = self.query.interaction_actions
        expected_result = ['InteractionActions1',
                            'InteractionActions2',
                            'InteractionActions3',
                            'InteractionActions4',
                            'InteractionActions5',
                            'InteractionActions6']
        self.assertEqual(result, expected_result)

    def test_actions(self):
        self.assertEqual(self.query.actions, ['TypeName1', 'TypeName2', 'TypeName3'])

    def test_pathways(self):
        pathways = [x.pathway_name for x in self.query.pathways]
        self.assertEqual(pathways, ['PathwayName1', 'PathwayName2', 'PathwayName3'])

    def test_get_gene_disease(self):
        r = self.query.get_gene_disease()[0]
        self.assertEqual(r.direct_evidence, 'DirectEvidence1')
        self.assertEqual(r.disease.disease_name, 'DiseaseName1')
        #self.assertEqual(r.gene)

    def test_direct_evidences(self):
        direct_evidences = self.query.direct_evidences

    def test_get_disease_pathways(self):
        disease_pathways = self.query.get_disease_pathways()[0]

    def test_get_chemical_diseases(self):
        chemical_diseases = self.query.get_chemical_diseases()[0]

    def test_get_gene_pathways(self):
        gene_pathways = self.query.get_gene_pathways()[0]

    #def test_get_go_enriched__by__chemical_name(self):
    #    r = self.query.get_go_enriched__by__chemical_name(chemical_name='ChemicalName1')[0]

    #def test_get_pathway_enriched__by__chemical_name(self):
    #    r = self.query.get_pathway_enriched__by__chemical_name(chemical_name='ChemicalName1')[0]

    #def test_get_therapeutic_chemical__by__disease_name(self):
    #    r = self.query.get_therapeutic_chemical__by__disease_name(disease_name='DiseaseName1', limit=1)[0]

    #def test_get_marker_chemical__by__disease_name(self):
    #    r = self.query.get_marker_chemical__by__disease_name(disease_name='DiseaseName1', limit=1)[0]

    def test_get_chemical__by__disease(self):
        r = self.query.get_chemical__by__disease(disease_name='DiseaseName1', limit=1)[0]

    def get_action(self):
        action = self.query.get_action()[0]

