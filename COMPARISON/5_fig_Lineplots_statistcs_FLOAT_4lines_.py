import pandas as pd
import numpy as np 
import sys
sys.path.append("/g100/home/userexternal/camadio0/CA_functions/")
import funzioni_CA
from funzioni_CA import parsing_path
from funzioni_CA import new_directory
from commons.utils import addsep
from utils import UNITS
from utils import cmp_for_maps
import matplotlib.pyplot as plt
from matplotlib import cm as color_map
import matplotlib as mpl
import sys

LINEWI=4

class SIM():
   def __init__(self, NAME='HC'):
      self.name =NAME
   def Extract_data_SIM(self , INDIR, RUN, PATH_TABLE, STATISTIC, VARNAME, SEAS):
      endstr='/'
      parsing_path(INDIR, endstr)
      parsing_path(RUN, endstr)
      INPUT      = INDIR +  RUN + VALIDATION_INSTRUMENT  + '/RST_BEFORE/'+ PATH_TABLE
      parsing_path(INPUT, endstr)
      df         = pd.read_csv(INPUT +SEAS+'_'+ VARNAME + '_' + STATISTIC + '.txt',  sep='\t', index_col=0)
      df.columns =  [c.replace(" ", "") for c in list(df.columns)]

      return (df , self.name)

INDIR                  = '/g100_scratch/userexternal/camadio0/PPCON/VALIDAZIONE_RUNs/FIGURE/'
OUTDIR                 = INDIR + 'COMPARISON/' 
VALIDATION_INSTRUMENT  = 'FLOAT'
PATH_TABLE             = 'Floats_bias_rmse_tables_Macro_seas/'
REF  , ref             = 'Hindcast/'           , 'HIND'
RUN1 , run_1           = 'DA_SATFLOAT/'        , 'SATFLOAT'
RUN2 , run_2           = 'DA_SATFLOAT_ppcon/'  , 'PPcon'
RUN3 , run_3           = 'DA_SAT/'              , 'SAT'

LISTA_RUN = [ref , run_1 , run_2 , run_3 ]
colors=['dodgerblue','orange','limegreen', 'plum']

N_sims = len(LISTA_RUN)
LIST_STATISTICS = ['RMSE']
parsing_path(INDIR,'/' )
parsing_path(OUTDIR,'/' )
new_directory(OUTDIR)
VARLIST=['P_l','N3n','O2o']
#VARLIST=['N3n']
#SEASON = ['Winter_FMA']
z = np.array([5,20,45 ,80,125,175,450 ])
SEASON = ['Winter_FMA','Summer_JJA']

savename = ""
for nrun in LISTA_RUN:
    savename+= '_'+nrun

