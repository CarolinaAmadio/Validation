import matplotlib
import numpy as np
from scipy.io import netcdf_file as NC
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
import sys
sys.path.append("/g100/home/userexternal/camadio0/CA_functions/")
from funzioni_CA import plot_heatmax
from basins_CA import plot_map_subbasins
from commons.layer import Layer
from commons_ import List_month

LIST_RUNS = ['DA_SATFLOAT/', 'DA_SATFLOAT_ppcon/']
run_names = "ppcon vs satfloat" 

LIST_STAT = ['RMSE', 'Bias']
INDIR     = "/g100_scratch/userexternal/camadio0/PPCON/VALIDAZIONE_RUNs/FIGURE/"
SUFFIX    = "FLOAT/RST_BEFORE/Floats_bias_rmse_tables_16Subs_Monthly/"

OUT_TABLEDIR='/g100_scratch/userexternal/camadio0/PPCON/VALIDAZIONE_RUNs/FIGURE/COMPARISON/FLOAT/'

VARLIST   = ['P_l','N3n','O2o']
VARLONGNAMES=['Chlorophyll','Nitrate','Oxygen']
LAYERLIST=[Layer(0,10), Layer(10,30), Layer(30,60), Layer(60,100), Layer(100,150), Layer(150,300), Layer(300,600)]

INDIR_RUN0= INDIR + LIST_RUNS[0] + SUFFIX
INDIR_RUN1= INDIR + LIST_RUNS[1] + SUFFIX

basins_list , _ = plot_map_subbasins()
MESI, mm        = List_month()
sorter= [ 'alb', 'swm1', 'swm2','nwm','tyr1', 'tyr2', 'ion1','adr1','adr2','ion2','ion3', 'lev1','lev2','lev3','lev4','aeg']

sorterIndex = dict(zip(sorter, range(len(sorter))))


for ivar, var in enumerate(VARLIST):
    for STAT in LIST_STAT:
        for Layer in LAYERLIST:
            df  = pd.read_csv( INDIR_RUN0 +  STAT + '_' + var + '_' + Layer.string()  + '.txt' , sep='\t' , index_col=0 )
            df1 = pd.read_csv( INDIR_RUN1 +  STAT + '_' + var + '_' + Layer.string()  + '.txt' , sep='\t' , index_col=0 )

            df = df.fillna(0)
            df1= df1.fillna(0)

            df = df.apply(pd.to_numeric, errors='coerce')
            df1= df1.apply(pd.to_numeric, errors='coerce')
            diff_df = (df1-df)
            #print( diff_df.max().max() )
            diff_df = diff_df.iloc[:,0:-1]
            diff_df['serv']=diff_df.index
            diff_df['serv_Rank'] = diff_df['serv'].map(sorterIndex)
            diff_df = diff_df.sort_values(by='serv_Rank')
            diff_df = diff_df.iloc[:,0:-2]
            diff_df = diff_df.fillna(0) 
            diff_df = diff_df.round(3)
       
            stat = diff_df.to_numpy().astype('float')
            cmap = colors.ListedColormap(['snow', 'gold',  'coral'])
            plt.close()
            fig, ax = plt.subplots(figsize=(14, 12))
            levmaxmin= max(abs(np.nanmin(stat)),abs(np.nanmax(stat) ) )*0.75 
            cmap = colors.ListedColormap(['blue','paleturquoise', 'snow',  'orange', 'red'])
            bounds=[ -levmaxmin, -levmaxmin*0.25   ,  -levmaxmin*0.05 , levmaxmin*0.05  , levmaxmin*0.25   , +levmaxmin  ]
            bounds.sort()
            bounds= np.array(bounds).round(3)
            #fig, ax = plot_heatmax(fig, ax, stat.T, bounds,MESI,basins_list,cmap)
            norm = colors.BoundaryNorm(bounds, cmap.N)
            img = plt.imshow(stat.T , origin='lower',cmap=cmap, norm=norm)
            cbar = plt.colorbar(img, cmap=cmap, norm=norm, boundaries=bounds, ticks=bounds )
            cbar.ax.tick_params(labelsize=20)
            ax = plt.gca();
            ax.set_yticks(range(len(MESI)))
            ax.set_xticks(range(len(basins_list   )))
            # Labels for major ticks
            ax.set_yticklabels( MESI,fontsize=22)
            ax.set_xticklabels(  basins_list,fontsize=22,rotation=90 )
            # Minor ticks
            ax.set_xticks(np.arange(-.5, stat.shape[0], 1), minor=True)
            ax.set_yticks(np.arange(-.5, stat.shape[1], 1), minor=True)
            ax.grid(which='minor', color='gainsboro', linestyle='-', linewidth=2)
            ax.grid(which='minor', color='k', linestyle='-', linewidth=2)
            for i in range(len(diff_df.index)):
                for j in range(len(diff_df.columns)):
                    if diff_df.iloc[i, j] == 0:
                       pass
                    else:
                       text = ax.text(i, j, np.around(diff_df.iloc[i, j],3) ,
                       ha="center", va="center", color="dimgray", fontsize=9)
            plt.title('Diff Monthly ' + run_names + ' '  + STAT +' in '+ var + '\n ' +  Layer.longname(), fontsize=24 )
            plt.subplots_adjust(left=0.1,top = 0.94 ,bottom=0.15,  right=0.9)
            plt.savefig( OUT_TABLEDIR + 'Monthly_'+  run_names.replace(' ' , '_') + STAT +'_'+var+'_'+Layer.longname()+ '.png')
            plt.close()



import shutil
shutil.copy('biofloats_rmse_comparison.py' , OUT_TABLEDIR + '/'  )
