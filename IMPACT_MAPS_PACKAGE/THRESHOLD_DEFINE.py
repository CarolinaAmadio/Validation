import numpy as np
import sys
sys.path.append("/g100/home/userexternal/camadio0/CA_functions/")

import pandas as pd

run='IN_SITU_2017_2018/'
run1='SYNTHETIC_2017_2018/'
OUTDIR='/g100_scratch/userexternal/camadio0/COMBINING_DA_NN/REVISIONE_SCRIPTS/IMPACT_MAPS_PACKAGE/'
STAGIONE=['Winter','Summer']
varlist=['N3n', 'P_l']

df = pd.DataFrame ()
for varname in varlist:   
    for iseas in STAGIONE:
        run_95  = pd.read_csv (OUTDIR+ run + 'insitu_final_95_'  + iseas  + '_' + varname + '.csv' , index_col=0 )
        run1_95 = pd.read_csv (OUTDIR+ run1+ 'syn_final_95_'    + iseas  + '_' + varname + '.csv' , index_col=0 )
        frames = [ run_95, run1_95]
        result = pd.concat(frames)
        print( iseas )
        print(varname)
        print(' median ' + str(np.nanmedian((np.array(result)).flatten())) )
        print(' mean ' + str(np.nanmean((np.array(result)).flatten())))
        if varname == 'P_l':
            THRES  = 0.3     # 0.4 
        if varname == 'N3n':
            THRES   = 0.07   # 0.1
        # run insitu
        arr = np.array(run_95)
        arr = arr.flatten()
        arr = arr[~np.isnan(arr)]
        size_SEA=arr.size
        size_FILTER = len(arr[arr> THRES])   
        print (run) 
        print(100*(size_FILTER/size_SEA ))
        arr = np.array(run1_95)
        arr = arr.flatten()
        arr = arr[~np.isnan(arr)]
        size_SEA=arr.size
        size_FILTER = len(arr[arr> THRES])
        print (run1)
        print(100*(size_FILTER/size_SEA ))
        print('______________     \n') 

#Thres_N3n = 0.1 --> 0.07
#Thres_P_l = 0.3 --> 0.02
#Thres_O2o = 0.03
