import argparse
def argument():
    parser = argparse.ArgumentParser(description = '''
    Produces Hovmoeller png files.
    An image for each wmo and for CHLA, NITRATE, DOXY
    Each image contains
    - the float trajectory
    - the Hovmoeller for float and model
    - the specific statistics
    ''', formatter_class=argparse.RawTextHelpFormatter)


    parser.add_argument(   '--maskfile', '-m',
                                type = str,
                                default = "/marconi_scratch/userexternal/lfeudale/Maskfiles/meshmask.nc",
                                required = False,
                                help = ''' Path of maskfile''')
    parser.add_argument(   '--basedir', '-b',
                                type = str,
                                required = True,
                                help = ''' Path of the PROFILATORE dir''')
    parser.add_argument(   '--indir', '-i',
                                type = str,
                                default = None,
                                required = True,
                                help = "Inputdir, the directory of the outputs of SingleFloat_vs_Model_Stat_Timeseries.py")

    parser.add_argument(   '--outdir', '-o',
                                type = str,
                                default = None,
                                required = True,
                                help = "path of the output dir")

    return parser.parse_args()

args = argument()


import os,sys
from commons.mask import Mask
from commons.Timelist import TimeList, TimeInterval
from basins.region import Rectangle
from instruments import superfloat as bio_float
from instruments.var_conversions import FLOATVARS
import numpy as np
import numpy.ma as ma
from commons.utils import addsep
import matplotlib.pyplot as pl
from instruments.matchup_manager import Matchup_Manager
import matplotlib.dates as mdates
from validation.online.SingleFloat_vs_Model_Stat_Timeseries_IOnc import ncreader
import datetime
import plotter
import plotter_oxy
from instruments import check
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import sys
sys.path.append("/g100/home/userexternal/camadio0/CA_functions/")
Check_obj = check.check("", verboselevel=0)

def get_level_depth(TheMask,lev):
    i0 = TheMask.getDepthIndex(lev)
    i1 = i0 + 1
    diff0 = lev - TheMask.zlevels[i0]
    diff1 = lev - TheMask.zlevels[i1]
    data = [(i0,diff0),(i1,diff1)]
    ix,_ = min(data, key=lambda t: t[1])
    return ix

def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2))

INDIR = addsep(args.indir)
OUTDIR = addsep(args.outdir)
BASEDIR = addsep(args.basedir)
TheMask=Mask(args.maskfile, loadtmask=False)

font_s =  13
font_s2 = 3
label_s = 15

TL = TimeList.fromfilenames(None, BASEDIR + "PROFILES/","ave*.nc")
deltaT= datetime.timedelta(hours=12)
TI = TimeInterval.fromdatetimes(TL.Timelist[0] - deltaT, TL.Timelist[-1] + deltaT)
ALL_PROFILES = bio_float.FloatSelector(None, TI, Rectangle(-6,36,30,46))
M = Matchup_Manager(ALL_PROFILES,TL,BASEDIR)

METRICS = ['Int_0-200','Corr','DCM','z_01','Nit_1','SurfVal','dNit_dz','CM','O2o_sat','OMZ','max_O2']
nStat = len(METRICS)
max_depth = get_level_depth(TheMask,60)

T_start2num = mdates.date2num(TI.start_time)
T_end2num   = mdates.date2num(TI.end_time)

plotvarname =[r'Oxy $[mmol/m^3]$']
VARLIST=['O2o']
extrap = [False]

nVar = len(VARLIST)
bt=60
depths=np.linspace(0,60,20)

sys.exit()

for ivar_m, var_mod in enumerate(VARLIST):
    var = FLOATVARS[var_mod]
    Profilelist = bio_float.FloatSelector(var, TI, Rectangle(-6,36,30,46))
    wmo_list=bio_float.get_wmo_list(Profilelist)
    
    for wmo in wmo_list:
        OUTFILE = OUTDIR + var_mod + "_" + wmo + ".png"
        print (OUTFILE)
        list_float_track=bio_float.filter_by_wmo(Profilelist,wmo)
        if ( var_mod == 'P_c'):
            fig,axes= plotter_oxy.figure_generator(list_float_track)
            ax1,ax2,ax3,ax4,ax5,ax6,ax7=axes
            xlabels = ax7.get_xticklabels()
            ax7.xaxis.grid(True)
        else:
            fig,axes= plotter.figure_generator(list_float_track)
            ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8=axes
            xlabels = ax8.get_xticklabels()
            ax8.xaxis.grid(True)

        nP = len(list_float_track)
        print (nP)
        if nP <2 : continue

        plotmat = np.zeros([len(depths), len(list_float_track)])*np.nan
        plotmat_model = np.zeros([len(depths), len(list_float_track)])*np.nan
        timelabel_list = list()

        for ip, p in enumerate(list_float_track):
            try:
                Pres,Prof,Qc=p.read(var,var_mod=var_mod)
                #print (Prof)
            except:
                #print (var_mod)
                timelabel_list.append(p.time)
                continue
            ii = Pres<=bt
            if ii.sum() < 2 :
                print ("less than 2 points")
                timelabel_list.append(p.time)
                continue

            timelabel_list.append(p.time)

            try:
              GM = M.getMatchups2([p], TheMask.zlevels, var_mod, interpolation_on_Float=False,checkobj=Check_obj, forced_depth=depths, extrapolation=extrap[ivar_m])
            except:
                print ("except")
                continue

            if GM.number()> 0:
                plotmat_model[:,ip] = GM.Model
                plotmat[      :,ip] = GM.Ref

        #print (var_mod + " " + np.str(len(timelabel_list)) +  p.available_params)

        title="FLOAT %s %s" %(p.name(), var)
        ax1.set_title(title, fontsize=18, pad=30)


        xs,ys = np.meshgrid(mdates.date2num(timelabel_list), depths)
        plotmat_m=ma.masked_invalid(plotmat)     

        # PLOT HOVMOELLER OF FLOAT
        levels = np.arange(200,261,5)
        import matplotlib.pyplot as plt
        cmap    =  plt.get_cmap('jet')
        norm    =  BoundaryNorm(levels, ncolors=cmap.N, clip=True)
        quadmesh = ax3.contourf(xs, ys, plotmat_m       , cmap=cmap ,levels=levels,  norm=norm, extend="both") 
        quadmesh = ax4.contourf(xs, ys, plotmat_model   , cmap=cmap ,levels=levels,  norm=norm, extend="both" )
        ax3.invert_yaxis()
        ax4.invert_yaxis()
        ax4.xaxis.set_major_formatter(mdates.DateFormatter("%Y%m"))

        colorbar_bottom= ax4.get_position().ymin
        colorbar_extent= ax3.get_position().ymax - colorbar_bottom
        cbaxes = fig.add_axes([0.91, colorbar_bottom , 0.02, colorbar_extent])
        cbar=fig.colorbar(quadmesh, cax = cbaxes)
        ticklabs = cbar.get_ticks()
