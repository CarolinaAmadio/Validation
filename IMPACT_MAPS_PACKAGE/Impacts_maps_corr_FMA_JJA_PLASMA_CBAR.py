#export PYTHONPATH='/g100/home/userexternal/camadio0/bit.sea_py3/'
#export ONLINE_REPO=/g100_scratch/userexternal/camadio0/SUPERFLOAT_2012_2021_V8c/ 

import numpy as np
import sys
sys.path.append("/g100/home/userexternal/camadio0/CA_functions/")
from netCDF4 import Dataset
import commons
from commons.mask import Mask
from commons.dataextractor import DataExtractor
from layer_integral.mapbuilder import MapBuilder
import matplotlib.colors as colors
from commons.layer import Layer
from layer_integral import mapbuilder
import shutil
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
from commons.time_interval import TimeInterval
from commons.Timelist import TimeList
from funzioni_CA import parsing_path
from funzioni_CA import new_directory
from funzioni_CA import plot_Medsea
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import matplotlib as mpl
from matplotlib import cm as color_map
import matplotlib as mpl
from mpl_toolkits.basemap import Basemap

# Input to change (no implement loop because script killes)
varname     = 'N3n'
#varname     = 'P_l'
#varname     = 'O2o'

iseas       = 0
USE_DF      = True  # imptut data already saved

if varname == 'P_l':
   depth       =  300
else:
   depth       =  600

# Input of simulationi: Run e REF(hindcast)

REF         = 'HC'
RUN ,run    = 'PPCON/DA_SATFLOAT_ppcon','PPCon'

INPUTDIR  = '/g100_scratch/userexternal/camadio0/' + RUN + '/wrkdir/POSTPROC/output/AVE_FREQ_1/TMP/'
INDIR     = '/g100_scratch/userexternal/camadio0/PPCON/VALIDAZIONE_RUNs/Validation/IMPACT_MAPS_PACKAGE/HC/'
OUTDIR    = '/g100_scratch/userexternal/camadio0/PPCON/VALIDAZIONE_RUNs/Validation/IMPACT_MAPS_PACKAGE/PPCon/'
maskfile  = '/g100_work/OGS_devC/Benchmark/SETUP/PREPROC/MASK/meshmask.nc'
DATESTART = '20190101'
DATE__END = '20200101'

print(varname)
print(INDIR)
print(INPUTDIR)

T_INT     = TimeInterval(DATESTART,DATE__END, '%Y%m%d')
TL_run    = TimeList.fromfilenames(T_INT, INPUTDIR,"ave*.nc",filtervar= varname)
TL_ref    = TimeList.fromfilenames(T_INT, INDIR,"ave*.nc",filtervar= varname)

def plot_map(lat,lon,data,MIN,MAX):
   map = Basemap(
     llcrnrlon  = -6, #  np.round(df.LON.min()-2,0), # Longitude lower right corner
     llcrnrlat  = 30, # np.round(df.LAT.min()-2,0), # Latitude lower right corner
     urcrnrlon  = 40, # np.round(df.LON.max()+2,0), # Longitude upper right corner
     urcrnrlat  = 46, # np.round(df.LAT.max()+2,0), # Latitude upper right corner
     resolution =   'i', # Crude resolution
     projection = 'merc', # Transverse Mercator projection
     lat_0      =   np.round(lat.mean(),0), # Central latitude
     lon_0      =   np.round(lon.mean(),0)   # Central longitude
)

   map.drawcoastlines()
   map.drawmapboundary(fill_color='aliceblue')
   map.fillcontinents(color='white',lake_color='lightcyan')
   map.drawparallels(np.arange(30,46,10.),labels=[1,0,0,0] ,dashes=[2,2],  fontsize=22 )
   map.drawmeridians(np.arange(-6,41,10), labels=[0,0,0,1],dashes=[2,2], fontsize=22)
   x, y = map(*np.meshgrid(lon,lat))
   levels  =   MaxNLocator(nbins=8).tick_values(np.nanmin(MIN),np.nanmax(MAX))
   levs = levels[::2]
   cmap    =  plt.get_cmap('plasma_r')
   norm    =  BoundaryNorm(levels, ncolors=cmap.N, clip=True)
   cset1   =  map.contourf(x,y,data,cmap=cmap,levels=levels, norm=norm, extend="both")
   return (map,cset1,levs,levels,x,y)

