### all_20y_precip_anom_plots.py
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
m2_80to00 = pyg.open(path_m + "remapcon2_PRECTOTCORR_OctToMay_climatology_1980to2000.nc")
m2_00to20 = pyg.open(path_m + "remapcon2_PRECTOTCORR_OctToMay_climatology_2000to2020.nc")
e5_40to60 = pyg.open(path_e + "remapcon2_tp_OctToMay_climatology_1940to1960.nc")
e5_60to80 = pyg.open(path_e + "remapcon2_tp_OctToMay_climatology_1960to1980.nc")
e5_80to00 = pyg.open(path_e + "remapcon2_tp_OctToMay_climatology_1980to2000.nc")
e5_00to20 = pyg.open(path_e + "remapcon2_tp_OctToMay_climatology_2000to2020.nc")
j55_60to80 = pyg.open(path_j + "remapcon2_TPRAT_GDS4_SFC_ave3h_OctToMay_climatology_1960to1980.nc")
j55_80to00 = pyg.open(path_j + "remapcon2_TPRAT_GDS4_SFC_ave3h_OctToMay_climatology_1980to2000.nc")
j55_00to20 = pyg.open(path_j + "remapcon2_TPRAT_GDS4_SFC_ave3h_OctToMay_climatology_2000to2020.nc")

def plot_anom(data_list, titles, fn, conv_factor):
    cm = pyg.clfdict(cdelt=0.5, ndiv=6, nl=0, nf=2, style='seq', cmap=pyl.cm.BrBG, extend='both')

    axes = []
    pyl.ioff()
    for data, title in zip(data_list, titles):
        diff = conv_factor*data.mean("time") - mrm.MRM
        map = dict(projection="NorthPolarStereo")
        ax = pyg.showvar(diff, map=map, **cm)
        ax.axes[0].set_extent([0,359,20,90], crs=ccrs.PlateCarree())
        ax.axes[0].setp(title=title)
        axes.append(ax)

    all_axes = pyg.plot.grid([axes])
    pyl.ion()
    all_axes.render()

    path = "/local1/storage1/jml559/ssw-hydro/regridded-plots/"
    pyl.savefig(path + fn)

"""data_list = [m2_80to00.PRECTOTCORR_CLIM, m2_00to20.PRECTOTCORR_CLIM]
file = "ps_MERRA2_20yr_precip_anoms.pdf"
titles = ["1980-2000","2000-2020"]
plot_anom(data_list, titles, file, 3600*24)""" # for MERRA-2

"""data_list = [e5_40to60.TP_CLIM, e5_60to80.TP_CLIM, e5_80to00.TP_CLIM, e5_00to20.TP_CLIM]
file = "ps_ERA5_20yr_precip_anoms.pdf"
titles = ["1940-1960", "1960-1980", "1980-2000", "2000-2020"]
plot_anom(data_list, titles, file, 1000*24)""" # for ERA-5

"""data_list = [j55_60to80.TP_CLIM, j55_80to00.TP_CLIM, j55_00to20.TP_CLIM]
file = "ps_JRA55_20yr_precip_anoms.pdf"
titles = ["1960-1980", "1980-2000", "2000-2020"]
plot_anom(data_list, titles, file, 1)""" # for JRA-55

# climatology differences
"""ds_1 = pyg.open(path + "remapcon2_PRECTOTCORR_DJFM_climatology_2000to2020.nc") ###
ds_base = pyg.open("mrm_DJFM_1980to2020.nc")
#ds_base = pyg.open(path + "PRECTOTCORR_DJFM_climatology_1980to2020.nc") # base period
cm = pyg.clfdict(cdelt=0.5, ndiv=6, nl=0, nf=2, style='seq', cmap=pyl.cm.BrBG, extend='both') # both
#diff = 3600*24*(ds_1.PRECTOTCORR_CLIM.mean("time") - ds_base.PRECTOTCORR_CLIM.mean("time"))
diff = 3600*24*ds_1.PRECTOTCORR_CLIM.mean("time") - ds_base.MRM
pyl.ioff()
map = dict(projection = "NorthPolarStereo")

ax = pyg.showvar(diff, map=map, **cm) 
ax.axes[0].set_extent([0,359,20,90],crs=ccrs.PlateCarree())
ax.axes[0].setp(title = "MERRA-2 DJFM precip climo (2000-2020 minus 1980-2020 MRM)") ###
pyl.ion()
ax.render() 
ax.axes[1].ax.set_title("mm/d", y=1.05, fontsize=12) 

path = "/local1/storage1/jml559/ssw-hydro/"
fn = "ps_MERRA2_2000to2020_minus_1980to2020_precip_MRM_DJFM.pdf" ###
pyl.savefig(path + fn) """

