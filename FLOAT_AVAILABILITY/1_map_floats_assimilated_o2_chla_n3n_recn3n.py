import numpy as np
import basins.OGS as OGS
from instruments import superfloat
from instruments.var_conversions import FLOATVARS
import warnings
warnings.filterwarnings('ignore')
import sys
sys.path.append("/g100/home/userexternal/camadio0/CA_functions/")
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from basins_CA import plot_map_subbasins
from matplotlib.patches import Polygon
name_basins, basin_borders = plot_map_subbasins()

RUN, run  = 'DA_SATFLOAT' , 'DA_SATFLOAT'
RUN, run  = 'PPCon' , 'PPCon'
VARLIST = ['N3n','P_l','O2o']


df    = pd.read_csv('Float_assimilated_'+ RUN    +'.csv' , index_col=0)
dfqc  = pd.read_csv('Float_assimilated_'+ RUN    +'_N3nqc.csv',   index_col=0)

CHLA    = df[['P_l_LON', 'P_l_LAT', 'P_l_DATE', 'P_l_NAME',]]
O2o     = df[['O2o_LON', 'O2o_LAT', 'O2o_DATE', 'O2o_NAME',]]
N3n     = dfqc[dfqc.Qc>=0]
N3n_rec = dfqc[dfqc.Qc<0]

# la somma di len(N3n) + len(N3n_rec) = len(df)
NAMEVAR  = 'N3n'
strings=df.columns
LIST_sliced_df = [string for string in strings if NAMEVAR in string]
df=df[LIST_sliced_df]
df.dropna(how='all', inplace=True)
LIST_COL         =  ['lon','lat','DATE','NAME']
df.columns = LIST_COL

fig, ax = plt.subplots(figsize=(15, 8))
map = Basemap(
     llcrnrlon  =  -6, #  np.round(df.LON.min()-2,0), # Longitude lower right corner
     llcrnrlat  =  30, # np.round(df.LAT.min()-2,0), # Latitude lower right corner
     urcrnrlon  =  36, # np.round(df.LON.max()+2,0), # Longitude upper right corner
     urcrnrlat  =  46, # np.round(df.LAT.max()+2,0), # Latitude upper right corner
     resolution =   'i', # Crude resolution
     projection = 'merc', # Transverse Mercator projection
)

map.drawparallels(np.arange(20,48,5.),labels=[1,0,0,0], linewidth=0.001, fontsize=24)
map.drawmeridians(np.arange(-6,40,5.),labels=[0,0,0,1], linewidth=0.001, fontsize=24)
map.drawcoastlines(color='silver' )
map.drawmapboundary(fill_color='white')
map.fillcontinents(color='white' ,lake_color='white')

#  linewidth = 00 doesnt work with version of python 3.6 and after
#map.drawparallels(np.arange(20,48,5.),labels=[1,0,0,0], linewidth=0.0, fontsize=20)
#map.drawmeridians(np.arange(-6,40,5.),labels=[0,0,0,1], linewidth=0.0, fontsize=20)

for III in range(0,len(name_basins)):
    lat_corners= np.array(basin_borders[III])[:,1]
    lon_corners= np.array(basin_borders[III])[:,0]
    poly_corners = np.zeros((len(lat_corners), 2), np.float64)
    poly_corners[:,0] = lon_corners
    poly_corners[:,1] = lat_corners
    x, y = map( poly_corners[:,0], poly_corners[:,1] )
    xy = zip(x,y)
    poly = Polygon( list(xy), facecolor='white', edgecolor='grey')
    plt.gca().add_patch(poly)

map.fillcontinents(color='white' ,lake_color='white')


# PLotto pseudonitrato dataset
N3n_rec = N3n_rec.iloc[:,0:-1]
N3n_rec.columns= LIST_COL
if len(N3n_rec) >0:
   lat=np.array(N3n_rec.lat)
   lon=np.array(N3n_rec.lon)
   lons, lats      = map(lon, lat)  # transform coordinates
   scat = ax.scatter(lons, lats,          s=200, zorder=4, marker='o', facecolor='tab:blue',  edgecolor='k'  , linewidth=0.9 , alpha=0.9)
   scat = ax.scatter(lons[0], lats[0],    s=200, zorder=4,  marker='o',  facecolor='tab:blue',  edgecolor='k', linewidth=0.9 , alpha=0.9, label= 'recNO3' )
   plt.gca()


