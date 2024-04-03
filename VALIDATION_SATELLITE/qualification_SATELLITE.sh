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

# 1.   Calcola files e li salva in pkl figura 4.3 satellite quid
#OUTFIG=$OUTDIR/Fig4.3/
#mkdir -p $OUTFIG
# python ScMYvalidation_plan.py -s $SAT_WEEKLY_DIR -i $INPUT_AGGR_DIR -m $MASKFILE -c open_sea -o $OUTFIG/export_data_ScMYValidation_plan_open_sea_STD_CORR.pkl -l 10 -v chl
# 1. end # 

#  2. creo i files csv per poi fare i barplots (un csv per run) OPEN SEA
#mkdir -p $OUTDIR/BARPLOT/
#python plot_timeseries_RMS_CORR.py -i $OUTFIG/export_data_ScMYValidation_plan_open_sea_STD_CORR.pkl -o $OUTDIR/BARPLOT/ -r $RUN
# 2. end #


#  3. fig 4.7refScale  CREATE MAP PPN INTEGRAL 0-200m #
mkdir -p $OUTDIR/Fig4.7refScale/

# seasonal generic without contour 
DATESTART=20190101
DATEEND=20200101

STAGIONE=WINTER
mkdir -p $OUTDIR/Fig4.7refScale/$STAGIONE
#python averager_and_plot_map_ppn_refScale_seas_FMA_JJA.py -i $INPUT_AGGR_DIR  -v ppn  -t integral -m $MASKFILE -o $OUTDIR/Fig4.7refScale/$STAGIONE -l Plotlist_bio.xml -s $DATESTART -e $DATEEND -seas $STAGIONE -run $RUN

STAGIONE=SUMMER
mkdir -p $OUTDIR/Fig4.7refScale/$STAGIONE
#python averager_and_plot_map_ppn_refScale_seas_FMA_JJA.py -i $INPUT_AGGR_DIR  -v ppn  -t integral -m $MASKFILE -o $OUTDIR/Fig4.7refScale/$STAGIONE -l Plotlist_bio.xml -s $DATESTART -e $DATEEND -seas $STAGIONE -run $RUN

# several versions
#averager_and_plot_map_ppn_refScale_seas_FMA_JJA_original.py
#averager_and_plot_map_ppn_refScale_seas_FMA_JJA_withtableold.py
#averager_and_plot_map_ppn_refScale_seas_FMA_JJA_with_table.py
# 3. end #

#  4. fig quid time series 4.2 solo open sea #
mkdir -p  $OUTDIR/Fig4.2/
echo $OUTDIR/Fig4.2/

echo python plot_timeseries_STD.py -v chl -i $OUTDIR/Fig4.3/export_data_ScMYValidation_plan_open_sea_STD_CORR.pkl -o $OUTDIR/Fig4.2/
