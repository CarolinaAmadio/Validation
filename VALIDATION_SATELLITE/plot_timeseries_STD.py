import argparse
def argument():
    parser = argparse.ArgumentParser(description = '''
    Plot timeseries for QUID.
    Reference doc: CMEMS-Med-QUID-006-008-V2-V1.0.docx
    Usually Figure IV.2
    ''',
    formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(   '--outdir', '-o',
                            type = str,
                            required =True,
                            default = "./",
                            help = ''' Output image dir'''
                            )
    parser.add_argument(   '--inputfile', '-i',
                            type = str,
                            required = True,
                            help = 'Input pickle file for open sea')
    parser.add_argument(   '--var', '-v',
                                type = str,
                                required = True,
                                choices = ['chl','kd'],
                                help = ''' model var name'''
                                )
    

    return parser.parse_args()

args = argument()

import pickle
import matplotlib.pyplot as pl
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import sys
import numpy as np
from matplotlib.ticker import FormatStrFormatter
from commons.utils import addsep
from basins import V2 as OGS

OUTDIR=addsep(args.outdir)
fid = open(args.inputfile,'rb')
LIST = pickle.load(fid)
fid.close()

TIMES,_,_,MODEL_MEAN,SAT___MEAN,_,_,MODEL__STD,SAT____STD,CORR = LIST

model_label=' MODEL'

if (args.var =="chl"):
    var_label = "CHL [mg/m$^3$]"
else:
    var_label = "KD [m$^{-1}$]"

print ("Time series of sub-basins are plotting .....")
for isub,sub in enumerate(OGS.P):
    if (sub.name == 'atl') : continue
    #print (sub.name)
    fig, ax = pl.subplots(figsize=(16 , 8))
    ax.fill_between(TIMES,SAT___MEAN[:,isub]-SAT____STD[:,isub],SAT___MEAN[:,isub]+SAT____STD[:,isub],color='palegreen', alpha=0.5)
    ax.plot(TIMES,SAT___MEAN[:,isub]-SAT____STD[:,isub] ,'lightgreen', linewidth=0.5)
    ax.plot(TIMES,SAT___MEAN[:,isub]+SAT____STD[:,isub] ,'lightgreen', linewidth=0.5)
    ax.plot(TIMES,SAT___MEAN[:,isub],'og',label=' SAT', linewidth=2 ,alpha=0.8)

    ax.fill_between(TIMES,MODEL_MEAN[:,isub]-MODEL__STD[:,isub],MODEL_MEAN[:,isub]+MODEL__STD[:,isub], color='silver', alpha=0.2)
    ax.plot(TIMES,MODEL_MEAN[:,isub]-MODEL__STD[:,isub],'dimgray', linewidth=0.5 )
    ax.plot(TIMES,MODEL_MEAN[:,isub]+MODEL__STD[:,isub],'dimgray', linewidth=0.5 )
    ax.plot(TIMES,MODEL_MEAN[:,isub],'-k',label=model_label, linewidth=2 ,alpha=0.8)

    ax.set_ylabel("%s - %s" %(sub.name.upper(), var_label  ) ).set_fontsize(22)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.legend(loc="best",labelspacing=0, handletextpad=0,borderpad=0.1)
    leg = pl.gca().get_legend()
    ltext  = leg.get_texts()
    pl.setp(ltext,fontsize=22)
    pl.rc('xtick', labelsize=22)
    pl.rc('ytick', labelsize=22)
    ax.tick_params(axis='both', labelsize=22)
    pl.ylim(0.0, np.max(MODEL_MEAN[:,isub]+MODEL__STD[:,isub]) * 1.2 )
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    dtFmt = mdates.DateFormatter('%m-%Y') # define the formatting
    #ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%Y"))
    pl.gca().xaxis.set_major_formatter(dtFmt)
    pl.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.grid(True)
    xlabels = ax.get_xticklabels()
    #pl.setp(xlabels, rotation=30)
    plt.xticks(rotation=90, fontweight='light',  fontsize=22)
    outfilename="%s%s_%s_STD.png"  %(OUTDIR, args.var, sub.name)
    pl.subplots_adjust(left=0.08,top = 0.95 ,bottom=0.2,  right=0.97)
    pl.savefig(outfilename)
