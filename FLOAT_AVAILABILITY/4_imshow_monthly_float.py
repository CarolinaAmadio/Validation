import pandas as pd
import numpy as np
import os

import warnings
warnings.filterwarnings('ignore')
import sys
sys.path.append("/g100/home/userexternal/camadio0/CA_functions/")
from basins_CA import plot_map_subbasins,sorted_basin
from commons_ import List_month
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

NAMEVAR  = 'N3n'
LIST_RUN = ['DA_SATFLOAT','DA_SATFLOAT_ppcon']
list_run = ['DA_SATFLOAT','PPCon']
DATADIR  = '/g100_scratch/userexternal/camadio0/PPCON/VALIDAZIONE_RUNs/FIGURE/'
SUFFIX   = '/AVAILABILITY_floats/'
MESI,mesi = List_month()
#sorter= [ 'alb', 'swm1', 'swm2','nwm','tyr1', 'tyr2', 'ion1','adr1','adr2','ion2','ion3', 'lev1','lev2','lev3','lev4','aeg']
sorted_basin_list=sorted_basin()

# creo df vuoto con indice nom bacini
INDEX, border =  plot_map_subbasins()
#df1   = pd.DataFrame(index=sorted_basin_list, columns= mesi)
df1   = pd.DataFrame(index=np.arange(1,13), columns = sorted_basin_list)

for RUN , run in zip(LIST_RUN, list_run):
    OUTDIR = DATADIR + RUN + SUFFIX +'/'
    df1 = pd.DataFrame(index=np.arange(1,13), columns = sorted_basin_list)
    print(RUN , run)
    SAVENAME='Complete_Float_assimilated_'+ RUN +'_'+ NAMEVAR
    df      = pd.read_csv(DATADIR + RUN + SUFFIX + 'Complete_Float_assimilated_'+ run +'_'+ NAMEVAR +'.csv', index_col=0)
    df2     = df[[ 'month','Basin']] 
    df2['tot'] = 1
    tmp = df2.groupby(by=['month','Basin' ]).sum()
    tmp.reset_index(inplace=True)
    for III in range(0,len(tmp)):
        serv=tmp.iloc[III,:]
        df1[serv.Basin].iloc[serv.month-1] = serv.tot
    df1 = df1.fillna(0)
    fig, ax = plt.subplots(figsize=(14, 12))
    cmap = colors.ListedColormap(['snow', 'springgreen',  'gold'])
    bounds=[-1, 1, 10,1000]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    img = plt.imshow(df1.to_numpy().astype('float'), origin='lower',cmap=cmap, norm=norm)

    #plt.colorbar(img, cmap=cmap, norm=norm, boundaries=bounds, ticks=bounds)
    ax = plt.gca();
    # Major ticks
    ax.set_yticks(range(len(df1)))
    ax.set_xticks(range(df1.shape[1]))
    # Labels for major ticks
    ax.set_yticklabels(MESI,fontsize=22)
    ax.set_xticklabels(df1.columns ,fontsize=22,rotation=90 )
    # Minor ticks
    ax.set_xticks(np.arange(-.5, df1.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-.5, df1.shape[0], 1), minor=True)
    #ax.grid(which='minor', color='gainsboro', linestyle='-', linewidth=2)
    ax.grid(which='minor', color='k', linestyle='-', linewidth=2)
    for i in range(len(df1.index)):
       for j in range(len(df1.columns)):
           if df1.iloc[i, j] == 0:
              pass
           else:
              text = ax.text(j, i, df1.iloc[i, j],
              ha="center", va="center", color="dimgray", fontsize=15)

    plt.title('Monthly BGC-float availabiliy per sub-basins \n' + NAMEVAR + ' run: ' + RUN , fontsize=24 )
    plt.subplots_adjust(left=0.1,top = 0.94 ,bottom=0.15,  right=0.97)
    plt.savefig( OUTDIR + 'Monthly_BGC_float_availabiliy_subbasins_'+NAMEVAR+'.png')
    plt.close()
    print(df1)
    df1.to_csv(OUTDIR + 'Monthly_BGC_float_availabiliy_subbasins_'+NAMEVAR+'.csv')
    if run == 'DA_SATFLOAT':
        import copy
        dfr=df1.copy()

#
# plot diff runs 
diff_ = df1-dfr
fig, ax = plt.subplots(figsize=(14, 12))
cmap = colors.ListedColormap(['snow', 'dodgerblue',  'red'])
bounds=[-1, 1, 10,1000]
norm = colors.BoundaryNorm(bounds, cmap.N)
img = plt.imshow(diff_.to_numpy().astype('float'), origin='lower',cmap=cmap, norm=norm)
ax = plt.gca();
ax.set_yticks(range(len(diff_)))
ax.set_xticks(range(diff_.shape[1]))
# Labels for major ticks
ax.set_yticklabels(MESI,fontsize=22)
ax.set_xticklabels(diff_.columns ,fontsize=22,rotation=90 )
# Minor ticks
ax.set_xticks(np.arange(-.5, diff_.shape[1], 1), minor=True)
ax.set_yticks(np.arange(-.5, diff_.shape[0], 1), minor=True)
#ax.grid(which='minor', color='gainsboro', linestyle='-', linewidth=2)
ax.grid(which='minor', color='k', linestyle='-', linewidth=2)
for i in range(len(diff_.index)):
   for j in range(len(diff_.columns)):
       if diff_.iloc[i, j] == 0:
          pass
       else:
          text = ax.text(j, i, diff_.iloc[i, j],
          ha="center", va="center", color="white", fontsize=22, weight='bold')

plt.title('diff BGC-float availabiliy per sub-basins \n' + NAMEVAR  ,fontsize=24 )
plt.subplots_adjust(left=0.1,top = 0.94 ,bottom=0.15,  right=0.97)
COMPARISON='/g100_scratch/userexternal/camadio0/PPCON/VALIDAZIONE_RUNs/FIGURE/COMPARISON/'
plt.savefig(  COMPARISON + 'diff_BGC_float_availabiliy_subbasins_'+NAMEVAR+'.png')
plt.close()
print(diff_)
diff_.to_csv( COMPARISON + 'diff_BGC_float_availabiliy_subbasins_'+NAMEVAR+'.csv')


#
