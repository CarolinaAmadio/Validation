#!/bin/bash

export MASKFILE=/g100_work/OGS_devC/Benchmark/SETUP/PREPROC/MASK/meshmask.nc
export PYTHONPATH=/g100_scratch/userexternal/camadio0/PPCON/bit.sea/ #/g100/home/userexternal/camadio0/bit.sea_py3/

#inputs 
RUN=DA_SATFLOAT_ppcon/
MODELDIR=$CINECA_SCRATCH/PPCON/DA_SATFLOAT_ppcon/wrkdir
VALIDATION_DIR=/g100_scratch/userexternal/camadio0/PPCON/VALIDAZIONE_RUNs/
SAT_WEEKLY_DIR=/g100_work/OGS_devC/Benchmark/SETUP/POSTPROC/SAT/CHL/WEEKLY_4_24/
INPUTDIR=${MODELDIR}/MODEL/AVE_FREQ_1/
INPUT_AGGR_DIR=${MODELDIR}/POSTPROC/output/AVE_FREQ_1/TMP/

OUTDIR=/g100_scratch/userexternal/camadio0/PPCON/VALIDAZIONE_RUNs/FIGURE/${RUN}/SATELLITE/
mkdir -p $VALIDATION_DIR ${VALIDATION_DIR}/FIGURE/ ${VALIDATION_DIR}/FIGURE//${RUN} $OUTDIR

# SATELLITE output in RUN/SATELLITE or COMPARISON

# figura 4.3 satellite
OUTFIG=$OUTDIR/Fig4.3/
mkdir -p $OUTFIG/offshore $OUTFIG/coast

# 1.   oooooooooooooooooooooooooooooooooooooooooooooooooooooooooo#
# Calcola files e li salva in pkl
echo python ScMYvalidation_plan.py -s $SAT_WEEKLY_DIR -i $INPUT_AGGR_DIR -m $MASKFILE -c open_sea -o $OUTFIG/export_data_ScMYValidation_plan_open_sea_STD_CORR.pkl -l 10 -v chl
# end  oooooooooooooooooooooooooooooooooooooooooooooooooooooooooo#

exit 0

#  2.  oooooooooooooooooooooooooooooooooooooooooooooooooooooooooo#
# creo i files csv per poi fare i barplots (un csv per run) OPEN SEA
OUTBARPLOT=BARPLOT/
mkdir -p $OUTBARPLOT
#python plot_timeseries_RMS_CORR.py -i $OUTFIG/export_data_ScMYValidation_plan_open_sea_STD_CORR.pkl -o $OUTBARPLOT -r $RUN
# end  oooooooooooooooooooooooooooooooooooooooooooooooooooo#

#  3.  oooooooooooooooooooooooooooooooooooooooooooooooooooooooooo#
#fig 4.7refScale  CREATE MAP PPN INTEGRAL 0-200m
mkdir -p $OUTDIR/Fig4.7refScale/
#echo python averager_and_plot_map_ppn_refScale.py -i $INPUT_AGGR_DIR  -v ppn  -t integral -m $MASKFILE -o $OUTDIR/Fig4.7refScale/ -l Plotlist_bio.xml -s 20170101 -e 20190101
# end  oooooooooooooooooooooooooooooooooooooooooooooooooooo#

# winter e summer richiede il file di assimilazione Float_assimilated_v9c.csv creato in home timeseries
STAGIONE=SUMMER
mkdir -p $OUTDIR/Fig4.7refScale/$STAGIONE
python averager_and_plot_map_ppn_refScale_seas_FMA_JJA.py -i $INPUT_AGGR_DIR  -v ppn  -t integral -m $MASKFILE -o $OUTDIR/Fig4.7refScale/$STAGIONE -l Plotlist_bio.xml -s 20170101 -e 20190101 -seas $STAGIONE

STAGIONE=WINTER
mkdir -p $OUTDIR/Fig4.7refScale/$STAGIONE
python averager_and_plot_map_ppn_refScale_seas_FMA_JJA.py -i $INPUT_AGGR_DIR  -v ppn  -t integral -m $MASKFILE -o $OUTDIR/Fig4.7refScale/$STAGIONE -l Plotlist_bio.xml -s 20170101 -e 20190101 -seas $STAGIONE














