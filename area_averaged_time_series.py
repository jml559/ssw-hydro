### plots time series of area-averaged precip anoms vs. event for all three reanalyses
### regression analyses 

import pygeode as pyg
import cartopy.crs as ccrs
import pylab as pyl; pyl.ion();
import numpy as np
import matplotlib.pyplot as plt
import random 

path_e = "/local1/storage1/jml559/era5/"
path_m = "/local1/storage1/jml559/merra2/"
path_j = "/local1/storage1/jml559/jra55/tprat/"

# composites relative to a running climatology
era5_bef = pyg.open(path_e + "remapcon2_before_SSWs_OctToMay_eventlatlon_1940to2020.nc")
era5_aft = pyg.open(path_e + "remapcon2_after_SSWs_OctToMay_eventlatlon_1940to2020.nc")
merra2_bef = pyg.open(path_m + "remapcon2_before_SSWs_OctToMay_eventlatlon_1980to2020.nc")
merra2_aft = pyg.open(path_m + "remapcon2_after_SSWs_OctToMay_eventlatlon_1980to2020.nc")
jra55_bef = pyg.open(path_j + "remapcon2_before_SSWs_OctToMay_eventlatlon_1960to2020.nc")
jra55_aft = pyg.open(path_j + "remapcon2_after_SSWs_OctToMay_eventlatlon_1960to2020.nc")

# composites relative to a fixed climatology 
""" era5_comp = pyg.open(path_e + "remapcon2_tp_OctToMay_composite_1940to2020_rel_1980to2020.nc")
merra2_comp = pyg.open(path_m + "remapcon2_PRECTOTCORR_OctToMay_composite_1940to2020_rel_1980to2020.nc")
jra55_comp = pyg.open(path_j + "remapcon2_TPRAT_OctToMay_composite_1960to2020_rel_1980to2020.nc") """

