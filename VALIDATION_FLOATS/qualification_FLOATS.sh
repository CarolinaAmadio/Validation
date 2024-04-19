#!/bin/bash

export ONLINE_REPO=/g100_work/OGS_devC/V9C/RUNS_SETUP/PREPROC/DA/
export MASKFILE=/g100_work/OGS_prodC/OPA/V10C/prod/wrkdir/analysis/2/MODEL/meshmask.nc
export PYTHONPATH=/g100_scratch/userexternal/camadio0/PPCON/bit.sea/ 

RUN=DA_SATFLOAT_ppcon/

mkdir $CINECA_SCRATCH/PPCON/VALIDAZIONE_RUNs/FIGURE/${RUN}
mkdir $CINECA_SCRATCH/PPCON/VALIDAZIONE_RUNs/FIGURE/${RUN}/FLOAT/
OUTDIR=$CINECA_SCRATCH/PPCON/VALIDAZIONE_RUNs/FIGURE/${RUN}/FLOAT/RST_BEFORE/
mkdir -p $OUTDIR

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
#python biofloats_ms_plotter_macro_seas.py -i $OUTDIR/float_bias_rmse_medianAE_Macro.nc -f $OUTFIGDIR -t $TABLE_DIR -y 1
echo python biofloats_ms_plotter_macro_seas.py -i $OUTDIR/float_bias_rmse_medianAE_Macro.nc -f $OUTFIGDIR -t $TABLE_DIR
#___________________________________________#

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



