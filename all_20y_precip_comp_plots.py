### all_20y_precip_comp_plots.py
# plots composite anomalies relative to a moving/weighted climatology
# plots RMSE of anomalies relative to multi-reanalysis mean for that period

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

# compute composite anomalies 
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

# compute multi-reanalysis mean composite
"""_60to80_bef = (1000*24*e5_bef[1] + j5_bef[0])/2
_60to80_aft = (1000*24*e5_aft[1] + j5_aft[0])/2
_80to00_bef = (3600*24*m2_bef[0] + 1000*24*e5_bef[2] + j5_bef[1])/3
_80to00_aft = (3600*24*m2_aft[0] + 1000*24*e5_aft[2] + j5_aft[1])/3
_00to20_bef = (3600*24*m2_bef[1] + 1000*24*e5_bef[3] + j5_bef[2])/3
_00to20_aft = (3600*24*m2_aft[1] + 1000*24*e5_aft[3] + j5_aft[2])/3

n_gridpoints = 360*180

# plot differences and compute RMSD
def plot_diff_and_rmsd(data_list, mrm_list, titles, fn, conv_factor):
    cm = pyg.clfdict(cdelt=0.2, ndiv=6, nl=0, nf=2, style='seq', cmap=pyl.cm.PuOr, extend='both')

    axes = []
    pyl.ioff()
    for data, mrm, title in zip(data_list, mrm_list, titles):
        comp = conv_factor*data # comp is in units of mm/d
        diff = comp - mrm 
        rmsd = np.round(np.sqrt(np.sum((comp - mrm)**2)/n_gridpoints),2)

        map = dict(projection="NorthPolarStereo")
        ax = pyg.showvar(diff, map=map, **cm)
        ax.axes[0].set_extent([0,359,20,90], crs=ccrs.PlateCarree())
        ax.axes[0].text(0.02, 0.02, f"RMSD: {rmsd} mm/d", transform="Axes", 
            fontweight="bold", fontsize=18) # to be fixed
        ax.axes[0].setp(title=title)
        axes.append(ax)

    all_axes = pyg.plot.grid([axes])
    pyl.ion()
    all_axes.render()

    path = "/local1/storage1/jml559/ssw-hydro/regridded-plots/"
    pyl.savefig(path + fn) """
        
"""titles = ["1980-2000", "2000-2020"]
mrm_list_bef = [_80to00_bef, _00to20_bef]
mrm_list_aft = [_80to00_aft, _00to20_aft]
plot_diff_and_rmsd(m2_bef, mrm_list_bef, titles, "ps_MERRA2_diff_before_SSWs_all.pdf", 3600*24)
plot_diff_and_rmsd(m2_aft, mrm_list_aft, titles, "ps_MERRA2_diff_after_SSWs_all.pdf", 3600*24)
print("Done") """

# uncomment later + check if plots look sensible
"""titles = ["1960-1980", "1980-2000", "2000-2020"]
mrm_list_bef = [_60to80_bef, _80to00_bef, _00to20_bef]
mrm_list_aft = [_60to80_aft, _80to00_aft, _00to20_aft]

plot_diff_and_rmsd(e5_bef, mrm_list_bef, titles, "ps_ERA5_diff_before_SSWs_all.pdf", 1000*24)
plot_diff_and_rmsd(e5_aft, mrm_list_aft, titles, "ps_ERA5_diff_after_SSWs_all.pdf", 1000*24)
print("Done")
plot_diff_and_rmsd(j5_bef, mrm_list_bef, titles, "ps_JRA55_diff_before_SSWs_all.pdf", 1)
plot_diff_and_rmsd(j5_aft, mrm_list_aft, titles, "ps_JRA55_diff_after_SSWs_all.pdf", 1)
print("Done")"""


