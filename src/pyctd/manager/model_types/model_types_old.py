# -*- coding: utf-8 -*-

class Action:
    parent_code = ('clv', 'deg', 'gly', 'lip', 'met', 'rib', 'sec', 'trt', 'upt')

    typename = (
        'abundance',
        'acetylation',
        'activity',
        'acylation',
        'ADP-ribosylation',
        'alkylation',
        'amination',
        'binding',
        'carbamoylation',
        'carboxylation',
        'chemical synthesis',
        'cleavage',
        'cotreatment',
        'degradation',
        'ethylation',
        'export',
        'expression',
        'farnesylation',
        'folding',
        'geranoylation',
        'glucuronidation',
        'glutathionylation',
        'glycation',
        'glycosylation',
        'hydrolysis',
        'hydroxylation',
        'import',
        'lipidation',
        'localization',
        'metabolic processing',
        'methylation',
        'mutagenesis',
        'myristoylation',
        'N-linked glycosylation',
        'nitrosation',
        'nucleotidylation',
        'O-linked glycosylation',
        'oxidation',
        'palmitoylation',
        'phosphorylation',
        'prenylation',
        'reaction',
        'reduction',
        'response to substance',
        'ribosylation',
        'secretion',
        'splicing',
        'stability',
        'sulfation',
        'sumoylation',
        'transport',
        'ubiquitination',
        'uptake'
    )


action = (
    'abundance',
    'acetylation',
    'activity',
    'acylation',
    'ADP-ribosylation',
    'alkylation',
    'amination',
    'binding',
    'carbamoylation',
    'carboxylation',
    'chemical synthesis',
    'cleavage',
    'cotreatment',
    'degradation',
    'ethylation',
    'export',
    'expression',
    'farnesylation',
    'folding',
    'geranoylation',
    'glucuronidation',
    'glutathionylation',
    'glycation',
    'glycosylation',
    'hydrolysis',
    'hydroxylation',
    'import',
    'lipidation',
    'localization',
    'metabolic processing',
    'methylation',
    'mutagenesis',
    'N-linked glycosylation',
    'nitrosation',
    'O-linked glycosylation',
    'oxidation',
    'phosphorylation',
    'prenylation',
    're',
    'reaction',
    'reduction',
    'response to substance',
    'ribosylation',
    'secretion',
    'splicing',
    'stability',
    'sulfation',
    'sumoylation',
    'transport',
    'ubiquitination',
    'uptake'
)

ontology = ('Biological Process', 'Cellular Component', 'Molecular Function')

interaction = ('increases', 'affects', 'decreases')

direct_evidence = ('marker/mechanism', 'marker/mechanism|therapeutic', 'therapeutic')

outcome_relationship = (
    'negative correlation',
    'no correlation',
    'positive correlation',
    'prediction/hypothesis'
)
