#!/usr/bin/env sh

# Compute the path to the owls-mutau directory
SCRIPTS=$(dirname "$0")
OWLS="$SCRIPTS/.."

#EXTENSIONS="pdf eps"
EXTENSIONS="pdf"

REGIONS="\
  mu_tau \
  mu_tau_1p \
  mu_tau_3p \
  mu_tau_tau25 \
  mu_tau_tau25_1p \
  mu_tau_tau25_3p \
  "
REGIONS=" \
  mu_tau \
  mu_tau_tau25 \
  "
#REGIONS="mu_tau"

DISTRIBUTIONS="tau_pt"

LUMINOSITY=3193.68 # 1/pb
DATA_PREFIX="/disk/d2/ohman/lhtnp_v12_merged"
YEAR=2015
OUTPUT="results/systematics/$YEAR"

#"$OWLS/tools/plot-syst-variation.py" \
  #--output $OUTPUT \
  #--extensions $EXTENSIONS \
  #--model-file "$OWLS/definitions/models-v12.py" \
  #--model osss_sub \
  #--regions-file "$OWLS/definitions/regions-v12.py" \
  #--regions $REGIONS \
  #--distributions-file "$OWLS/definitions/distributions.py" \
  #--distributions $DISTRIBUTIONS \
  #--environment-file "$SCRIPTS/environment.py" \
  #--label "Bkg MC (OS-SS) + SS Data" \
  #-- \
  #data_prefix=$DATA_PREFIX \
  #year=$YEAR

LUMINOSITY=5115.35 # 1/pb
DATA_PREFIX="/disk/d2/ohman/lhtnp_v12_merged"
YEAR=2016
OUTPUT="results/systematics/$YEAR"

"$OWLS/tools/plot-syst-variation.py" \
  --output $OUTPUT \
  --extensions $EXTENSIONS \
  --model-file "$OWLS/definitions/models-v12.py" \
  --model osss_sub \
  --regions-file "$OWLS/definitions/regions-v12.py" \
  --regions $REGIONS \
  --distributions-file "$OWLS/definitions/distributions.py" \
  --distributions $DISTRIBUTIONS \
  --environment-file "$SCRIPTS/environment.py" \
  --label "Bkg MC (OS-SS) + SS Data" \
  -- \
  data_prefix=$DATA_PREFIX \
  year=$YEAR
