import argparse
from numpy import dtype
def argument():
    parser = argparse.ArgumentParser(description = '''
    A unit conversion is performed, about ppn.
    ''',
    formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(   '--outdir', '-o',
                            type = str,
                            required =True,
                            default = "./",
                            help = ''' Output dir'''
                            )

    parser.add_argument(   '--inputdir', '-i',
                            type = str,
                            required = True,
                            default = './',
                            help = 'Input dir')

    parser.add_argument(   '--varname', '-v',
                                type = str,
                                required = True,
                                default = '',
                                choices = ['P_l','P_i','N1p', 'N3n', 'O2o', 'pCO2','PH','pH','ppn','P_c','Ac','DIC'] )
    parser.add_argument(   '--plotlistfile', '-l',
                                type = str,
                                required = True,
                                help = '''Plotlist_bio.xml"
                                ''')
    parser.add_argument(   '--maskfile', '-m',
                                type = str,
                                required = True,
                                help = 'Path of the mask file')
    parser.add_argument(   '--optype', '-t',
                                type = str,
                                required = True,
                                default = '',
                                choices = ['integral','mean'],
                                help ="  INTEGRALE:  * heigth of the layer, MEDIA    :  average of layer")
    parser.add_argument(   '--starttime','-s',
                                type = str,
                                required = True,
                                help = 'start date in yyyymmdd format')
    parser.add_argument(   '--endtime','-e',
                                type = str,
                                required = True,
                                help = 'start date in yyyymmdd format')      
    parser.add_argument(   '--iseas','-seas',
                                type = str,
                                required = True,
                                help = 'seas = Winter or Summmer No others')
    parser.add_argument(   '--run_name','-run',
                                type = str,
                                required = True,
                                help = 'run es "HIND"')


    return parser.parse_args()
args = argument()

import numpy as np
import matplotlib.pyplot as pl
from commons.time_interval import TimeInterval
from commons.Timelist import TimeList
from commons.mask import Mask
from commons.layer import Layer
from layer_integral.mapbuilder import MapBuilder, Plot
from commons.dataextractor import DataExtractor
from commons.time_averagers import TimeAverager3D
from layer_integral import coastline
import commons.timerequestors as requestors
from commons.utils import addsep
from commons.xml_module import *
from xml.dom import minidom
from commons import netcdf3
import pandas as pd
import sys
import matplotlib.colors as colors
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
sys.path.append("/g100/home/userexternal/camadio0/CA_functions/")
from mpl_toolkits.basemap import Basemap
import warnings
warnings.filterwarnings('ignore')
from netCDF4 import Dataset
from matplotlib import gridspec


class Seasons():
      def __init__ (self, name):
          self.name = name

          if name.capitalize() in 'Winter' and len(name) >2:
             self.code = 0
             self.ST_CODE =  ['2','3','4']
             self.months  =  ['Feb','Mar' , 'Apr']
             self.colorline= 'b'
          elif name.capitalize() in 'Spring' and len(name) >2:
             self.code = 1
             self.ST_CODE = ['5','6']
             self.months=['May']
             self.colorline = 'orange'
          elif name.capitalize() in 'Summer' and len(name) >2:
             self.code = 2
             self.ST_CODE = ['6','7','8']
             self.months=['Jun','Jul','Aug']
             self.colorline = 'r'
          elif name.capitalize() in 'Autumn' or name.capitalize in 'Fall':
              if len(name) >2:
                 self.code = 3
                 self.ST_CODE =  ['10','11','12']
                 self.months=['Oct','Nov','Dec']
                 self.colorline = 'dodgerblue'
          else:
             import sys
             sys.exit('error in name of season')
def Season_colorlist():
    SEAScmap = ['b',  'r' ]
    MONTcmap = [ 'navy','mediumblue','blue',
                 'orange', 'darkorange', 'peru'  ,
                 'r', 'darkred' , 'firebrick' ,
                 'skyblue', 'deepskyblue', 'dodgerblue']
    return(SEAScmap, MONTcmap)

xmldoc    = minidom.parse(args.plotlistfile)
INPUTDIR  = addsep(args.inputdir)
OUTDIR = addsep(args.outdir)
var       = args.varname
iseas     = args.iseas
RUN       = args.run_name 

if "ins"     in RUN.lower():
   RUN_='DAfl'
   prex= 'i'
elif "hind"  in RUN.lower():
   RUN_='HIND'
   prex='h'
elif "syn"  in RUN.lower():
   RUN_='DAnn'
   prex='s'
elif "ppcon" in RUN.lower():
   RUN_ = 'PPCon'
   prex='p'
elif "DA_SATFLOAT/" == RUN:
   RUN_ = 'DA_SATFLOAT'
   prex='p'

else:
   raise Exception(" no run code with this name") 
   sys.exit('che run???') 

# carol
if iseas.capitalize().startswith('W'):
   iseas    = 'Winter'
   levels = np.arange(200,601,50)
   levels  = np.sort(np.append(0,levels))
   levs    = levels
   levs    = np.array([0,200,250,300,350,400,450,500,550,600 ])  #levels[::1]
elif iseas.capitalize().startswith('S') and iseas[1].capitalize().startswith('U') :
   iseas    = 'Summer'
   levels = np.arange(400,701,25)
   #levels  = np.sort(np.append(300,levels))
   levels  = np.sort(np.append(0,levels))
   levs=levels
   levs    = np.array([0, 400, 450, 500, 550, 600,650,700])  #levels[::2]

DIFF_DIR  = 'PPN_DIFF/'
DIFF_FILE = DIFF_DIR+iseas+'_DAfl_vs_DAnn.nc'
import os.path
# lot contour if a file of diff between 2 RUNS Exists
if os.path.isfile(DIFF_FILE):
   nc_diff   = Dataset(DIFF_FILE)
   ppn_diff  = nc_diff.variables['ppn'][:]


for lm in xmldoc.getElementsByTagName("LayersMaps"):
    for pdef in get_subelements(lm, "plots"):
        filevar = get_node_attr(pdef, "var")        
        if not filevar == var : continue
        PLOT = Plot(get_node_attr(pdef, "var"), get_node_attr(pdef, "longname"), get_node_attr(pdef, "plotunits"), [], [0,1] )
        for d in get_subelements(pdef, "depth"):
            levplot  = float(get_node_attr(d, "levplot")) 
            clim     = eval(get_node_attr(d, "clim"))
            L = Layer(get_node_attr(d,"top"), get_node_attr(d, "bottom"))
            PLOT.append_layer(L,clim=clim, mapdepthfilter=levplot)

clon,clat = coastline.get()
TheMask=Mask(args.maskfile)

CONVERSION_DICT={
         'ppn' : 365./1000,
         'P_c' : 1,
         'P_i' : 1,
         'DIC' : 1
         }

TI         = TimeInterval(args.starttime,args.endtime,"%Y%m%d")
req_label  = "Ave." + str(args.starttime)[:-2] + "-" +str(args.endtime)[:-2]

TL = TimeList.fromfilenames(TI, INPUTDIR,"ave*.nc",filtervar=var)
if TL.inputFrequency is None:
    TL.inputFrequency='monthly'
    print ("inputFrequency forced to monthly because of selection of single time")

from commons import season
from commons import timerequestors
seasonObj = season.season()

if iseas == 'Winter':
    req = requestors.Clim_season(0,seasonObj)
elif  iseas == 'Summer': 
    req = requestors.Clim_season(2,seasonObj)

indexes,weights = TL.select(req)
VARCONV=CONVERSION_DICT[var]

# se ho il file passo
import os
ncfile    = OUTDIR + iseas+ "_Map_" + var + "_" + req_label + "_Int" +  '0000-0200m-0200m'  + "_refScale_mgm2d.nc"
if os.path.isfile(ncfile):
   from netCDF4 import Dataset     
   nc = Dataset(ncfile)
   integrated_masked  =  nc.variables['ppn'][:] 
   outfile    = OUTDIR +prex+'_' +  iseas+ "_Map_" + var + "_" + req_label + "_Int" +  '0000-0200m-0200m' + "_refScale_mgm2d.png"
else:
   # setting up filelist for requested period -----------------
   filelist=[]
   for k in indexes:
       t = TL.Timelist[k]
       filename = INPUTDIR + "ave." + t.strftime("%Y%m%d-%H:%M:%S") + "." + var + ".nc"
       filelist.append(filename)
   # ----------------------------------------------------------
   print ("time averaging ...")
   M3d     = TimeAverager3D(filelist, weights, var, TheMask)
   print ("... done.")
   for il, layer in enumerate(PLOT.layerlist):
       z_mask = PLOT.depthfilters[il]
       z_mask_string = "-%04gm" %z_mask
       if  args.optype=='integral':
           outfile    = OUTDIR + iseas+ "_Map_" + var + "_" + req_label + "_Int" + layer.longname() + z_mask_string  + "_refScale_mgm2d.png"
       else:
           outfile    = OUTDIR + iseas+ "_Map_" + var + "_" + req_label + "_Ave" + layer.longname() + z_mask_string  + "_mgm2d.png"
       De      = DataExtractor(TheMask,rawdata=M3d)
       if args.optype=='integral':
           integrated = MapBuilder.get_layer_integral(De, layer)
       else:
           integrated = MapBuilder.get_layer_average(De, layer)
       integrated=integrated * VARCONV
       mask=TheMask.mask_at_level(z_mask)
       clim=PLOT.climlist[il]
       integrated_masked=integrated*mask # taglio il costiero
       integrated_masked[integrated_masked==0]=np.nan # sostituisco gli 0 con i NAN
       integrated_masked = (integrated_masked*1000)/365.

for il, layer in enumerate(PLOT.layerlist):
    z_mask = PLOT.depthfilters[il]
    z_mask_string = "-%04gm" %z_mask

# X ppn:
    pl.close()
    fig,ax = pl.subplots(figsize=(9,5))
    #fig.set_size_inches(10.0, 10.0*16/42)
    ax.set_position([0.08, 0.13, 0.78, 0.78])
    cmap    =  pl.get_cmap('plasma_r')
    #fig, (ax, ax2) = pl.subplots(1, 2,figsize=(12,6)  , gridspec_kw={'width_ratios': [5, 1]})
    #cmap    =  pl.get_cmap('Blues_r')
    norm    =  BoundaryNorm(levels, ncolors=cmap.N, clip=True)
    CS=ax.contourf(TheMask.xlevels, TheMask.ylevels,integrated_masked, cmap=cmap,norm=norm,  levels=levels,  extend="max")
    cbar=fig.colorbar(CS,ticks=levs, ax=ax)
    cbar.ax.tick_params(labelsize=16)
    #if RUN_ == 'DAnn':
    #   cc=ax.contour( TheMask.xlevels, TheMask.ylevels, ppn_diff, [15], colors=['k'], linewidths=2 )
    #   labels = ['diff DAfl DAnn: +15 ']
    #   for i in range(len(labels)):
    #     cc.collections[i].set_label(labels[i])
    #   legend =pl.legend(loc='upper left', fontsize=10)  
    #   legend.get_frame().set_alpha(None)
    #   #pl.legend(loc='upper center', bbox_to_anchor=(.5, 0.2),  fancybox=False, shadow=False, fontsize=20)
    CS.ax.set_xlim([-5,36])
    CS.ax.set_ylim([30,46])
    CS.ax.set_xlabel('Lon').set_fontsize(18)
    CS.ax.set_ylabel('Lat').set_fontsize(18)
    ax.tick_params(axis='x', labelsize=10)
    CS.ax.text(-4,31.5, 'NPP' + ' [' +"mgC m$ ^{-2}$ d$^{-1}$"  + ']',horizontalalignment='left',verticalalignment='center',fontsize=16, color='black')
    CS.ax.xaxis.set_ticks(np.arange(-2,36,6))
    CS.ax.yaxis.set_ticks(np.arange(30,46,4))
    #Draw coastline
    CS.ax.plot(clon,clat, color='#000000',linewidth=0.5)
    CS.ax.set_xlim([-6, 36])
    CS.ax.set_ylim([30, 46])
    ax.tick_params(axis='both', which='major', labelsize=18)
    title = "%s %s %s %s" % (RUN_ +':' , iseas + ' 2017-2018', 'NPP', layer.__repr__())
    pl.suptitle(title, fontsize = 20)
    pl.subplots_adjust(left=0.08, top = 0.9,bottom=0.17, right=1.05)
    pl.savefig(outfile, dpi=300)
    if (var == "ppn"):
        ncfile = OUTDIR + iseas+"_Map_" + var + "_" + req_label + "_Int" + layer.longname() + z_mask_string  + "_refScale_mgm2d.nc"
        netcdf3.write_2d_file(integrated_masked,"ppn",ncfile,TheMask)
        from basins import V2 as OGS
        from commons.submask import SubMask
        from basins.basin import ComposedBasin
        from commons.utils import writetable
        tablefile = OUTDIR + '/' + var +'_'+iseas +'_mean_basin.csv'
        OGSred = ComposedBasin('OGSred',[OGS.alb, \
                    OGS.swm1, OGS.swm2, OGS.nwm, OGS.tyr, \
                    OGS.adr, OGS.ion, OGS.lev , OGS.med], \
                    'Gruped Subbasin for ppn analysis')
        SUBlist = OGSred.basin_list
        nSub   = len(OGSred.basin_list)
        rows_names=[sub.name for sub in SUBlist]
        ppn_submean = np.zeros((nSub,1),np.float32)*np.nan
        for isub, sub in enumerate(OGSred):
            S = SubMask(sub, maskobject=TheMask)
            mask2d=S.mask[0,:,:]
            ppn_submean[isub,0] = np.nanmean(integrated_masked[mask2d])
        df = pd.DataFrame(np.array(ppn_submean))
        df.index = rows_names
        df.columns = ['mgCm-2d-1']
        df.to_csv(tablefile )


    #pl.close(fig)
    #ax2 = fig.add_subplot(122)
    #tablefile = OUTDIR + '/' + var +'_'+iseas +'_mean_basin.csv'
    #df = pd.read_csv(tablefile,index_col=0)
    #font_size=18
    #bbox=[0, 0, 1, 1]
    #ax2.axis('off')
    #mpl_table = ax2.table(cellText = df.values.round(), rowLabels = df.index, bbox=bbox, colLabels=df.columns)
    #mpl_table.auto_set_font_size(False)
    #mpl_table.set_fontsize(font_size)

import shutil
shutil.copy('averager_and_plot_map_ppn_refScale_seas_FMA_JJA.py' , OUTDIR + '/'  )
