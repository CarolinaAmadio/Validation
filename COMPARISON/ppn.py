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
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import matplotlib.colors as colors
from matplotlib.colors import BoundaryNorm
from commons.mask import Mask
from layer_integral import coastline


REF  , ref         = 'Hindcast'           , 'HIND'
REF  , ref         = 'DA_SAT'           , 'DA_sat'
run1 , run_1       = 'DA_SATFLOAT'        , 'DA_satfloat'
run2 , run_2       = 'DA_SATFLOAT_ppcon'  , 'DA_satfloat_ppcon'
INDIR= '/g100_scratch/userexternal/camadio0/PPCON/VALIDAZIONE_RUNs/FIGURE/'
PREX = '/SATELLITE/Fig4.7refScale/'
LIST_STAG = ['SUMMER' ,  'WINTER']
extfile= '_Map_ppn_Ave.201901-202001_Int0000-0200m-0200m_refScale_mgm2d.nc'
maskfile='/g100_work/OGS_devC/Benchmark/SETUP/PREPROC/MASK/meshmask.nc'
OUTDIR                 = INDIR + 'COMPARISON/'


TheMask=Mask(maskfile)

for III, stag in enumerate(LIST_STAG):
    nfile = (stag.lower()).capitalize()
    nc  = Dataset(INDIR+REF+'/'+PREX+stag+'/'+nfile+extfile   )
    nc1 = Dataset(INDIR+run1+'/'+PREX+stag+'/'+nfile+extfile   )
    nc2 = Dataset(INDIR+run2+'/'+PREX+stag+'/'+nfile+extfile   )
    ppn = nc.variables['ppn'][:]
    ppn1= nc1.variables['ppn'][:]
    ppn2= nc2.variables['ppn'][:]
    plt.close()
    # run1  - ref
    fig,ax = plt.subplots(figsize=(11,5))
    ax.set_position([0.08, 0.13, 0.78, 0.78])
    levels  =   MaxNLocator(nbins=50).tick_values(-50,+50) 
    levs = levels[::10]
    plt.grid(color='k', linestyle=':', linewidth=1) # horizontal lins
    cmap    =  plt.get_cmap('bwr')
    norm    =  BoundaryNorm(levels, ncolors=cmap.N, clip=True)
    CS=ax.contourf(TheMask.xlevels, TheMask.ylevels, ppn1-ppn  , cmap=cmap,norm=norm,  levels=levels,  extend="both")
    cbar=fig.colorbar(CS,ticks=levs, ax=ax)
    cbar.ax.tick_params(labelsize=16)
    ax.set_xlim([-6,36])
    ax.set_ylim([30,46])
    ax.set_xlabel('Lon').set_fontsize(18)
    ax.set_ylabel('Lat').set_fontsize(18)
    ax.tick_params(axis='x', labelsize=10)
    ax.text(-4,31.5, 'NPP' + ' [' +"mgC m$ ^{-2}$ d$^{-1}$"  + ']',horizontalalignment='left',verticalalignment='center',fontsize=16, color='black')
    ax.xaxis.set_ticks(np.arange(-2,36,6))
    ax.yaxis.set_ticks(np.arange(30,46,4))
    #Draw coastline
    clon,clat = coastline.get()
    ax.plot(clon,clat, color='#000000',linewidth=0.5)
    ax.tick_params(axis='both', which='major', labelsize=18)
    #title = "%s %s %s %s" % (RUN_ +':' , iseas + ' 2017-2018', 'NPP', layer.__repr__())
    plt.suptitle("Diff ppn "+ run1 +" vs "+ ref + '_' + stag, fontsize = 20)
    plt.subplots_adjust(left=0.08, top = 0.9,bottom=0.17, right=1.05)
    plt.savefig(OUTDIR +  'Diff_ppn_'+ run1 +'_vs_'+ ref + '_' + stag  +'.png')# , dpi=300)
    plt.close()
    
    # run2  - ref
    fig,ax = plt.subplots(figsize=(11,5))
    ax.set_position([0.08, 0.13, 0.78, 0.78])
    levels  =   MaxNLocator(nbins=50).tick_values(-50,np.nanmax(50))
    levs = levels[::10]
    plt.grid(color='k', linestyle=':', linewidth=1) # horizontal lins
    cmap    =  plt.get_cmap('bwr')
    norm    =  BoundaryNorm(levels, ncolors=cmap.N, clip=True)
    CS=ax.contourf(TheMask.xlevels, TheMask.ylevels, ppn2-ppn  , cmap=cmap,norm=norm,  levels=levels,  extend="both")
    cbar=fig.colorbar(CS,ticks=levs, ax=ax)
    cbar.ax.tick_params(labelsize=16)
    ax.set_xlim([-6,36])
    ax.set_ylim([30,46])
    ax.set_xlabel('Lon').set_fontsize(18)
    ax.set_ylabel('Lat').set_fontsize(18)
    ax.tick_params(axis='x', labelsize=10)
    ax.text(-4,31.5, 'NPP' + ' [' +"mgC m$ ^{-2}$ d$^{-1}$"  + ']',horizontalalignment='left',verticalalignment='center',fontsize=16, color='black')
    ax.xaxis.set_ticks(np.arange(-2,36,6))
    ax.yaxis.set_ticks(np.arange(30,46,4))
    #Draw coastline
    ax.plot(clon,clat, color='#000000',linewidth=0.5)
    ax.set_xlim([-6, 36])
    ax.set_ylim([30, 46])
    ax.tick_params(axis='both', which='major', labelsize=18)
    #title = "%s %s %s %s" % (RUN_ +':' , iseas + ' 2017-2018', 'NPP', layer.__repr__())
    plt.suptitle("Diff ppn "+ run2 +" vs "+ ref +  '_' + stag , fontsize = 20)
    plt.subplots_adjust(left=0.08, top = 0.9,bottom=0.17, right=1.05)
    plt.savefig(OUTDIR +  'Diff_ppn_'+run2+'_vs_'+ ref + '_' + stag  +'.png') #, dpi=300)

    # run1 run2
    fig,ax = plt.subplots(figsize=(11,5))
    ax.set_position([0.08, 0.13, 0.78, 0.78])
    levels  =   MaxNLocator(nbins=50).tick_values(-20,+20)
    levs = levels[::10]
    plt.grid(color='k', linestyle=':', linewidth=1) # horizontal lins
    cmap    =  plt.get_cmap('bwr')
    norm    =  BoundaryNorm(levels, ncolors=cmap.N, clip=True)
    CS=ax.contourf(TheMask.xlevels, TheMask.ylevels, ppn2-ppn1  , cmap=cmap,norm=norm,  levels=levels,  extend="both")
    cbar=fig.colorbar(CS,ticks=levs, ax=ax)
    cbar.ax.tick_params(labelsize=16)
    ax.set_xlim([-6,36])
    ax.set_ylim([30,46])
    ax.set_xlabel('Lon').set_fontsize(18)
    ax.set_ylabel('Lat').set_fontsize(18)
    ax.tick_params(axis='x', labelsize=10)
    ax.text(-4,31.5, 'NPP' + ' [' +"mgC m$ ^{-2}$ d$^{-1}$"  + ']',horizontalalignment='left',verticalalignment='center',fontsize=16, color='black')
    ax.xaxis.set_ticks(np.arange(-2,36,6))
    ax.yaxis.set_ticks(np.arange(30,46,4))
    #Draw coastline
    clon,clat = coastline.get()
    ax.plot(clon,clat, color='#000000',linewidth=0.5)
    ax.tick_params(axis='both', which='major', labelsize=18)
    #title = "%s %s %s %s" % (RUN_ +':' , iseas + ' 2017-2018', 'NPP', layer.__repr__())
    plt.suptitle("Diff ppn "+ run2  +" vs "+ run1 +  '_' + stag, fontsize = 20)
    plt.subplots_adjust(left=0.08, top = 0.9,bottom=0.17, right=1.05)
    plt.savefig(OUTDIR +  'Diff_ppn_'+run2+'_vs_'+ run1 + '_' + stag  +'.png')# , dpi=300)
    plt.close()
    
