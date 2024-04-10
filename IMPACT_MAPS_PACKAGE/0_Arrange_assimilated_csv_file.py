import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

""" this script arrange the assimilation csv obtained in 
    /g100/home/userexternal/camadio0/Time_Series_plot/OUTPUT_PSEUDOCAL_2017_2018/./0_mapfloats_assimilated.py
    prende i misfit chech nella $RUN/wrkdir/DA/ e fa il files dei floats ASSIMILATI
    NON LAVOTO SU EXPORT DELL ONLINE REPO CON Profilelist

    Output: Un file csv per variabile:
    Float_assimilated_ VARNAME $RUN   .csv
"""

#RUN, run  = 'Multivariate_2017_2018' , 'Multi'
#RUN, run  = 'PSEUDO_2017_2018_CAL', 'PCAL'
#RUN, run  = 'IN_SITU_2017_2018'  , 'insitu'
#RUN ,run  = 'SYNTHETIC_2017_2018'  , 'syn'
RUN ,run    = 'PPCon','PPCon'


VARLIST     =  ['N3n','P_l','O2o']
df1         =  pd.read_csv('Float_assimilated_'+ run +'.csv', index_col=0)
COLUMN_LIST =  ['ID', 'time', 'lat', 'lon', 'name']


for varname in VARLIST:
    filter_col = [col for col in df1 if col.startswith(varname)]
    dfvar = df1[filter_col]
    dfvar.dropna(inplace=True)

    dfvar.columns = ['lon','lat','time','name']
    dfvar["ID"] =   dfvar['name'] 
    dfvar[sorted(COLUMN_LIST )]
    print('Float_assimilated_'+ run + '_' + varname + '.csv')
    dfvar.to_csv('Float_assimilated_'+ run + '_' + varname + '.csv')




