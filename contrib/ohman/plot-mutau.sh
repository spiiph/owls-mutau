#!/bin/bash


# Plot many distributions for
# - OS Data vs MC
# - OS-SS


# Compute the path to the owls-taunu directory
CONTRIB=$(dirname "$0")
OWLS="$CONTRIB/../.."

MC_REGIONS="\
  mu_tau_os mu_tau_tau25_os \
  mu_tau_loose_os mu_tau_loose_tau25_os \
  mu_tau_gradient_os mu_tau_gradient_tau25_os \
  "

OSSS_REGIONS="\
  mu_tau mu_tau_tau25 \
  mu_tau_loose mu_tau_loose_tau25 \
  mu_tau_gradient mu_tau_gradient_tau25 \
  "

OSSS_SYST_REGIONS="\
  mu_tau_gradient mu_tau_gradient_tau25 \
  "

DISTRIBUTIONS="\
  tau_pt tau_eta tau_phi \
  tau_bdt_score tau_n_tracks \
  mu_pt mu_eta mu_phi \
  bjet_multiplicity jet_multiplicity \
  deta dphi dr \
  met_et met_phi mt \
  mu nvx \
  "
#EXTENSIONS="pdf eps"
EXTENSIONS="pdf"
LUMINOSITY=3209.0 # 1/pb
DATA_PREFIX="/disk/d1/ohman/tagprobe_2016-01-11_merged"


# Plots with only MC backgrounds, and split into MC processes
OUTPUT="results_mutau/plots_mc"
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/share/mutau/models.py" \
  --model mc \
  --regions-file "$OWLS/share/mutau/regions.py" \
  --regions $MC_REGIONS \
  --distributions-file "$OWLS/share/mutau/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$CONTRIB/environment.py" \
  --text-count \
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  enable_systematics=False \
  luminosity=$LUMINOSITY


# Plots with only MC backgrounds, and split into truth and fakes for ttbar
# and single top
OUTPUT="results_mutau/plots_mc_fakes"
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/share/mutau/models.py" \
  --model mc_fakes \
  --regions-file "$OWLS/share/mutau/regions.py" \
  --regions $MC_REGIONS\
  --distributions-file "$OWLS/share/mutau/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$CONTRIB/environment.py" \
  --text-count \
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  enable_systematics=False \
  luminosity=$LUMINOSITY

# Plots with OS-SS backgrounds, and split into truth and fakes for ttbar and
# single top
OUTPUT="results_mutau/plots_osss_fakes"
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/share/mutau/models.py" \
  --model osss_fakes \
  --regions-file "$OWLS/share/mutau/regions.py" \
  --regions $OSSS_REGIONS \
  --distributions-file "$OWLS/share/mutau/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$CONTRIB/environment.py" \
  --text-count \
  --error-label "Stat. Unc." \
  data_prefix=$DATA_PREFIX \
  enable_systematics=False \
  luminosity=$LUMINOSITY

# Plots with OS-SS backgrounds, and split into truth and fakes for ttbar and
# single top
OUTPUT="results_mutau/plots_osss_fakes_syst"
"$OWLS/tools/plot.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/share/mutau/models.py" \
  --model osss_fakes \
  --regions-file "$OWLS/share/mutau/regions.py" \
  --regions $OSSS_SYST_REGIONS \
  --distributions-file "$OWLS/share/mutau/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$CONTRIB/environment.py" \
  --text-count \
  --error-label "Stat. #otimes Sys. Unc." \
  data_prefix=$DATA_PREFIX \
  enable_systematics=True \
  luminosity=$LUMINOSITY
