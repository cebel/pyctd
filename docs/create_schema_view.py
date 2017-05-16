"""Create UML models for all SQLAlchemy models in PyCTD. Test only on Linux 
install before
python3 -m pip install sadisplay
sudo apt-get install graphviz
"""

import codecs
import sadisplay
from pyctd.manager.database import models
import os
import inspect
import sqlalchemy

base_folder = './source/_static/models/'

def create_uml_files(list_of_models, file_prefix):
    desc = sadisplay.describe(list_of_models)
    path_prefix = os.path.join(base_folder,file_prefix)
    with codecs.open(path_prefix+'.dot', 'w', encoding='utf-8') as f:
        f.write(sadisplay.dot(desc))
    os.system(''.join(['dot -Tpng ',path_prefix,'.dot > ',path_prefix,'.png']))

# for all models one UML
list_of_all_models = [getattr(models, attr) for attr in dir(models)]
create_uml_files(list_of_all_models, 'all')


## for every model one UML
#for cls in list_of_all_models:
#    if inspect.isclass(cls) and type(cls)==sqlalchemy.ext.declarative.api.DeclarativeMeta:
#        create_uml_files([cls], cls.__name__)

# Special UMLs

# Disease
create_uml_files([
    models.Disease,
    models.DiseaseAltdiseaseid,
    models.DiseasePathway,
    models.DiseaseSlimmapping,
    models.DiseaseSynonym,
    models.DiseasePathway
], 'disease')

# Gene
create_uml_files([
    models.Gene,
    models.GeneAltGeneId,
    models.GeneBiogrid,
    models.GeneDisease,
    models.GenePathway,
    models.GenePharmgkb,
    models.GeneSynonym,
    models.GeneUniprot
], 'gene')

# GeneDisease
create_uml_files([
    models.GeneDisease,
    models.Gene,
    models.Disease,
    models.GeneDiseasePubmed,
    models.GeneDiseaseOmim,
], 'geneDisease')

# Chemical
create_uml_files([
    models.Chemical,
    models.ChemicalParentid,
    models.ChemicalTreenumber,
    models.ChemicalDrugbank,
    models.ChemicalSynonym,
], 'chemical')

# ChemicalDisease
create_uml_files([
    models.ChemicalDisease,
    models.Chemical,
    models.Disease,
    models.ChemicalDiseaseOmim,
    models.ChemicalDiseasePubmedid,
], 'chemicalDisease')

# ChemGeneIxn
create_uml_files([
    models.ChemGeneIxn,
    models.ChemGeneIxnGeneForm,
    models.ChemGeneIxnInteractionAction,
    models.ChemGeneIxnPubmed,
    models.Gene,
    models.Chemical
],'chemGeneIxn')

# DiseasePathway
create_uml_files([
    models.DiseasePathway,
    models.Disease,
    models.DiseasePathway,
],'diseasePathway')

# GeneDisease
create_uml_files([
    models.GeneDisease,
    models.Gene,
    models.GeneDiseaseOmim,
    models.GeneDiseasePubmed,
    models.Disease,
],'geneDisease')