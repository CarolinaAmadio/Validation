import numpy as np
from commons.Timelist import TimeList
import warnings
warnings.filterwarnings('ignore')

#\\RUN, run  = 'Multivariate_2017_2018' , 'Multi'
#RUN, run  = 'PSEUDO_2017_2018_CAL'   , 'PCAL'
#RUN, run  = 'IN_SITU_2017_2018'      , 'insitu'
#RUN ,run  = 'SYNTHETIC_2017_2018'    , 'syn'

RUN ,run    = 'PPCon','PPCon'

INDIR='/g100_scratch/userexternal/camadio0/'+RUN+'/wrkdir/MODEL/DA__FREQ_1/'
TLmis = TimeList.fromfilenames(None,INDIR,'*.arg_mis.dat', \
               prefix='',dateformat='%Y%m%d')

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
        indvar = np.where(misarray[:,1]==DICTflagvar[var_mod])
        if len(indvar[0])< 1: continue
        newarray = misarray[indvar,:][0]
        LONall = newarray[:,2]
        llon,indunique = np.unique(LONall,return_index=True)
        llat = newarray[indunique,3]
        LONprofs[var_mod].extend(llon)
        LATprofs[var_mod].extend(llat)
        DATEprofs[var_mod].extend([TLmis.Timelist[ifile] for ii in range(len(llon))])

        NAMEfloat = newarray[indunique,-1]
        NAMEprofs[var_mod].extend([np.str(np.int(nn)) for nn in NAMEfloat])

        nprofiles = len(llon)
        nprofs[var_mod] += nprofiles

import pandas as pd


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

df.to_csv('Float_assimilated_'+ run +'.csv')