# SECOND FIGURE ON STATISTICS:

        # READ STATISTICS FILE *.nc
        INPUT_FILE = "%s%s_%s.nc" %(INDIR, var_mod, wmo )
        A = ncreader(INPUT_FILE)
        times = timelabel_list

        model, ref =           A.plotdata(var_mod,'Int_0-200', only_good=False)
        if np.isnan(ref).all(): continue
        surf_model, surf_ref = A.plotdata(var_mod,'SurfVal', only_good=False)
        model_corr , ref_corr =A.plotdata(var_mod,'Corr', only_good=False)

        ax6.plot(times,  ref,'.b',label='FLO INTEG')
        ax6.plot(times,model,'b',label='MOD INTEG')

        ax5.plot(times,  surf_ref,'.b',label='FLOAT') #'REF SURF')
        ax5.plot(times,  surf_model,'b',label='MODEL') #'MOD SURF')

        if ( var_mod == "O2o" ):
            ax6.set_ylabel('INTG 0-200m \n $[mmol{\  } m^{-3}]$',fontsize=15)
            ax5.set_ylabel('SURF \n $[mmol{\  } m^{-3}]$',fontsize=15)
            model_Osat, ref_Osat = A.plotdata(var_mod,'O2o_sat', only_good=False)
            model_OMZ , ref_OMZ = A.plotdata(var_mod,'OMZ', only_good=False)
            model_maxO2, ref_maxO2 = A.plotdata(var_mod,'max_O2', only_good=False)
            ax5.plot(times, ref_Osat, '.r',label='O2sat (FLOAT)') #'REF OXY at SATURATION'
            ax8.plot(times, ref_OMZ, '.r',label='OMZ Flo') #'REF OMZ
            ax8.plot(times, model_OMZ, 'r',label='OMZ Mod') #'Model OMZ
            ax8.plot(times, ref_maxO2 , '.b',label='O2max Flo') #'REF maxO2
            ax8.plot(times, model_maxO2 , 'b' ,label='O2max Model') #'Mod maxO2
            ax8.set_ylim(1000,0)
            legend = ax8.legend(loc='upper left', shadow=True, fontsize=10)
        legend = ax5.legend(loc='upper left', shadow=True, fontsize=12)
        ax8.plot(times,  np.ones_like(times))
               
        times_r = times
        try:
            ax2.set_xticklabels([])
            ax3.set_xticklabels([])
            ax4.set_xticklabels([])
            ax5.set_xticklabels([])
            ax6.set_xticklabels([])
        except:
            print ("nans in figure")
        if (np.isnan(ref_corr).all() == False ):
            import matplotlib.pyplot as plt
            import matplotlib.colors as colors
            from matplotlib.colors import BoundaryNorm
            from funzioni_CA import MidpointNormalize
            cmap    =  plt.get_cmap('jet')
            levels_misfit  =   MaxNLocator(nbins=10).tick_values(0,40  )
            norm    =  BoundaryNorm(levels_misfit, ncolors=cmap.N, clip=True)
            cset1  = ax7.contourf(xs, ys, rmse(plotmat_model, plotmat_m ), cmap=cmap ,levels=levels_misfit, extend="both", norm=MidpointNormalize(midpoint=0))
        #clb     =  plt.colorbar(cset1 ax=ax7)
        #cbar_=fig.colorbar(cset1, cax = cbaxes)
        #ticklabs_ = cbar_.get_ticks()

        colorbar_bottom= ax7.get_position().ymin
        colorbar_extent= ax7.get_position().ymax - colorbar_bottom
        cbaxes = fig.add_axes([0.91, colorbar_bottom , 0.02, colorbar_extent])
        cbar=fig.colorbar(cset1, cax = cbaxes)
        ticklabs = cbar.get_ticks()
        ax7.invert_yaxis()
        ax7.set_title('RMSE O2o mean'  + str(rmse(plotmat_model, plotmat_m ).mean()) , fontsize=18, pad=30)
        xlabels = ax8.get_xticklabels()
        pl.setp(xlabels, rotation=30, fontsize=14)

        for ax in axes:ax.tick_params(axis = 'both', which = 'major', labelsize = label_s)
        for ax in axes[2:]: ax.set_xlim([T_start2num,timelabel_list[-1]])
        ax5.xaxis.grid(True)
        ax6.xaxis.grid(True)
        ax7.xaxis.grid(True)
        fig.savefig(OUTFILE)
        pl.close(fig)
