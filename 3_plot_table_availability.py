import pandas as pd
import numpy as np
import os

import warnings
warnings.filterwarnings('ignore')
import sys
sys.path.append("/g100/home/userexternal/camadio0/CA_functions/")
from basins_CA import plot_map_subbasins

#RUN, run    = 'IN_SITU_2017_2018'  , 'DAfl'
#RUN, run  = 'SYNTHETIC_2017_2018'  , 'DAnn'

#LIST_RUN = ['IN_SITU_2017_2018','SYNTHETIC_2017_2018']
#list_run = ['DAfl', 'DAnn']


RUN, run     = 'PPCon' , 'PPCon'
NAMEVAR  = 'N3n'

WINT = [2,3,4]
SUMM = [6,7,8]

# creo df vuoto con indice nom bacini
INDEX, border = a,b = plot_map_subbasins()
df1   = pd.DataFrame(index=INDEX, columns= ['Insitu','NNrec'])
dfw   = pd.DataFrame(index=INDEX, columns= ['w_ins','w_rec'])
dfs   = pd.DataFrame(index=INDEX, columns= ['s_ins','s_rec'])

for RUN , run in zip(LIST_RUN, list_run):
    print(RUN , run)
    SAVENAME='Complete_Float_assimilated_'+ RUN +'_'+ NAMEVAR
    df      = pd.read_csv('Complete_Float_assimilated_'+ RUN +'_'+ NAMEVAR +'.csv', index_col=0)
    for isub, sub in enumerate(INDEX):
       tmp  = df[df.Basin == sub]
       tmpw = tmp[tmp['month'].isin(WINT)]
       tmps = tmp[tmp['month'].isin(SUMM)]
       df1.loc[sub][run] = len(tmp)
       dfw.loc[sub][run+'_win'] = len(tmpw)
       dfs.loc[sub][run+'_sum'] = len(tmps)

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
#df1['DAnn'] = df1.DAnn - df1.DAfl
#df1.columns=['Nitrate', 'Rec.Nitrate']

df1['DAnn']= df1.DAnn - df1.DAfl
df1['DAnn_win']= df1.DAnn_win - df1.DAfl_win
df1['DAnn_sum']= df1.DAnn_sum - df1.DAfl_sum

df1['DAnn'] = df1.DAnn - df1.DAnn_win - df1.DAnn_sum
df1['DAfl'] = df1.DAfl - df1.DAfl_win - df1.DAfl_sum 

LISTCOL = ['DAfl', 'DAfl_win','DAfl_sum' , 'DAnn'   , 'DAnn_win'  , 'DAnn_sum' ]
df1 = df1[LISTCOL]
df1.columns= ['NO3' ,  'NO3_win','NO3_sum'  , 'recNO3' , 'recNO3_win', 'recNO3_sum']


colors = ['silver', 'cyan','gold','gray','dodgerblue','orange']
ax = df1.iloc[:,:].plot.bar(figsize=(14,5.5), stacked=True, color=colors, edgecolor='k' ,fontsize=20,rot=90, alpha=0.6)
#df1.columns= ['Nitr.','Nitr.Win','NitrSum','recNitr.','RecNitrWin','RecNitrSum']
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
plt.subplots_adjust(left=0.09, hspace= 0.3,  wspace=0.13, top= 0.91, bottom=0.25, right=0.99)
plt.xlabel('Mediterranean Sub-basins',fontsize=22)
plt.ylabel('N. Profiles', fontsize=22)
#plt.show()
#plt.legend(df1.columns,fontsize=16 )
plt.legend(fontsize=16)
plt.savefig('BGC_Float_availability_.png',dpi=300)
#plt.savefig('BGC_Float_availability_.png')


"""
#fig,ax = plt.subplots()
#ax1 = df1.plot(kind='bar',figsize=(14,5) ,stacked=True, width=0.85, edgecolor='w',  color=['tab:blue','orangered'],fontsize=20,rot=90)
#colors    = ['gray','silver','dodgerblue','lightskyblue','orange','gold']
#colors = ['dodgerblue','lightskyblue','orange','gold']

#ax = df1.iloc[:,0:2].plot(figsize=(14,5), stacked=True, color=colors[0:2], linewidth= 3, style=['.-','-'] , fontsize=20,rot=90, alpha=0.2)
#df1.iloc[:,0:2].plot(kind='area',figsize=(14,5) ,stacked=True, color=['gray','silver'] ,fontsize=20,rot=90, alpha=0.6)
#df1.iloc[:,2:].plot(kind='bar',figsize=(14,5) ,stacked=True, width=0.9, edgecolor='k', color=colors ,fontsize=20,rot=90, alpha=0.6)

#fig,ax = plt.subplots(figsize=(14,5) )
#df1[['DAfl', 'DAnn']].plot.bar(stacked=True, width=0.85, position=0, color=['gray','silver'], ax=ax, alpha=0.6)
#df1[['DAfl_win', 'DAnn_win', 'DAfl_sum', 'DAnn_sum']].plot.bar(stacked=True, width=0.85,position=4 , color=colors[3:], ax=ax, alpha=0.6)
#df1[['DAfl_sum', 'DAnn_sum']].plot.bar(stacked=True, width=0.85,  color=['orange','gold'] , ax=ax, alpha=0.1)
"""