for SEAS in SEASON:
 for STATISTIC in LIST_STATISTICS:
    OUTDIR1 = (OUTDIR +  '/')
    parsing_path(OUTDIR1,'/' )
    new_directory(OUTDIR1) 
    for VARNAME in VARLIST:
       VARUNITS = UNITS(VARNAME)
       print(VARNAME)
       ref1                 =  SIM(REF)
       dfref, ref_name      =  ref1.Extract_data_SIM( INDIR  ,  REF    , PATH_TABLE ,STATISTIC, VARNAME ,SEAS)
       # run 1 run 2
       sim1, sim2           =  SIM(RUN1) , SIM(RUN2) 
       dfsim1 , sim1_name   =  sim1.Extract_data_SIM( INDIR ,  RUN1   , PATH_TABLE ,STATISTIC, VARNAME ,SEAS)
       dfsim2 , sim2_name   =  sim2.Extract_data_SIM( INDIR ,  RUN2   , PATH_TABLE ,STATISTIC, VARNAME ,SEAS)
       
       sim3                 =   SIM(RUN3)
       dfsim3 , sim3_name   =  sim3.Extract_data_SIM( INDIR ,  RUN3   , PATH_TABLE ,STATISTIC, VARNAME ,SEAS)

       # REF  removing cols with nan
       dfref            = dfref.apply(pd.to_numeric, errors='coerce')
       dfref.dropna(how='all', inplace= True)
       dfref.dropna(axis=1, how='all', inplace= True)
       # RUN 1 RUN 2 
       dfsim1 ,dfsim2 = dfsim1.apply(pd.to_numeric, errors='coerce') , dfsim2.apply(pd.to_numeric, errors='coerce')
       dfsim1.dropna(how='all', inplace= True) , dfsim2.dropna(how='all', inplace= True)
       dfsim1.dropna(axis=1, how='all', inplace= True) , dfsim2.dropna(axis=1, how='all', inplace= True)
       
       dfsim3         = dfsim3.apply(pd.to_numeric, errors='coerce')
       dfsim3.dropna(how='all', inplace= True)
       dfsim3.dropna(axis=1, how='all', inplace= True)
       
       LIST_COL = dfsim1.T.columns
       import matplotlib as mpl
       import matplotlib.pyplot as plt
       from pylab import *
       fig, axs = plt.subplots(1,dfsim1.shape[0], figsize=(9, 6),sharex=True, sharey=True ,facecolor='w', edgecolor='k')
       for III in range(0,len(LIST_COL)):
          namestat = LIST_COL[III].replace(' ', '')
          if STATISTIC=='BIAS' :
             axs[III].axvline(0, color='dimgrey', lw=1.)
          if VARNAME=='P_l':
             axs[III].plot(np.array(dfsim2.T.iloc[0:-1,III]), -z[0:-1],  color=colors[2], linestyle='solid', linewidth=LINEWI ,
                      alpha=0.5 , label = 'DAnn' + colors[2][0:2] )
             axs[III].plot(np.array(dfref.T.iloc[0:-1,III]) , -z[0:-1], color=colors[0] , linestyle='solid', linewidth=LINEWI ,
                      alpha=0.5 , label = 'HIND_' + colors[0][0:2]  )
             axs[III].plot(np.array(dfsim1.T.iloc[0:-1,III]),  -z[0:-1], color=colors[1], linestyle='dashed',linewidth=LINEWI ,
                      alpha=0.7 , label = 'DAfl_'  + colors[1][0:2] )         
             axs[III].plot(np.array(dfsim3.T.iloc[0:-1,III]),  -z[0:-1], color=colors[3], linestyle='dashed', linewidth=LINEWI,
                      alpha=0.7 , label = 'DAsat_'+ colors[3][0:2])
          else:

             axs[III].plot(np.array(dfsim2.T.iloc[:,III]), -z,  color=colors[2] ,  linestyle='solid', linewidth=LINEWI,
                      alpha=0.5 , label = 'DAnn')
             axs[III].plot(np.array(dfref.T.iloc[:,III]) , -z, color=colors[0]  ,  linestyle='solid', linewidth=LINEWI,
                      alpha=0.5 , label = 'HIND' )
             axs[III].plot(np.array(dfsim1.T.iloc[:,III]),  -z, color=colors[1]  , linestyle='dashed', linewidth=LINEWI,
                      alpha=0.7 , label = 'DAfl') 
             axs[III].plot(np.array(dfsim3.T.iloc[:,III]) , -z, color=colors[3]  , linestyle='dashed', linewidth=LINEWI,
                      alpha=0.7 , label = 'DAsat' )


          axs[III].grid( linestyle=':', linewidth=0.5, color='k' )       
          axs[III].set_title(namestat.capitalize(), fontweight="bold", fontsize=18 )
          if VARNAME =='P_l': 
             axs[III].xaxis.set_tick_params(labelsize=20, rotation=90)
          else:
             axs[III].xaxis.set_tick_params(labelsize=20, rotation=90)
          axs[III].yaxis.set_tick_params(labelsize=22)

       title_seas = SEAS.replace('_','_(')
       title_seas = title_seas + ')'
       title_seas = title_seas.replace('_(',' (')
       if VARNAME== 'P_l':
          if STATISTIC=='RMSE':
             plt.xlim(0, 0.4)
             plt.suptitle( title_seas  +' Chlorophyll \n', fontsize=20)
       if VARNAME== 'N3n':
          plt.suptitle(title_seas  + ' Nitrate \n'   , fontsize=20) 
       if VARNAME== 'O2o':
          plt.xlim(0, 27) 
          plt.suptitle(title_seas  + ' Oxygen \n', fontsize=20)
          
       if dfsim1.shape[0] <= 3:
          box = axs[1].get_position()
          axs[1].set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
       else:    
          box = axs[3].get_position()
          axs[3].set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
       
       fig.text(0.025, 0.5,  'Depth (m)',fontsize=20 , ha='center', va='center', rotation='vertical')
       fig.text(0.5, 0.05, VARUNITS , ha='center', va='center', fontsize=20)

       plt.subplots_adjust(top= 0.85, bottom=0.2, left=0.15,right=0.98, wspace=0.3)
       plt.savefig(OUTDIR1 + STATISTIC + '_profiles_'+ SEAS+'_' + savename +'_' +VARNAME+ '_dpi300.png' ,dpi=300)
       print(OUTDIR1+  STATISTIC + '_profiles_'+ SEAS+'_' + savename +'_' +VARNAME+ '.png')
       plt.close()
    del (OUTDIR1)


import numpy as np
import matplotlib.pyplot as plt

colors=['dodgerblue','orange','limegreen', 'plum']
lines   =  ['-','-','--','--']
alpha   =  [0.5,0.5,0.7,0.7]
#f = lambda m,c,l,a: plt.plot([],[],marker=m, color=c, ls=l, alpha=a )[0]
#handles = [f(markers[i], colors[i], lines[i],alpha[i] ) for i in range(3)]

handles = [ (colors[i], lines[i],alpha[i] ) for i in range(4)]
labels =  ['HIND','SATFLOAT','PPcon','DA_SAT']
legend = plt.legend( handles,labels, ncol=len(colors))

def export_legend(legend, filename="legend.png", expand=[-8,-8,8,8]):
    fig  = legend.figure
    fig.canvas.draw()
    bbox  = legend.get_window_extent()
    bbox = bbox.from_extents(*(bbox.extents + np.array(expand)))
    bbox = bbox.transformed(fig.dpi_scale_trans.inverted())
    fig.savefig(filename, dpi=300, bbox_inches=bbox)

export_legend(legend)