parsing_path(INDIR,'/' )

dep         = str(depth)
TheMask     = Mask(maskfile)
DEN         = TheMask.getDepthIndex(depth)+2
jpk,jpj,jpi = TheMask.shape
nav_lev =  TheMask.zlevels
LAYERLIST =Layer(0,depth)

if iseas==0:
    STAGIONE='Winter'
elif iseas==2:
    STAGIONE='Summer'
else:
    sys.exit('error stagione')


if USE_DF: 
    final    = pd.read_csv (OUTDIR+ run+ '_final_'     + STAGIONE  + '_' + varname + '.csv' , index_col=0 )
    final_95 = pd.read_csv (OUTDIR+ run+ '_final_95_'  + STAGIONE  + '_' + varname + '.csv' , index_col=0 )
    final_50 = pd.read_csv (OUTDIR+ run+ '_final_50_'  + STAGIONE  + '_' + varname + '.csv' , index_col=0 )
else:
    #ciclo su stagione loop lungo killed spesso
    from commons import season
    from commons import timerequestors as requestors
    seasonObj = season.season()
    meanREF = {}
    DIFF= {}
    if iseas == 0 :
      FEB_req = requestors.Clim_month(2)
      MAR_req = requestors.Clim_month(3)
      APR_req = requestors.Clim_month(4)
      ii,w   = TL_ref.select( FEB_req)
      mi,mw  = TL_ref.select( MAR_req)
      ai,aw  = TL_ref.select( APR_req)
      ii.extend(mi)
      ii.extend(ai)
      ii.sort()
    elif iseas==2:
      JUN_req = requestors.Clim_month(6)
      JUL_req = requestors.Clim_month(7)
      AUG_req = requestors.Clim_month(8)
      ii,w  = TL_ref.select( JUN_req)
      ji,jw = TL_ref.select( JUL_req)
      ai,aw = TL_ref.select( AUG_req)
      ii.extend(ji)
      ii.extend(ai)
      ii.sort()
    else:
      sys.exit('season not implemented')

    indseas = ii # indici lista
    del ii
    LISTref = []
    LIST_DIFF = []
    for ii in indseas:
       # ref
       fileref = TL_ref.filelist[ii]
       filerun = TL_run.filelist[ii]
       # stupid check
       if TL_ref.Timelist[ii] == TL_run.Timelist[ii]:
           pass
       else:
           sys.exit('check time')    
       mmr = Dataset(fileref)
       var_= mmr.variables[varname][0,0:DEN,:,:]
       FILL_VAL = var_.fill_value
       #LISTref.append(var_)
       mmr.close()

       # run
       mrun = Dataset(filerun)
       var_run= mrun.variables[varname][0,0:DEN,:,:]
       De_run  = DataExtractor(TheMask, rawdata= var_run )
       De_ref  = DataExtractor(TheMask, rawdata= var_   )
    
       REF_mapdiffabsINT  = MapBuilder.get_layer_integral(De_ref, LAYERLIST)
       LISTref.append(REF_mapdiffabsINT)
       diffabs = np.abs(De_run.filled_values - De_ref.filled_values)
       De_dabs = DataExtractor(TheMask,rawdata=diffabs)
       mapdiffabsINT  = MapBuilder.get_layer_integral(De_dabs, LAYERLIST)
       LIST_DIFF.append(mapdiffabsINT)
    #del(var_ , var_run)
    #meanREF = LISTref   # denomitarore formula in teruzzi 2019
    # media sul tempo 
    DIFF = np.array(LIST_DIFF)
    data= np.nanmean(DIFF , axis=0)
    # numeratore 95 percentile
    data_95 = np.nanpercentile( DIFF, 95, axis=0) 
    # numeratore 50 percentile
    data_50 = np.nanpercentile( DIFF, 50, axis=0)
    # DENOMINATORE
    # meanREF[iseas]
    meanREF = np.array(LISTref)
    meanREF[meanREF>= FILL_VAL]=np.nan
    INT = np.nanmean( meanREF )
    final    = data/INT
    final_95 = data_95/INT
    final_50 = data_50/INT
    # SAVE DF TO AVOID RUN PREVIOUS PART OF 
    df_final = pd.DataFrame(final)
    df_final_95 = pd.DataFrame(final_95)
    df_final_50 = pd.DataFrame(final_50)
    df_final.to_csv( OUTDIR +   run + '_final_'    + STAGIONE + '_' + varname + '.csv')
    df_final_95.to_csv(OUTDIR +  run + '_final_95_' + STAGIONE + '_' + varname + '.csv')
    df_final_50.to_csv(OUTDIR + run + '_final_50_' + STAGIONE + '_' + varname + '.csv')


