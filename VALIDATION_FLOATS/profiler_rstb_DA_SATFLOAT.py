#!/usr/bin/env python
# Author: Giorgio Bolzon <gbolzon@ogs.trieste.it>
# Script to generate profiles of model files in
# the same time and locations where instruments
# such as bioFloats, mooring or vessels have been found.

# When imported, this scripts only defines settings for matchup generation.

from instruments.superfloat import FloatSelector
from instruments.matchup_manager import Matchup_Manager
from commons.time_interval import TimeInterval
from commons.Timelist import TimeList
from basins.region import Rectangle

RUN="/PPCON/DA_SATFLOAT"

INPUTDIR='/g100_scratch/userexternal/camadio0/' + RUN + '/wrkdir/POSTPROC/output/RST_BEFORE/TMP/'
# output directory, where aveScan.py will be run.
BASEDIR='/g100_scratch/userexternal/camadio0/' + RUN + '/wrkdir/PROFILATORE_FLOAT_RST_BEF_V9C/'

import os
if not os.path.exists(BASEDIR ):
    os.makedirs(BASEDIR)

DATESTART = '20190101'
DATE__END = '20200101'
modelprefix = 'RSTbefore.'

T_INT = TimeInterval(DATESTART,DATE__END, '%Y%m%d')
TL = TimeList.fromfilenames(T_INT, INPUTDIR,"*-13:00*.nc",filtervar="P_l",prefix=modelprefix)

ALL_PROFILES = FloatSelector(None,T_INT, Rectangle(-6,36,30,46))

vardescriptorfile='/g100_scratch/userexternal/camadio0/PPCON/VALIDAZIONE_RUNs/Validation/VALIDATION_FLOATS/Valid/VarDescriptorRST.xml'

#This previous part will be imported in matchups setup.
# The following part, the profiler, is executed once and for all.
# It might take some time, depending on length of simulation or size of files.
if __name__ == '__main__':
    # Here instruments time and positions are read as well as model times
    M = Matchup_Manager(ALL_PROFILES,TL,BASEDIR)

    profilerscript = BASEDIR + 'jobProfiler.sh'
    aggregatedir="/g100_scratch/userexternal/camadio0/PROVA/"
    M.writefiles_for_profiling(vardescriptorfile, profilerscript, aggregatedir=aggregatedir) # preparation of data for aveScan

    M.dumpModelProfiles(profilerscript) # sequential launch of aveScan
