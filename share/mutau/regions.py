"""Regions for the tau+jets analysis.
"""

# System imports
from functools import partial

# owls-hep imports
from owls_hep.region import Region
from owls_hep.expression import expression_substitute

# Set up definitions
definitions = {
    # General weight
    'weight': 'weight_mc*weight_pileup',

    # Weight for events with b-jet or b-jet veto
    'weight_b': 'bjet_sf_MVX_NOMINAL_sf*bjet_sf_MVX_NOMINAL_ineff_sf',

    # Weights for events with muons
    'weight_mu': (
        'lep_0_NOMINAL_effSF_RecoMedium * '
        'lep_0_NOMINAL_HLT_mu20_iloose_L1MU15_MU_TRIG_QUAL_MEDIUM_MU_TRIG_ISO_NONE'
    ),
    'weight_mu_grad': (
        'lep_0_NOMINAL_effSF_RecoMedium * '
        'lep_0_NOMINAL_HLT_mu20_iloose_L1MU15_MU_TRIG_QUAL_MEDIUM_MU_TRIG_ISO_GRADIENT'
    ),

    # Muon trigger for 2015 data
    'mu_trigger': (
        '(HLT_mu20_iloose_L1MU15 && muTrigMatch_0_HLT_mu20_iloose_L1MU15)'),

    # OS/SS for mu+tau selection
    'os': 'lephad_qxq == -1',
    'ss': 'lephad_qxq == 1',

    # Nominal isolation
    'iso': (
        'lep_0_iso_ptcone40/1000.0/lep_0_pt < 0.01 && '
        'lep_0_iso_etcone20/1000.0/lep_0_pt < 0.04'),
    # Looser isolation
    'iso_loose': (
        'lep_0_iso_ptcone40/1000.0/lep_0_pt < 0.10 && '
        'lep_0_iso_etcone20/1000.0/lep_0_pt < 0.13'),
    # Gradient isolation WP
    'iso_gradient': 'lep_0_iso_wp >= 10000',

    # b-jet requirement and veto
    'bjet': 'n_bjets >= 1',
    'bveto': 'n_bjets == 0',

    # tau requirement
    'loose_tau': 'n_taus >= 1 && tau_0_pt > 25 && tau_0_jet_bdt_loose',
    'medium_tau': 'n_taus >= 1 && tau_0_pt > 25 && tau_0_jet_bdt_medium',
    'tight_tau': 'n_taus >= 1 && tau_0_pt > 25 && tau_0_jet_bdt_tight',

    'very_loose_not_medium_tau': 'n_taus >= 1 && tau_0_pt > 25 && tau_0_jet_bdt_score > 0.5 && !tau_0_jet_bdt_medium',
    'very_loose_not_loose_tau': 'n_taus >= 1 && tau_0_pt > 25 && tau_0_jet_bdt_score > 0.5 && !tau_0_jet_bdt_loose',

    # mu+tau T&P
    'mu_tau': (
        'n_electrons == 0 && '
        'n_muons == 1 && lep_0_id_medium && lep_0_pt > 22'),

    # Jet requirement
    '2jets': 'n_jets >= 2',

    # W CR
    'wcr': 'met_reco_et > 30 && lephad_mt_lep0_met > 60',
}

expr = partial(expression_substitute, definitions = definitions)

def _vary_me(name, selection, weight, label, patches, metadata, variations):
    if not name in globals():
        globals()[name] = Region(expr(selection),
                                 expr(weight),
                                 label,
                                 patches,
                                 metadata = metadata)
    for v in variations:
        globals()[name + v[0]] = Region(expr(selection + v[1]),
                                        expr(weight + v[2]),
                                        label + v[3],
                                        patches,
                                        metadata = metadata)


_id_variations = [
    ('_loose', '&& tau_0_jet_bdt_loose', '', ' (loose #tau)'),
    ('_medium', '&& tau_0_jet_bdt_medium', '', ' (medium #tau)'),
    ('_tight', '&& tau_0_jet_bdt_tight', '', ' (tight #tau)'),
]

