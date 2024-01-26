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

RUN, run    = 'IN_SITU_2017_2018'  , 'insitu'
RUN1 ,run1  = 'SYN_NITRATE_ERROR'  , 'syn'
VARLIST = ['N3n','P_l','O2o']


dfc  = pd.read_csv('Float_assimilated_'+ RUN1    +'.csv' , index_col=0)
dfm  = pd.read_csv('Float_assimilated_'+ RUN   +'.csv', index_col=0)


# ho gia verificato che chla e chl1 sono uguali 
CHLA = dfc[['P_l_LON', 'P_l_LAT', 'P_l_DATE', 'P_l_NAME',]]

# Prendo solo i nitrati di PSEUDO 1434 CIRCA dfc
NAMEVAR  = 'N3n'
strings=dfc.columns
LIST_sliced_df = [string for string in strings if NAMEVAR in string]
dfc=dfc[LIST_sliced_df]
dfc.dropna(how='all', inplace=True)
LIST_COL         =  ['lon','lat','DATE','NAME']
dfc.columns = LIST_COL

fig, ax = plt.subplots(figsize=(15, 8))
map = Basemap(
     llcrnrlon  =  -6, #  np.round(df.LON.min()-2,0), # Longitude lower right corner
     llcrnrlat  =  30, # np.round(df.LAT.min()-2,0), # Latitude lower right corner
     urcrnrlon  =  36, # np.round(df.LON.max()+2,0), # Longitude upper right corner
     urcrnrlat  =  46, # np.round(df.LAT.max()+2,0), # Latitude upper right corner
     resolution =   'i', # Crude resolution
     projection = 'merc', # Transverse Mercator projection
)
map.drawcoastlines(color='silver' )
map.drawmapboundary(fill_color='white')
map.fillcontinents(color='white' ,lake_color='white')
#map.drawparallels(np.arange(20,48,1.), labels=[1,0,0,0] ,dashes=[2,2])
#map.drawmeridians(np.arange(-6,40,1.), labels=[0,0,0,1],dashes=[2,2])

map.drawparallels(np.arange(20,48,5.),labels=[1,0,0,0], linewidth=0.0, fontsize=24)
map.drawmeridians(np.arange(-6,40,5.),labels=[0,0,0,1], linewidth=0.0, fontsize=24)

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
lat=np.array(dfc.lat)
lon=np.array(dfc.lon)
lons, lats      = map(lon, lat)  # transform coordinates
scat = ax.scatter(lons, lats,          s=200, zorder=4, marker='o', facecolor='tab:blue',  edgecolor='k'  , linewidth=0.9 , alpha=0.9)
scat = ax.scatter(lons[0], lats[0],    s=200, zorder=4,  marker='o',  facecolor='tab:blue',  edgecolor='k', linewidth=0.9 , alpha=0.9, label= 'Reconst. Nitrate' )
plt.gca()

# ora sopra ci plotto Nitrati con un altro colore
# lavoro su nitrati da dataframe di tutte le vars cone sopra
dfm=dfm[LIST_sliced_df]
dfm.dropna(how='all', inplace=True)
dfm.columns = LIST_COL

lat=np.array(dfm.lat)
lon=np.array(dfm.lon)
lons,lats  = map(lon,lat)

# plotto nitrati
scat = ax.scatter(lons[0], lats[0],  s=150, zorder=4, marker='o' , color='orangered', edgecolor='k', linewidth=.1 ,  label= 'Nitrate' )
scat = ax.scatter(lons,    lats,     s=150, zorder=4, marker='o' , color='orangered', edgecolor='k', linewidth=.1 )


# Cloro crocette
#lat=np.array(CHLA.P_l_LAT)
#lon=np.array(CHLA.P_l_LON)
#lons, lats      = map(lon, lat)  # transform coordinates
#scat = ax.scatter(lons, lats,          s=20, zorder=4, color='w', marker= "s", edgecolor='k', linewidth=0.9 , alpha=1)
#scat = ax.scatter(lons[0], lats[0],    s=20, zorder=4, color='w', marker= "s", edgecolor='k', linewidth=0.9 , alpha=1, label= 'Chla' )
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

plt.title('BGC-Argo availability for: 2017-2018', fontsize=24, weight='bold', color='k')
plt.subplots_adjust(left=0.05,top = 0.90 ,bottom=0.12,  right=0.99)
fig.legend(loc='lower left', bbox_to_anchor=(0.1,0.13), fontsize=24,  shadow=True, ncol=1)
#plt.savefig('float_maps_dpi300.png')
plt.savefig('z.png')
plt.close()