N3n = N3n.iloc[:,0:-1]
N3n.columns= LIST_COL
lat=np.array(N3n.lat)
lon=np.array(N3n.lon)
lons,lats  = map(lon,lat)

# plotto nitrati
scat = ax.scatter(lons[0], lats[0],  s=150, zorder=4, marker='o' , color='orangered', edgecolor='k', linewidth=.1 ,  label= 'NO3' )
scat = ax.scatter(lons,    lats,     s=150, zorder=4, marker='o' , color='orangered', edgecolor='k', linewidth=.1 )


# Cloro quadretti
lat=np.array(CHLA.P_l_LAT)
lon=np.array(CHLA.P_l_LON)
lons, lats      = map(lon, lat)  # transform coordinates
scat = ax.scatter(lons, lats,          s=20, zorder=4, color='w', marker= "s", edgecolor='k', linewidth=0.9 , alpha=1)
scat = ax.scatter(lons[0], lats[0],    s=20, zorder=4, color='w', marker= "s", edgecolor='k', linewidth=0.9 , alpha=1, label= 'Chl' )
plt.gca()

ax.annotate(text = "Alb",xy  = (map(-3.5,  35.8) ), fontsize=16,  weight='bold') #,bbox={'facecolor': 'w', 'alpha': 0.5, 'pad': 10}  ))
ax.annotate(text = "Swm1",xy = (map(2,     37.45)   ), fontsize=16, weight='bold' )
ax.annotate(text = "Nwm",xy  = (map(1.,    40.2) ), fontsize=16,weight='bold' )
ax.annotate(text = "Swm2",xy = (map(5.1,   36.7) ), fontsize=16 , weight='bold')
ax.annotate(text = "Tyr1",xy = (map(10,    41.7) ), fontsize=16, weight='bold')
ax.annotate(text = "Tyr2",xy = (map(10.8,  38.3)   ), fontsize=16, weight='bold')
ax.annotate(text = "Adr1",xy = (map(14.3,  43)   ), fontsize=16, weight='bold')
ax.annotate(text = "Adr2",xy = (map(18.,   40.5)   ), fontsize=16, weight='bold')
ax.annotate(text = "Aeg",xy = (map(25,     37)   ), fontsize=16, weight='bold')

ax.annotate(text = "Ion1",xy = (map(12,    34.5)   ), fontsize=16, weight='bold')
ax.annotate(text = "Ion2",xy = (map(17,    32.5)   ), fontsize=16, weight='bold')
ax.annotate(text = "Ion3",xy = (map(19,    38)   ), fontsize=16, weight='bold')

ax.annotate(text = "Lev1",xy = (map(22.2,    33)   ), fontsize=16, weight='bold')
ax.annotate(text = "Lev2",xy = (map(31,    31.8)   ), fontsize=16, weight='bold')
ax.annotate(text = "Lev3",xy = (map(30.,   35)   ), fontsize=16, weight='bold')
ax.annotate(text = "Lev4",xy = (map(33.5,  34.1)   ), fontsize=16, weight='bold')

#plt.text('Longitude (deg)', fontsize=22, rotation=90 )
#plt.text('Latitude (deg)' , fontsize=22)

plt.title('Spatial Distribution of BGC Argo and recNO3 in 2019', fontsize=24, color='k')
plt.subplots_adjust(left=0.1,top = 0.90 ,bottom=0.12,  right=0.95)
fig.legend(loc='lower left', bbox_to_anchor=(0.1,0.13), fontsize=22,  shadow=True, ncol=1)

#plt.show()
plt.savefig('2_fig_float_maps_dpi300_'+run+'.png') # , dpi=300)
plt.close()



