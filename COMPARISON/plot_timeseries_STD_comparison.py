# adjusted to plot more lines  from   plot_timeseries_STD.py
import pickle
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import sys
sys.path.append("/g100/home/userexternal/camadio0/CA_functions/")
from utils import UNITS
import numpy as np
from matplotlib.ticker import FormatStrFormatter
from commons.utils import addsep
from basins import V2 as OGS
import pandas as pd

VAR="chl" #else kd
OUTDIR    = '/g100_scratch/userexternal/camadio0/PPCON/VALIDAZIONE_RUNs/FIGURE/COMPARISON/'
LIST_RUN  = ['Hindcast','DA_SATFLOAT','DA_SATFLOAT_ppcon']
colors    = ['dodgerblue','orange','limegreen','gray','plum']
INDIR     = '/g100_scratch/userexternal/camadio0/PPCON/VALIDAZIONE_RUNs/FIGURE/'
SUFFIX    = '/SATELLITE//Fig4.3/export_data_ScMYValidation_plan_open_sea_STD_CORR.pkl'
LIST      = {}

LIST        = {name: pd.DataFrame() for name in LIST_RUN}
TIMES       = {name: pd.DataFrame() for name in LIST_RUN} 
MODEL_MEAN  = {name: pd.DataFrame() for name in LIST_RUN}
SAT___MEAN  = {name: pd.DataFrame() for name in LIST_RUN}
MODEL__STD  = {name: pd.DataFrame() for name in LIST_RUN}
SAT____STD  = {name: pd.DataFrame() for name in LIST_RUN}
CORR        = {name: pd.DataFrame() for name in LIST_RUN}

for III,RUN in enumerate(LIST_RUN):
    inputfile = INDIR + RUN + SUFFIX
    fid = open(inputfile,'rb')
    LIST[RUN] = pickle.load(fid)
    TIMES[RUN],_,_,MODEL_MEAN[RUN],SAT___MEAN[RUN],_,_,MODEL__STD[RUN],SAT____STD[RUN],CORR[RUN] = LIST[RUN]
    fid.close()

#TIMES,_,_,MODEL_MEAN,SAT___MEAN,_,_,MODEL__STD,SAT____STD,CORR = LIST[LIST_RUN[0]]
#TIMES1,_,_,MODEL_MEAN1,SAT___MEAN1,_,_,MODEL__STD1,SAT____STD1,CORR1 = LIST[LIST_RUN[1]]
#TIMES2,_,_,MODEL_MEAN2,SAT___MEAN2,_,_,MODEL__STD2,SAT____STD2,CORR2 = LIST[LIST_RUN[2]]

model_label =' MODEL'
var_label   = UNITS(VAR) 

print ("Time series of sub-basins are plotting .....")
for isub,sub in enumerate(OGS.P):
    if (sub.name == 'atl') : continue
    #print (sub.name)
    fig, ax = plt.subplots(figsize=(16 , 8))
    #ax.axvspan(31,119, ymin=0, ymax=0.6, alpha=0.5)
    #ax.axvspan(151,242, ymin=0, ymax=0.6, alpha=0.5)

    for III,RUN in enumerate(LIST_RUN):
        if III ==0:
           ax.plot(TIMES[RUN],SAT___MEAN[RUN][:,isub], color='grey', marker='o', label=' SAT', linewidth=0.1 ,alpha=0.8) 
        ax.plot(TIMES[RUN] ,MODEL_MEAN[RUN][:,isub],color=colors[III] , label=RUN , linewidth=2 ,alpha=0.8)

    ax.set_ylabel("%s - %s" %(sub.name.upper(), var_label  ) ).set_fontsize(22)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.legend(loc="best",labelspacing=0, handletextpad=0,borderpad=0.1)
    leg = plt.gca().get_legend()
    ltext  = leg.get_texts()
    plt.setp(ltext,fontsize=22)
    plt.rc('xtick', labelsize=22)
    plt.rc('ytick', labelsize=22)
    ax.tick_params(axis='both', labelsize=22)
    #pl.ylim(0.0, np.max(MODEL_MEAN[:,isub]+MODEL__STD[:,isub]) * 1.2 )
    plt.ylim(0.0, 0.6)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    dtFmt = mdates.DateFormatter('%m-%Y') # define the formatting
    #ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%Y"))
    plt.gca().xaxis.set_major_formatter(dtFmt)
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.grid(True)
    xlabels = ax.get_xticklabels()
    #pl.setp(xlabels, rotation=30)
    plt.xticks(rotation=90, fontweight='light',  fontsize=22)
    outfilename="%s%s_%s_STD.png"  %(OUTDIR, VAR, sub.name)
    plt.subplots_adjust(left=0.08,top = 0.95 ,bottom=0.2,  right=0.97)
    plt.title(VAR +  var_label +'  in ' + sub.name, fontsize=24)
    plt.savefig(outfilename)
    plt.close()

print(outfilename)