# plots time series of area-averaged precip anoms vs. event
def plot_ts(lat1, lat2, lon1, lon2, region, path):
    # before SSWs (running climo)
    era5_bef_arr = era5_bef.prectotcorr_comp(lat=(lat1,lat2),lon=(lon1,lon2)).mean("latitude","longitude")[:]
    merra2_bef_arr = merra2_bef.prectotcorr_comp(lat=(lat1,lat2),lon=(lon1,lon2)).mean("latitude","longitude")[:]
    jra55_bef_arr = jra55_bef.tprat_comp(lat=(lat1,lat2),lon=(lon1,lon2)).mean("latitude","longitude")[:]

    # after SSWs (running climo)
    era5_aft_arr = era5_aft.prectotcorr_comp(lat=(lat1,lat2),lon=(lon1,lon2)).mean("latitude","longitude")[:]
    merra2_aft_arr = merra2_aft.prectotcorr_comp(lat=(lat1,lat2),lon=(lon1,lon2)).mean("latitude","longitude")[:]
    jra55_aft_arr = jra55_aft.tprat_comp(lat=(lat1,lat2),lon=(lon1,lon2)).mean("latitude","longitude")[:] 

    """# before SSWs (fixed climo)
    era5_bef_arr = era5_comp.tp_anom(lat=(lat1,lat2),lon=(lon1,lon2),
        time=(-40,0)).mean("latitude","longitude").nanmean('time')[:]
    merra2_bef_arr = merra2_comp.prectotcorr_anom(lat=(lat1,lat2),lon=(lon1,lon2),
        time=(-40,0)).mean("latitude","longitude").nanmean('time')[:]
    jra55_bef_arr = jra55_comp.tp_anom(lat=(lat1,lat2),lon=(lon1,lon2),
        time=(-40,0)).mean("latitude","longitude").nanmean('time')[:]

    # after SSWs (fixed climo)
    era5_aft_arr = era5_comp.tp_anom(lat=(lat1,lat2),lon=(lon1,lon2),
        time=(0,61)).mean("latitude","longitude").nanmean('time')[:]
    merra2_aft_arr = merra2_comp.prectotcorr_anom(lat=(lat1,lat2),lon=(lon1,lon2),
        time=(0,61)).mean("latitude","longitude").nanmean('time')[:]
    jra55_aft_arr = jra55_comp.tp_anom(lat=(lat1,lat2),lon=(lon1,lon2),
        time=(0,61)).mean("latitude","longitude").nanmean('time')[:]"""

    # pad time series with leading NaNs 
    def pad_ts(series, max_len=52):
        padded = np.full(max_len, np.nan)
        padded[-len(series):] = series
        return padded
    
    era5_bef_arr = 1000*24*pad_ts(era5_bef_arr)
    merra2_bef_arr = 3600*24*pad_ts(merra2_bef_arr)
    jra55_bef_arr = pad_ts(jra55_bef_arr)
    era5_aft_arr = 1000*24*pad_ts(era5_aft_arr)
    merra2_aft_arr = 3600*24*pad_ts(merra2_aft_arr)
    jra55_aft_arr = pad_ts(jra55_aft_arr)

    fig, ax = plt.subplots(1, 2, figsize=(10, 4.5), sharey=True)
    x_axis = np.arange(1,53)

    # resample ERA-5 data
    """resample_bef_all = np.zeros(())
    resample_aft_all = 
    resample_bef_1980 = 
    resample_aft_1980 = 
    resample_bef_2000 = 
    resample_aft_2000 =  """

    # colors from https://s-rip.github.io/report/colourdefinition.html 
    ax[0].plot(x_axis, era5_bef_arr, label='ERA-5', color="#5F98C6") 
    ax[0].plot(x_axis, merra2_bef_arr, label='MERRA-2', color="#E21F26")
    ax[0].plot(x_axis, jra55_bef_arr, label='JRA-55', color="#723B7A")
    #ax[0].axhline(-1, color="#CB9A4C", linestyle='--', linewidth=1)
    #ax[0].axhline(1, color="#52ACA1", linestyle='--', linewidth=1)
    """ax[0].axhline(0, color='black', linestyle='--', linewidth=1)
    ax[0].axvline(14.5, color='gray', linestyle='--', linewidth=1)
    ax[0].axvline(27.5, color='gray', linestyle='--', linewidth=1)
    ax[0].axvline(38.5, color='gray', linestyle='--', linewidth=1)
    ax[0].set_xticks([1, 11, 21, 31, 41, 51]) 
    ax[0].set_xlabel('Event')
    ax[0].set_ylabel('Area-averaged anomaly (mm/d)')
    ax[0].set_ylim(-4, 4)
    ax[0].set_title('Before SSWs', fontsize=14)
    ax[0].text(13, -3.8, "1960", rotation='vertical', fontweight="bold")
    ax[0].text(26, -3.8, "1980", rotation='vertical', fontweight="bold")
    ax[0].text(37, -3.8, "2000", rotation='vertical', fontweight="bold")
    ax[0].legend()"""

    ax[1].plot(x_axis, era5_aft_arr, label='ERA-5', color="#5F98C6") 
    ax[1].plot(x_axis, merra2_aft_arr, label='MERRA-2', color="#E21F26")
    ax[1].plot(x_axis, jra55_aft_arr, label='JRA-55', color="#723B7A")
    #ax[1].axhline(-1, color="#CB9A4C", linestyle='--', linewidth=1)
    #ax[1].axhline(1, color="#52ACA1", linestyle='--', linewidth=1)
    for i in range(2):
        ax[i].axhline(0, color='black', linestyle='--', linewidth=1)
        ax[i].axvline(14.5, color='gray', linestyle='--', linewidth=1)
        ax[i].axvline(27.5, color='gray', linestyle='--', linewidth=1)
        ax[i].axvline(38.5, color='gray', linestyle='--', linewidth=1)
        ax[i].set_xticks([1, 11, 21, 31, 41, 51]) 
        ax[i].set_xlabel('Event')
        ax[i].set_ylabel('Area-averaged anomaly (mm/d)')
        ax[i].set_ylim(-4, 4)
        #ax[i].set_title('After SSWs', fontsize=14)
        ax[i].text(13, -3.8, "1960", rotation='vertical', fontweight="bold")
        ax[i].text(26, -3.8, "1980", rotation='vertical', fontweight="bold")
        ax[i].text(37, -3.8, "2000", rotation='vertical', fontweight="bold")
        ax[i].legend()

    plt.suptitle("Area-averaged precip anomalies, " + region, fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()
    pyl.savefig(path)

# running climo
""" plot_ts(36, 44, 350, 359, "Iberia (running climo)", 
    "/local1/storage1/jml559/ssw-hydro/iberia_runningclimo_ts.pdf")
plot_ts(55, 70, 4, 20, "Scandinavia (running climo)",
    "/local1/storage1/jml559/ssw-hydro/scandinavia_runningclimo_ts.pdf")
plot_ts(45, 55, 225, 238, "Pac NW (running climo)",
    "/local1/storage1/jml559/ssw-hydro/PacNW_runningclimo_ts.pdf") """

# fixed climo
""" plot_ts(36, 44, 350, 359, "Iberia (relative to 1980-2020 climatology)", 
    "/local1/storage1/jml559/ssw-hydro/iberia_rel1980to2020_ts.pdf")
plot_ts(55, 70, 4, 20, "Scandinavia (relative to 1980-2020 climatology)",
    "/local1/storage1/jml559/ssw-hydro/scandinavia_rel1980to2020_ts.pdf")
plot_ts(45, 55, 225, 238, "Pac NW (relative to 1980-2020 climatology)",
    "/local1/storage1/jml559/ssw-hydro/PacNW_rel1980to2020_ts.pdf") """




    






   

