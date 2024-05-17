#!/bin/bash

export ONLINE_REPO=/g100_work/OGS_devC/V9C/RUNS_SETUP/PREPROC/DA/
export MASKFILE=/g100_work/OGS_prodC/OPA/V10C/prod/wrkdir/analysis/2/MODEL/meshmask.nc
export PYTHONPATH=/g100_scratch/userexternal/camadio0/PPCON/bit.sea/

RUN=DA_SAT/


#!/bin/bash


if [ "$RUN" = "DA_SAT/" ]; then
   BASEDIR=/g100_scratch/userexternal/camadio0/PPCON/$RUN/wrkdir/PROFILATORE_FLOAT_AVE
elif [ "$RUN" = "Hindcast/" ]; then
   BASEDIR=/g100_scratch/userexternal/camadio0/PPCON/$RUN/wrkdir/PROFILATORE_FLOAT_AVE 
else
   BASEDIR=/g100_scratch/userexternal/camadio0/PPCON/$RUN/wrkdir/PROFILATORE_FLOAT_RST_BEF_V9C
fi

OUTDIR_RST=$CINECA_SCRATCH/PPCON/VALIDAZIONE_RUNs/FIGURE/${RUN}/FLOAT/RST_BEFORE/

echo "::::::::::::::::::::::::::::::::::"
echo $RUN 
echo $BASEDIR
echo $OUTDIR_RST


# BIOFLOATS SECTION: Hovmoeller plots, wmo trajectories and statistics per basin
# RST BEFORE
#BASEDIR=/g100_scratch/userexternal/camadio0/$RUN/wrkdir/PROFILATORE_FLOAT_RST_BEF_V9C
#OUTDIR_RST=$CINECA_SCRATCH/FLOAT_ELAB_DAFloat/QuIDeval/$RUN/FLOAT/RST_BEFORE



OUT44=$OUTDIR_RST/Fig4.4
NCDIR=$OUT44/tmp_nc
mkdir -p $OUT44 $NCDIR

#python SingleFloat_vs_Model_Stat_Timeseries.py -m $MASKFILE -b $BASEDIR -o $NCDIR
python Hov_Stat_plot.py -m $MASKFILE -i $NCDIR -o $OUT44 -b $BASEDIR


#OUT44=$OUTDIR_RST/Fig4.4_zoom
#mkdir -p $OUT44
#python Hov_Stat_plot_ZOOM.py -m $MASKFILE -i $NCDIR -o $OUT44 -b $BASEDIR

#cp qualification_Hos_stat.sh $OUTDIR_RST 
#cp *py $OUTDIR_RST