# mu+tau regions
_variations = [
    ('_tau25', '&& HLT_tau25_medium1_tracktwo', '', ' (tau25)'),
    ('_tau35', '&& HLT_tau35_medium1_tracktwo', '', ' (tau35)'),
    ('_tau25_os', '&& [os] && HLT_tau25_medium1_tracktwo', '', ' (tau25, OS)'),
    ('_tau35_os', '&& [os] && HLT_tau35_medium1_tracktwo', '', ' (tau35, OS)'),
    ('_1p', '&& tau_0_n_tracks == 1', '', ' (1-prong)'),
    ('_3p', '&& tau_0_n_tracks == 3', '', ' (3-prong)'),
    ('_os', '&& [os]', '', ' (OS)'),
    ('_ss', '&& [ss]', '', ' (SS)'),
]

# Nominal mu+tau region and variations
_vary_me('mu_tau',
         '[mu_trigger] && [mu_tau] && [medium_tau] && [2jets] && [bjet] && [iso]',
         '[weight]',
         '#mu+#tau (run1 iso)',
         {'mc': expr('[weight_mu] * [weight_b]')},
         {'rqcd': 'mu_tau_qcd_cr'},
         _variations)

_vary_me('mu_tau_gradient',
         '[mu_trigger] && [mu_tau] && [medium_tau] && [2jets] && [bjet] && [iso_gradient]',
         '[weight]',
         '#mu+#tau (Gradient iso)',
         {'mc': expr('[weight_mu_grad] * [weight_b]')},
         {'rqcd': 'mu_tau_gradient_qcd_cr'},
         _variations)

_vary_me('mu_tau_loose',
         '[mu_trigger] && [mu_tau] && [medium_tau] && [2jets] && [bjet] && [iso_loose]',
         '[weight]',
         '#mu+#tau (Run1 loose iso)',
         {'mc': expr('[weight_mu] * [weight_b]')},
         {'rqcd': 'mu_tau_qcd_cr'},
         _variations)

# mu+tau region and variations without isolation cut
_vary_me('mu_tau_noiso',
         '[mu_trigger] && [mu_tau] && [medium_tau] && [2jets] && [bjet]',
         '[weight]',
         '#mu+#tau',
         {'mc': expr('[weight_mu] * [weight_b]')},
         {'rqcd': 'mu_tau_qcd_cr'},
         _variations)

# QCD CR with anti-isolation
_vary_me('mu_tau_qcd_cr',
         expr('[mu_trigger] && [mu_tau] && [medium_tau] && [2jets] && ![iso_loose]'),
         expr('[weight]'),
         'QCD CR (Run1 loose iso)',
         {'mc': expr('[weight_mu]')},
         {'rqcd': 'mu_tau_qcd_cr'},
         _variations)

# QCD CR with gradient anti-isolation
_vary_me('mu_tau_gradient_qcd_cr',
         expr('[mu_trigger] && [mu_tau] && [medium_tau] && [2jets] && ![iso_gradient]'),
         expr('[weight]'),
         'QCD CR (Gradient iso)',
         {'mc': expr('[weight_mu_grad]')},
         {'rqcd': 'mu_tau_gradient_qcd_cr'},
         _variations)

# QCD CR with anti-tau cut
_vary_me('mu_tau_qcd_cr_anti_tau',
         expr('[mu_trigger] && [mu_tau] && [very_loose_not_medium_tau] && [2jets] && ![iso_loose]'),
         expr('[weight]'),
         'QCD CR (anti-#tau, anti-iso)',
         {'mc': expr('[weight_mu]')},
         {'rqcd': 'mu_tau_qcd_cr'},
         _variations)

# W CR
_vary_me('mu_tau_w_cr',
         expr('[mu_trigger] && [mu_tau] && [medium_tau] && [bveto] && [wcr] && [iso]'),
         expr('[weight]'),
         'W CR',
         {'mc': expr('[weight_mu] * [weight_b]')},
         {'rqcd': 'mu_tau_qcd_cr'},
         _variations)

# W anti-tau CR
_vary_me('mu_tau_w_cr_anti_tau',
         expr('[mu_trigger] && [mu_tau] && [very_loose_not_medium_tau] && [bveto] && [wcr] && [iso]'),
         expr('[weight]'),
         'W CR (anti-#tau)',
         {'mc': expr('[weight_mu] * [weight_b]')},
         {'rqcd': 'mu_tau_qcd_cr'},
         _variations)
