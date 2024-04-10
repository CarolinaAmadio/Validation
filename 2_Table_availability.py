# it create a csv of assimilated float with more info metadata

import pandas as pd
import numpy as np
import os

import warnings
warnings.filterwarnings('ignore')
import sys
sys.path.append("/g100/home/userexternal/camadio0/CA_functions/")
from commons_ import col_to_dt

#RUN, run    = 'IN_SITU_2017_2018'  , 'insitu'
#RUN, run    = 'SYNTHETIC_2017_2018'  , 'syn'
RUN, run     = 'PPCon' , 'PPCon'

VARLIST  = ['N3n','P_l','O2o']
NAMEVAR  = 'N3n'
LIST_COL =  ['lon','lat','DATE','NAME']

ADD_FREQ_FLOAT=True

dfc  = pd.read_csv('Float_assimilated_'+ RUN   +'.csv', index_col=0)
if NAMEVAR  == 'N3n':
   df1  = pd.read_csv('Float_assimilated_'+ RUN  +'_N3nqc.csv', index_col=0)
   if 'Qc' in df1.columns:
       LIST_COL.append('qc')
   df1.columns= LIST_COL

SAVENAME='Complete_Float_assimilated_'+ RUN +'_'+ NAMEVAR 

strings=dfc.columns
LIST_sliced_df = [string for string in strings if NAMEVAR in string]
dfc=dfc[LIST_sliced_df]
dfc.dropna(how='all', inplace=True)
LIST_COL =  ['lon','lat','DATE','NAME']
dfc.columns = LIST_COL

ncol='DATE'
dfc=col_to_dt(dfc, ncol)
dfc['month'] = dfc.date.dt.month
dfc['year']  = dfc.date.dt.year
dfc = dfc.sort_values(by=['NAME','date'])

if ADD_FREQ_FLOAT: 
 dfc['Time_diff_'+NAMEVAR ] = np.nan   
 LIST=[]
 for WMO in dfc.NAME:
    serv = dfc[dfc.NAME==WMO]
    a    = serv.date.diff().dt.days
    dfc.loc[dfc["NAME" ] == WMO, 'Time_diff_'+NAMEVAR ] = a.values
from commons_ import col_to_basin
from commons_ import West_or_East
dfc ['West'] = 0
dfc ['East'] = 0
dfc = col_to_basin(dfc)
for III in range(0,len(dfc)):
    tmp =  dfc.iloc[III,:]
    if West_or_East(tmp.Basin) == 'East':
       dfc.East.iloc[III] =1
    else:
       dfc.West.iloc[III] =1

dfc['qc'] = np.nan
dfc.NAME = dfc.NAME.astype(int)
df1.NAME = df1.NAME.astype(int)


for III in range (0,len(df1)):
    tmp= df1.iloc[III,:]
    dfc['qc'] = np.where((dfc.lon == tmp.lon  )  & (dfc.lat == tmp.lat  )  & (dfc.NAME == tmp.NAME  ) , tmp.qc, dfc.qc  )

dfc.sort_index(ascending=True)
dfc.to_csv( SAVENAME + '.csv')

