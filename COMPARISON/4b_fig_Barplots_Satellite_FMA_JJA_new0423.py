import pandas as pd
import numpy as np
import sys
sys.path.append("/g100/home/userexternal/camadio0/CA_functions/")
import funzioni_CA
from commons.utils import addsep
from utils import UNITS
from basins import V2 as OGS
import matplotlib.pyplot as plt
import matplotlib as mpl
from pylab import *

REF  , ref         = 'HC'                 , 'HIND'
run1 , run_1       = 'DA_SATFLOAT'        , 'DAfl'
run2 , run_2       = 'DA_SATFLOAT_ppcon'  , 'ppcon'

#INDIR     = '/g100_scratch/userexternal/camadio0/VALIDAZIONE_RUN_CMEMS_scripts/VALIDAZIONE_SATELLITE/BARPLOT/'

LISTA_RUN = [ref , run_1 , run_2 ]

colors = ['dodgerblue','orange','limegreen','gray','plum']

dfsim1 = pd.read_csv ( REF    + '_FMA_JJA_table4.1_chla.csv' , index_col=0)
dfsim2 = pd.read_csv ( run1   + '_FMA_JJA_table4.1_chla.csv' , index_col=0)
dfsim3 = pd.read_csv ( run2   + '_FMA_JJA_table4.1_chla.csv' , index_col=0)

iVAR       = 'P_l'
VARUNITS   = UNITS(iVAR)
BASIN_LIST = []

for isub,sub in enumerate(OGS.P):
    BASIN_LIST.append(sub.name)

LIST_STAG = ['FMA','JJA'] 
#LIST_STAG = ['RMSEwin','RMSEsum']

# primo dataset_:  winter --> df
df = pd.DataFrame(index= BASIN_LIST, columns= LISTA_RUN )
df[LISTA_RUN[0]] , df[LISTA_RUN[1]] , df[LISTA_RUN[2]] = np.array( dfsim1.RMS_MA) , np.array( dfsim2.RMS_MA) , np.array(dfsim3.RMS_MA)
df = df.iloc[:-2,:]
 
# secondo summer     --> dfs
dfs =  pd.DataFrame(index= BASIN_LIST, columns= LISTA_RUN )
dfs[LISTA_RUN[0]] , dfs[LISTA_RUN[1]] , dfs[LISTA_RUN[2]] = np.array( dfsim1.RMS_JJ) , np.array( dfsim2.RMS_JJ) , np.array(dfsim3.RMS_JJ)
dfs = dfs.iloc[:-2,:]

fig, axs = plt.subplots(figsize=(18,6),nrows=1, ncols=1)
#st = axes_style("whitegrid")

axsw  = df.plot(ax = axs, kind='bar', width=1., edgecolor='w'  ,color= colors, grid=False,alpha=0.7  ,fontsize=20,rot=90,legend=False )
#axss = dfs.plot(ax = axs[1], kind='bar', width=1., edgecolor='w'  ,color= colors, grid=False,alpha=0.7  ,fontsize=20,rot=90,legend=False )

# add texture
bars = axsw.patches
#hatches = ''.join(h*len(df) for h in '/.-')
hatches = ''.join(h*len(df) for h in '  .')
for bar, hatch in zip(bars, hatches):
    bar.set_hatch(hatch)

#bars = axss.patches
#hatches = ''.join(h*len(df) for h in '  .')
#for bar, hatch in zip(bars, hatches):
#    bar.set_hatch(hatch)

#box = axs[1].get_position()
#axs[1].set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
#axs[1].legend(loc='upper center', bbox_to_anchor=(-.15, -0.2),  fancybox=False, shadow=False, ncol=5, fontsize=18)

axs.set_title('Winter (FMA) RMSE', fontweight="bold", fontsize=16  )
#axs[1].set_title('Summer (JJA) RMSE', fontweight="bold", fontsize=16  )

axs.xaxis.set_tick_params(labelsize=18, rotation=45)
#axs[1].xaxis.set_tick_params(labelsize=18, rotation=45)
axs.yaxis.set_tick_params(labelsize=18)
#axs[1].yaxis.set_tick_params(labelsize=18)

fig.text(0.015, 0.58,  'Chlorophyll RMSE ' + VARUNITS  ,  fontsize=16 , ha='center', va='center', rotation='vertical')

savename = ""
for nrun in LISTA_RUN:
    savename+= '_'+nrun    

plt.subplots_adjust(left=0.06, hspace= 0.0,  wspace=0.09, top= 0.91, bottom=0.25, right=0.99)
plt.savefig('4_fig_RMSE__chla_SAT_HC_win' + savename + '_FMA_JJA_dpi300.png')
#plt.savefig('4_fig_RMSE__chla_SAT_HC_sum' + savename + '_FMA_JJA_dpi300.png')

plt.close()

import sys
sys.exit()

