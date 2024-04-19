import pandas as pd
import numpy as np
import os

import warnings
warnings.filterwarnings('ignore')
import sys
sys.path.append("/g100/home/userexternal/camadio0/CA_functions/")
from basins_CA import plot_map_subbasins

NAMEVAR  = 'N3n'
list_run = ['DA_SATFLOAT','PPCon']
LIST_RUN = ['DA_SATFLOAT','PPCon']
WINT = [2,3,4]
SUMM = [6,7,8]

summer_list = ['sum_' + x for x in  LIST_RUN if isinstance(x, str)]
winter_list = ['win_' + x for x in  LIST_RUN if isinstance(x, str)]


# creo df vuoto con indice nom bacini
INDEX, border = a,b = plot_map_subbasins()
df1   = pd.DataFrame(index=INDEX, columns= list_run)
dfw   = pd.DataFrame(index=INDEX, columns= winter_list)
dfs   = pd.DataFrame(index=INDEX, columns= summer_list)

for RUN , run in zip(LIST_RUN, list_run):
    print(RUN , run)
    SAVENAME='Complete_Float_assimilated_'+ RUN +'_'+ NAMEVAR
    df      = pd.read_csv('Complete_Float_assimilated_'+ RUN +'_'+ NAMEVAR +'.csv', index_col=0)
    for isub, sub in enumerate(INDEX):
       tmp  = df[df.Basin == sub]
       tmpw = tmp[tmp['month'].isin(WINT)]
       tmps = tmp[tmp['month'].isin(SUMM)]
       df1.loc[sub][run] = len(tmp)
       dfw.loc[sub]['win_' + run] = len(tmpw)
       dfs.loc[sub]['sum_' + run] = len(tmps)

dftot =  pd.concat([df1, dfw, dfs], axis=1)
df1=dftot

import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import matplotlib as mpl
from matplotlib import cm as color_map
import matplotlib as mpl
from mpl_toolkits.basemap import Basemap

# sort index west-->east 
sorter= [ 'alb', 'swm1', 'swm2','nwm','tyr1', 'tyr2', 'ion1','adr1','adr2','ion2','ion3', 'lev1','lev2','lev3','lev4','aeg']
sorterIndex = dict(zip(sorter, range(len(sorter))))
# Generate a rank column that will be used to sort
# the dataframe numerically
df1['serv'] = df1.index
df1['serv_Rank'] = df1['serv'].map(sorterIndex)
df1 = df1.sort_values(by='serv_Rank')
df1 = df1.iloc[:,0:6]

#tolgo win and sum to total
df1['spr_aut_' + list_run[0] ] = df1[list_run[0]] - df1[winter_list[0]] - df1[summer_list[0]]
df1['spr_aut_' + list_run[1] ] = df1[list_run[1]] - df1[winter_list[1]] - df1[summer_list[1]]


LISTCOL = [ 'spr_aut_' + list_run[0],  winter_list[0], summer_list[0], 
          'spr_aut_' + list_run[1]  ,  winter_list[1], summer_list[1] ] 
df1 = df1[LISTCOL]
colors = ['silver', 'cyan','gold','gray','dodgerblue','orange']
ax = df1.iloc[:,:].plot.bar(figsize=(14,8), stacked=True, color=colors, edgecolor='k' ,fontsize=20,rot=90, alpha=0.6)
plt.grid(axis='y',linestyle=':', linewidth=0.5, color='k')
plt.title('Seasonal distribution of nitrate and reconstructed nitrate' ,fontsize=24)
plt.axvline(5.5,color='black', linewidth=1)
# add texture
bars = ax.patches
hatches = ''.join(h*len(df1) for h in '   ///')
for bar, hatch in zip(bars, hatches):
    bar.set_hatch(hatch)

plt.text(1.,415, 'West',horizontalalignment='left',verticalalignment='center',fontsize=24, color='black')
plt.text(10,415, 'East',horizontalalignment='left',verticalalignment='center',fontsize=24, color='black')
plt.xlabel('Mediterranean Sub-basins',fontsize=22)
plt.ylabel('N. Profiles', fontsize=22)
#ax.legend(fontsize=16)
plt.legend(loc='upper center', bbox_to_anchor=(.5, -0.31),  fancybox=False, shadow=False, ncol=2, fontsize=18)

plt.subplots_adjust(left=0.09, hspace= 0.3,  wspace=0.13, top= 0.91, bottom=0.35, right=0.99)
#plt.savefig('BGC_Float_seasonal_availability_.png',dpi=300)
plt.savefig('BGC_Float_seasonal_availability_.png')


