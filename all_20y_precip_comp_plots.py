### all_20y_precip_comp_plots.py
# computes 20-year Oct to May precipitation anomalies
# Relative to Oct to May multi-reanalysis mean precipitation in 1980-2020

import pygeode as pyg
import pylab as pyl; pyl.ion();
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

mrm = pyg.open("/local1/storage1/jml559/ssw-hydro/mrm_OctToMay_2000to2020.nc")
path_m = "/local1/storage1/jml559/merra2/"
path_e = "/local1/storage1/jml559/era5/"
path_j = "/local1/storage1/jml559/jra55/tprat/"

m2_bef = [pyg.open(path_m + "remapcon2_before_SSWs_OctToMay_1980to2000.nc").prectotcorr_comp,
            pyg.open(path_m + "remapcon2_before_SSWs_OctToMay_2000to2020.nc").prectotcorr_comp]
m2_aft = [pyg.open(path_m + "remapcon2_after_SSWs_OctToMay_1980to2000.nc").prectotcorr_comp,
            pyg.open(path_m + "remapcon2_after_SSWs_OctToMay_2000to2020.nc").prectotcorr_comp]
e5_bef = [pyg.open(f"{path_e}remapcon2_before_SSWs_OctToMay_{a}to{a+20}.nc").prectotcorr_comp 
            for a in np.arange(1940,2001,20)]
e5_aft = [pyg.open(f"{path_e}remapcon2_after_SSWs_OctToMay_{a}to{a+20}.nc").prectotcorr_comp 
            for a in np.arange(1940,2001,20)]
j5_bef = [pyg.open(f"{path_j}remapcon2_before_SSWs_OctToMay_{a}to{a+20}.nc").tprat_comp 
            for a in np.arange(1960,2001,20)]
j5_aft = [pyg.open(f"{path_j}remapcon2_after_SSWs_OctToMay_{a}to{a+20}.nc").tprat_comp 
            for a in np.arange(1960,2001,20)]

def plot_comp(data_list, titles, fn, conv_factor):
    cm = pyg.clfdict(cdelt=0.5, ndiv=6, nl=0, nf=2, style='seq', cmap=pyl.cm.BrBG, extend='both')

    axes = []
    pyl.ioff()
    for data, title in zip(data_list, titles):
        comp = conv_factor*data # comp is in units of mm/d
        map = dict(projection="NorthPolarStereo")
        ax = pyg.showvar(comp, map=map, **cm)
        ax.axes[0].set_extent([0,359,20,90], crs=ccrs.PlateCarree())
        ax.axes[0].setp(title=title)
        axes.append(ax)

    all_axes = pyg.plot.grid([axes])
    pyl.ion()
    all_axes.render()

    path = "/local1/storage1/jml559/ssw-hydro/regridded-plots/"
    pyl.savefig(path + fn)

titles = ["1980-2000","2000-2020"]
plot_comp(m2_bef, titles, "ps_MERRA2_before_SSWs_all.pdf", 3600*24)
plot_comp(m2_aft, titles, "ps_MERRA2_after_SSWs_all.pdf", 3600*24)
print("Done")

titles = ["1940-1960", "1960-1980", "1980-2000", "2000-2020"]
plot_comp(e5_bef, titles, "ps_ERA5_before_SSWs_all.pdf", 1000*24)
plot_comp(e5_aft, titles, "ps_ERA5_after_SSWs_all.pdf", 1000*24)
print("Done")

titles = ["1960-1980", "1980-2000", "2000-2020"]
plot_comp(j5_bef, titles, "ps_JRA55_before_SSWs_all.pdf", 1)
plot_comp(j5_aft, titles, "ps_JRA55_after_SSWs_all.pdf", 1)
print("Done")



"""data_list = [m2_80to00.PRECTOTCORR_CLIM, m2_00to20.PRECTOTCORR_CLIM]
file = "ps_MERRA2_20yr_precip_anoms.pdf"
titles = ["1980-2000","2000-2020"]
plot_anom(data_list, titles, file, 3600*24)""" # for MERRA-2

#e5_bef = [pyg.open(path_e + "remapcon2_tp_OctToMay_climatology_%dto%d.nc") % (a, a+20) for a in np.arange(1940,2000,10)]

#year_list = [path+'era5_*%d*.nc' % a for a in range(194,203)]