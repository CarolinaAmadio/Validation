# crea il file *csv con i float assimilati per n3n,p_l e o2o 
# lo fa dagli argmis

import numpy as np
from commons.Timelist import TimeList
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

#RUN, run  = 'hindcast_2017_2018'      , 'hindcast_2017_2018'      # -->  no assimilazioen
#RUN, run  = 'Multivariate_2017_2018'  , 'Multivariate_2017_2018'
#RUN, run  = 'PSEUDO_2017_2018_CAL'    , 'PSEUDO_2017_2018_CAL'
#RUN, run  = 'SYNTHETIC_2017_2018'     , 'SYNTHETIC_2017_2018' 
RUN, run  = 'SYNTHETIC_2017_2018_NITRATE_ERROR' , 'SYN_NITRATE_ERROR'
#RUN, run  = 'IN_SITU_2017_2018' , 'IN_SITU_2017_2018'


NITRATE_PSEUDO=True # to save specific dataframe for investigate Nitrate qc 

INDIR='/g100_scratch/userexternal/camadio0/'+RUN+'/wrkdir/MODEL/DA__FREQ_1/'
INDA ='/g100_scratch/userexternal/camadio0/'+RUN+'/wrkdir/DA/'
TLmis = TimeList.fromfilenames(None,INDIR,'*.arg_mis.dat', \
               prefix='',dateformat='%Y%m%d')

TLmis_n3n = TimeList.fromfilenames(None,INDA,'*N3n*.csv', \
               prefix='',dateformat='%Y%m%d')

# argmisdat clumns ['Nr','VAR_type', 'lon', 'lat' , 'depth' ,'nr1','misfit', 'error', 'wmo']
# DA/[date] N3n_check.csv ,Nr,VAR_type,lon,lat,depth,nr1,misfit,error,wmo,qc

nprofs = {}
LONprofs = {}
LATprofs = {}
DATEprofs = {}
NAMEprofs = {}

VARLIST = ['N3n','P_l','O2o']
for var_mod in VARLIST:
    nprofs[var_mod] = 0
    LONprofs[var_mod] = []
    LATprofs[var_mod] = []
    DATEprofs[var_mod] = []
    NAMEprofs[var_mod] = []

DICTflagvar = {
     'P_l': 0,
     'N3n': 1,
     'O2o': 2,
}

check = 0


for ifile,misfile in enumerate(TLmis.filelist):
    fid = open(misfile,'r')
    misarray = np.loadtxt(fid,skiprows=1)
    fid.close()
    if len(misarray) <1:
        check += 1
        continue
    for var_mod in VARLIST:  
        indvar = np.where(misarray[:,1]==DICTflagvar[var_mod]) #idx per vartype column
        #indvar nitrate coming from all the wmo available in a day
        if len(indvar[0])< 1: continue
        newarray = misarray[indvar,:][0] # select per index the [0] return 2d array
        LONall = newarray[:,2]
        llon,indunique = np.unique(LONall,return_index=True)
        llat = newarray[indunique,3]
        LONprofs[var_mod].extend(llon)
        LATprofs[var_mod].extend(llat)
        DATEprofs[var_mod].extend([TLmis.Timelist[ifile] for ii in range(len(llon))])
        NAMEfloat = newarray[indunique,-1]
        NAMEprofs[var_mod].extend([str(int(nn)) for nn in NAMEfloat])
        nprofiles = len(llon)
        nprofs[var_mod] += nprofiles

DF_LEN  = nprofs[max(nprofs, key=nprofs.get)]
LIST_COLUMN_NAME =  []
LIST_COL         =  ['LON','LAT','DATE','NAME']

for VAR in VARLIST:
    for COL in LIST_COL: 
        namecol = VAR+'_'+ COL
        LIST_COLUMN_NAME.append(namecol)

df      = pd.DataFrame(index = np.arange(0, DF_LEN) , columns=  LIST_COLUMN_NAME)


for VAR in VARLIST:
    VarValue  = np.array(LONprofs[VAR]) 
    df[VAR+'_LON'].iloc[0:len(VarValue)]  = np.array(LONprofs[VAR])
    df[VAR+'_LAT'].iloc[0:len(VarValue)]  = np.array(LATprofs[VAR])
    df[VAR+'_DATE'].iloc[0:len(VarValue)] = np.array(DATEprofs[VAR])
    df[VAR+'_NAME'].iloc[0:len(VarValue)] = np.array(NAMEprofs[VAR])

df.to_csv('Float_assimilated_'+run+'.csv')


df1=df.iloc[:,0:4]
df1.dropna(inplace=True)
df1.N3n_NAME = df1.N3n_NAME.astype(int)
df1.N3n_LAT = df1.N3n_LAT.astype(float)
df1.N3n_LON = df1.N3n_LON.astype(float)

df1['Qc'] = np.nan


if NITRATE_PSEUDO:
  for FILEN3N in TLmis_n3n.filelist:
      serv = pd.read_csv(FILEN3N , index_col=0)
      serv = serv[serv.VAR_type==1.0]
      serv.wmo = serv.wmo.astype(int)
      WMOserie =  serv.wmo.drop_duplicates()

      for WMO in WMOserie:
         s_tm = serv[serv.wmo== WMO]
         d_tm = df1[df1.N3n_NAME== WMO]
         lat_ = s_tm.lat.drop_duplicates()
         lon_ = s_tm.lon.drop_duplicates()
         d_tm = d_tm[d_tm.N3n_LAT==lat_.values[0] ]
         d_tm = d_tm[d_tm.N3n_LON==lon_.values[0] ]
         IDX = d_tm.index.values[0]
         df1.Qc.iloc[IDX] = s_tm.qc.drop_duplicates().values[0]
        

df1.to_csv('Float_assimilated_'+run+'_N3nqc.csv')



