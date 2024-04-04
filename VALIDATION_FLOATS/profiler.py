#export /g100_work/OGS_devC/V9C/RUNS_SETUP/PREPROC/DA/SUPERFLOAT


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
# location of input big ave files, usually the TMP directory.
# ave files are supposed to have N3n, O2o and chl

RUN="/PPCON/DA_SATFLOAT_ppcon"
INPUTDIR="/g100_scratch/userexternal/camadio0/" + RUN + "/wrkdir/POSTPROC/output/AVE_FREQ_1/TMP"
# output directory, where aveScan.py will be run.
BASEDIR='/g100_scratch/userexternal/camadio0/' + RUN + '/wrkdir/PROFILATORE_FLOAT_AVE/'

print(INPUTDIR)
print(INPUTDIR)
print(INPUTDIR)

import os
if not os.path.exists(BASEDIR ):
    os.makedirs(BASEDIR)


DATESTART = '20190101'
DATE__END = '20200101'

T_INT = TimeInterval(DATESTART,DATE__END, '%Y%m%d')
TL = TimeList.fromfilenames(T_INT, INPUTDIR,"ave*.nc",filtervar="P_l")
ALL_PROFILES = FloatSelector(None,T_INT, Rectangle(-6,36,30,46))

vardescriptorfile='/g100_scratch/userexternal/camadio0/' + RUN + '/wrkdir/Valid/VarDescriptor.xml'
print (vardescriptorfile)

#This previous part will be imported in matchups setup.
# The following part, the profiler, is executed once and for all.
# It might take some time, depending on length of simulation or size of files.
if __name__ == '__main__':
    # Here instruments time and positions are read as well as model times
    M = Matchup_Manager(ALL_PROFILES,TL,BASEDIR)
    profilerscript = BASEDIR + 'jobProfiler.sh'
    aggregatedir="/g100_scratch/userexternal/camadio0/PROVA/"    #INPUTDIR
    M.writefiles_for_profiling(vardescriptorfile, profilerscript, aggregatedir=aggregatedir) # preparation of data for aveScan
    M.dumpModelProfiles(profilerscript) # sequential launch of aveScan
