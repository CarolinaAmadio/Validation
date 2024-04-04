#!/bin/bash

export ONLINE_REPO=/g100_work/OGS_devC/V9C/RUNS_SETUP/PREPROC/DA/
export MASKFILE=/g100_scratch/userexternal/camadio0/meshmask_24.nc
export PYTHONPATH=/g100/home/userexternal/camadio0/bit.sea_py3/
#RUN=SYNTHETIC_2017_2018
#RUN=hindcast_2017_2018
RUN=IN_SITU_2017_2018

echo $RUN
echo $ONLINE_REPO

OUTDIR=$CINECA_SCRATCH/FLOAT_ELAB_DAFloat/QuIDeval/$RUN/FLOAT/RST_BEFORE/
#OUTDIR=$CINECA_SCRATCH/FLOAT_ELAB_DAFloat/QuIDeval/$RUN/FLOAT/AVE_DAILY/
mkdir -p $CINECA_SCRATCH/FLOAT_ELAB_DAFloat/QuIDeval/
mkdir -p $CINECA_SCRATCH/FLOAT_ELAB_DAFloat/QuIDeval/$RUN/
mkdir -p $CINECA_SCRATCH/FLOAT_ELAB_DAFloat/QuIDeval/$RUN/FLOAT/ 
mkdir -p $OUTDIR

#profiler_HIND.py

#___________________________________________#
# STATISTICS PER ogs.nrt 6 MACRO  basins  --> ANNUALI
#___________________________________________#

OUTFIGDIR=$OUTDIR/Floats_bias_rmse_Timeseries_Macro_yrly
TABLE_DIR=$OUTDIR/Floats_bias_rmse_tables_Macro_yrly

mkdir -p $OUTFIGDIR $TABLE_DIR
#python biofloats_ms_Macro.py -m $MASKFILE -o $OUTDIR/float_bias_rmse_medianAE_Macro.nc
#python biofloats_ms_plotter_Macro_yrly.py -i $OUTDIR/float_bias_rmse_medianAE_Macro.nc -f $OUTFIGDIR -t $TABLE_DIR


#___________________________________________#
# STATISTICS PER ogs.nrt 6 MACRO basins  --> stagionali
OUTFIGDIR=$OUTDIR/Floats_bias_rmse_Timeseries_Macro_seas/
TABLE_DIR=$OUTDIR/Floats_bias_rmse_tables_Macro_seas/
mkdir -p $OUTFIGDIR $TABLE_DIR
echo python biofloats_ms_plotter_macro_seas.py -i $OUTDIR/float_bias_rmse_medianAE_Macro.nc -f $OUTFIGDIR -t $TABLE_DIR

#___________________________________________#


exit 0

# soooootttoooobaaaciiinnniiiii
#     STATISTICS PER SELECTED SUBBASIN  --> ANNUALI    
# (in the scripts specificati)
#___________________________________________#
OUTFIGDIR=$OUTDIR/Floats_bias_rmse_Timeseries_selected_yrly
TABLE_DIR=$OUTDIR/Floats_bias_rmse_tables_selected_yrly
mkdir -p $OUTFIGDIR $TABLE_DIR
python biofloats_ms_Selected.py -m $MASKFILE -o $OUTDIR/float_bias_rmse_medianAE_selected_seas.nc


#___________________________________________#
#     STATISTICS PER SELECTED SUBBASIN  -->  stagionali
# (in the scripts specificati)
#___________________________________________#

OUTFIGDIR=$OUTDIR/Floats_bias_rmse_Timeseries_selected_seas
TABLE_DIR=$OUTDIR/Floats_bias_rmse_tables_selected_seas
mkdir -p $OUTFIGDIR $TABLE_DIR
python biofloats_ms_plotter_selected_seas.py -i $OUTDIR/float_bias_rmse_medianAE_selected_seas.nc -f $OUTFIGDIR  -t $TABLE_DIR



