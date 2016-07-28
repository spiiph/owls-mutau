#!/bin/bash


# Plot many distributions for
# - OS Data vs MC
# - OS-SS


# Compute the path to the owls-mutau directory
SCRIPTS=$(dirname "$0")
OWLS="$SCRIPTS/.."

MC_REGIONS="\
  mu_tau_os mu_tau_ss \
  mu_tau_1p mu_tau_3p \
  mu_tau_tau25_os mu_tau_tau25_ss \
  mu_tau_tau25_1p mu_tau_tau25_3p \
  "
MC_REGIONS="\
  mu_tau_os mu_tau_ss \
  mu_tau_tau25_os mu_tau_tau25_ss \
  "

OSSS_REGIONS="\
  mu_tau \
  mu_tau_1p mu_tau_3p \
  mu_tau_tau25 \
  mu_tau_tau25_1p mu_tau_tau25_3p \
  "
OSSS_REGIONS="\
  mu_tau \
  mu_tau_tau25 \
  "

# All kinematic distributions
DISTRIBUTIONS="\
  tau_pt tau_eta tau_phi \
  tau_bdt_score tau_bdt_score_trig tau_n_tracks \
  mu_pt mu_eta mu_phi \
  bjet_multiplicity jet_multiplicity \
  deta dphi dr \
  met_et met_phi mt \
  mu nvx \
  "
# mu and tau kinematic distributions
DISTRIBUTIONS="\
  tau_pt tau_eta tau_phi \
  mu_pt mu_eta mu_phi \
  bjet_multiplicity jet_multiplicity \
  mu nvx \
  "

## Weight distributions
#DISTRIBUTIONS="\
  #NOMINAL_pileup_combined_weight \
  #lep_0_NOMINAL_MuEffSF_Reco_QualMedium \
  #lep_0_NOMINAL_MuEffSF_IsoGradient \
  #lep_0_NOMINAL_MuEffSF_HLT_mu20_iloose_L1MU15_OR_HLT_mu40_QualMedium_IsoIsoGradient \
  #lep_0_NOMINAL_MuEffSF_HLT_mu24_imedium_OR_HLT_mu50_QualMedium_IsoIsoGradient \
  #tau_0_NOMINAL_effSF_VeryLooseLlhEleOLR_electron  \
  #tau_0_NOMINAL_TAU_EFF_JETIDBDTMEDIUM  \
  #tau_0_NOMINAL_TAU_EFF_RECO  \
  #tau_0_NOMINAL_TAU_EFF_SELECTION \
  #"
#DISTRIBUTIONS="\
  #jet_NOMINAL_global_effSF_JVT \
  #jet_NOMINAL_global_effSF_MVX \
  #jet_NOMINAL_global_ineffSF_MVX \
  #"

EXTENSIONS="pdf eps"
EXTENSIONS="pdf"
DATA_PREFIX="/disk/d2/ohman/lhtnp_v16_merged"

LUMINOSITY=3193.68 # 1/pb
YEAR=2015

## Plots with MC backgrounds only
#OUTPUT="results/plots_mc/$YEAR"
#"$OWLS/tools/plot.py" \
  #--output $OUTPUT \
  #--extensions $EXTENSIONS \
  #--model-file "$OWLS/definitions/models-v12.py" \
  #--model mc \
  #--regions-file "$OWLS/definitions/regions-v12.py" \
  #--regions $MC_REGIONS \
  #--distributions-file "$OWLS/definitions/distributions.py" \
  #--distributions $DISTRIBUTIONS \
  #--environment-file "$SCRIPTS/environment.py" \
  #--text-count \
  #--label "MC15C, 20.7, Data $YEAR" \
  #--error-label "Stat. Unc." \
#data_prefix=$DATA_PREFIX \
#year=$YEAR \
#enable_systematics=False \
#luminosity=$LUMINOSITY

# Plots with OS-SS backgrounds
OUTPUT="results/plots_osss_fakes/$YEAR"
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/definitions/models-v12.py" \
  --model osss_fakes2 \
  --regions-file "$OWLS/definitions/regions-v12.py" \
  --regions $OSSS_REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$SCRIPTS/environment.py" \
  --text-count \
  --label "MC15C, 20.7, Data $YEAR" \
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  year=$YEAR \
  enable_systematics=False \
  luminosity=$LUMINOSITY


LUMINOSITY=7587.26 # 1/pb
YEAR=2016

## Plots with MC backgrounds only
#OUTPUT="results/plots_mc/$YEAR"
#"$OWLS/tools/plot.py" \
  #--output $OUTPUT \
  #--extensions $EXTENSIONS \
  #--model-file "$OWLS/definitions/models-v12.py" \
  #--model mc \
  #--regions-file "$OWLS/definitions/regions-v12.py" \
  #--regions $MC_REGIONS \
  #--distributions-file "$OWLS/definitions/distributions.py" \
  #--distributions $DISTRIBUTIONS \
  #--environment-file "$SCRIPTS/environment.py" \
  #--text-count \
  #--label "MC15C, 20.7, Data $YEAR" \
  #--error-label "Stat. Unc." \
  #data_prefix=$DATA_PREFIX \
  #year=$YEAR \
  #enable_systematics=False \
  #luminosity=$LUMINOSITY

# Plots with OS-SS backgrounds
OUTPUT="results/plots_osss_fakes/$YEAR"
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/definitions/models-v12.py" \
  --model osss_fakes2 \
  --regions-file "$OWLS/definitions/regions-v12.py" \
  --regions $OSSS_REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$SCRIPTS/environment.py" \
  --text-count \
  --label "MC15C, 20.7, Data $YEAR" \
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  year=$YEAR \
  enable_systematics=False \
  luminosity=$LUMINOSITY
