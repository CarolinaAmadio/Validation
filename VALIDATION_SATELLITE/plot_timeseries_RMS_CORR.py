import argparse
def argument():
    parser = argparse.ArgumentParser(description = '''
    creo i files csv di RMSE assimilati 
    per poi fare barplot di rmse

    ''',
    formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(   '--outdir', '-o',
                            type = str,
                            required =True,
                            default = "./",
                            help = ''' Output image dir'''
                            )

    parser.add_argument(   '--inputdir', '-i',
                            type = str,
                            required = True,
                            default = 'path export_data_ScMYValidation_plan.pkl',
                            help = 'Input pickle file')
    parser.add_argument(   '--run', '-r',
                                type = str,
                                required = True,
                                help = ''' simulation name'''
                                )
    return parser.parse_args()

args = argument()


# OUTPUTS
import pickle
import numpy as np
from commons.utils import addsep# table IV.1 in frmato csv per mesi e stagioni modificate
from commons.utils import addsep

#RUN      = 'hindcast_2017_2018'
#RUN      = 'Multivariate_2017_2018'
#RUN      = 'PSEUDO_2017_2018_CAL'  
#RUN       = 'IN_SITU_2017_2018'
#RUN       = 'SYNTHETIC_2017_2018'

RUN        = args.run
INPUTFILE  = args.inputdir
OUTDIR     = addsep(args.outdir)

print('Processed statistics for run: ')
print(RUN)


#INPUTDIR = '/g100_scratch/userexternal/camadio0/FLOAT_ELAB_DAFloat/QuIDeval/' 
#OUTDIR   = '/g100/home/userexternal/camadio0/FIG_PAPER/'
fid = open(  INPUTFILE,   'rb')
LIST = pickle.load(fid)
fid.close()


model_label=' MODEL'
var_label = "CHL [mg/m$^3$]"

TIMES                          = LIST[0]
BGC_CLASS4_CHL_RMS_SURF_BASIN  = LIST[1]
BGC_CLASS4_CHL_BIAS_SURF_BASIN = LIST[2]

from basins import V2 as OGS

nSUB = len(OGS.P.basin_list)

from commons import timerequestors
from commons.Timelist import TimeInterval, TimeList
TL=TimeList(TIMES)
from commons.utils import writetable

# Marzo  poi Aprile
FEB_req = timerequestors.Clim_month(2)
MAR_req = timerequestors.Clim_month(3)
APR_req = timerequestors.Clim_month(4)

ii,w   = TL.select( FEB_req)
mi,mw  = TL.select( MAR_req)
ai,aw  = TL.select( APR_req)

ii.extend(mi)
ii.extend(ai)
ii.sort()

RMS__win = np.nanmean(BGC_CLASS4_CHL_RMS_SURF_BASIN[     ii,:],axis=0)


# Giugno poi appendo luglio

JUN_req = timerequestors.Clim_month(6)
JUL_req = timerequestors.Clim_month(7)
AUG_req = timerequestors.Clim_month(8)

ii,w  = TL.select( JUN_req)
ji,jw = TL.select( JUL_req)
ai,aw = TL.select( AUG_req) 

ii.extend(ji)
ii.extend(ai)
ii.sort()

RMS__sum = np.nanmean(BGC_CLASS4_CHL_RMS_SURF_BASIN[     ii,:],axis=0)

mat = np.zeros((nSUB,18),np.float32)
mat[:,0] = RMS__win
mat[:,1] = RMS__sum

import pandas as pd
df_column_names = ['Sub_basin','RMS_MA','RMS_JJ']
df              = pd.DataFrame(index= np.arange(0, nSUB ) , columns =df_column_names )
df.Sub_basin         = OGS.P.basin_list 
df.RMS_MA, df.RMS_JJ = RMS__win , RMS__sum

print('Data saved at:  ' + OUTDIR  +"FMA_JJA_table4.1_chla.csv")
df.to_csv(OUTDIR  +"FMA_JJA_table4.1_chla.csv")

#writetable(outfiletable, mat, rows_names, column_names, fmt='%5.3f\t')