#
lat = TheMask.ylevels[:,0]
lon = TheMask.xlevels[0,:]

# red circle as in teruzzi et al., 2021
Lon = TheMask.xlevels
Lat = TheMask.ylevels

df           =  pd.read_csv('Float_assimilated_'+run +'_' +varname+'.csv' ,index_col=0  )
ar_lat = df.lat.values
ar_lon = df.lon.values
areasf = {}

df1=pd.DataFrame(index=np.arange(0, Lon.shape[0]), columns= np.arange(0,Lon.shape[1]))

for vals in range(0,len(df)):
    dist = ((Lon-ar_lon[vals])**2+(Lat-ar_lat[vals])**2)**.5
    areasf[vals]= np.zeros((jpj,jpi))
    areasf[vals][dist<0.3] = 1
    areasf[vals][TheMask.mask[0,:,:]==False] = np.nan
    if vals == 0:
       df1.iloc[:,:] = areasf[vals]
    else:
       df1.iloc[:,:] = df1.iloc[:,:]+areasf[vals]    

df1[df1 > 0] = 1

#   hardcoded defined min max to compare winter and summer sims
if varname == 'O2o':
    NAME='Oxygen'
    MIN = 0.
    MAX = 0.02
elif varname== 'P_l':
    NAME='Chlorophyll'
    MIN = 0.
    MAX = 0.8
else: 
    NAME='Nitrate'
    MIN = 0.
    MAX = 0.4
# INTEGRALE 0-depth m 95 percentile
fig = plt.figure(figsize=(12,8))
ax=fig.add_subplot()
map,cset1,levs ,levels,  xx,yy  = plot_map(lat,lon,final_95, MIN, MAX)
cb3 =fig.colorbar(cset1, ax=ax, fraction=0.02, pad=0.04)

cb3.set_ticks(levs)
cb3.ax.tick_params(labelsize=24)  # set your label size here
#cs = map.contour(xx,yy,np.array(df1) , [ 0,1], linewidths=2,  colors='w')

plt.title(NAME + ' Layer: '+LAYERLIST.longname() +'\n 95 percentile, I(t) (t0= ' +str(DATESTART[0:4]) + ', tend= ' +  str( int(DATE__END[0:4])-1) + ' in '+ STAGIONE + ')' ,fontsize=18, color='k',)
fig.tight_layout()
plt.savefig(OUTDIR+'/'+ varname +'_'+ run+'_'+STAGIONE+'_'+ LAYERLIST.longname()+'_95percentile_impact_maps_plasma_dpi300_.png' , dpi=300)

# percentuale of med interested (val> trhes ) 

