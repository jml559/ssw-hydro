### plots area-averaged precip vs. NAO, NinoSST and N Pac SST indices

import pygeode as pyg
import cartopy.crs as ccrs
import pylab as pyl; pyl.ion();
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

path_e = "/local1/storage1/jml559/era5/"
path_m = "/local1/storage1/jml559/merra2/"
path_j = "/local1/storage1/jml559/jra55/tprat/"
index_data = pyg.open("/local1/storage1/jml559/era5/ERA5_52SSWs_NAO_Nino34_NPacDipole_indices.nc")

# composites relative to a running climatology
era5_bef = pyg.open(path_e + "remapcon2_before_SSWs_OctToMay_eventlatlon_1940to2020.nc")
era5_aft = pyg.open(path_e + "remapcon2_after_SSWs_OctToMay_eventlatlon_1940to2020.nc")

# plots scatterplot of some index vs. area-averaged precip anom 
def index_vs_prec_anom(lat1, lat2, lon1, lon2, index_bef, index_aft, index_str, region, path):
    era5_bef_arr = era5_bef.prectotcorr_comp(lat=(lat1,lat2),lon=(lon1,lon2)).mean("latitude","longitude")[:]
    era5_aft_arr = era5_aft.prectotcorr_comp(lat=(lat1,lat2),lon=(lon1,lon2)).mean("latitude","longitude")[:]

    # pad time series with leading NaNs 
    def pad_ts(series, max_len=52):
        padded = np.full(max_len, np.nan)
        padded[-len(series):] = series
        return padded
    
    era5_bef_arr = 1000*24*pad_ts(era5_bef_arr)
    era5_aft_arr = 1000*24*pad_ts(era5_aft_arr)

    # get index_bef and index_aft variables (must be specified in function call)
    index_bef_arr = index_bef[:]
    index_aft_arr = index_aft[:]

    fig, ax = plt.subplots(1, 2, figsize=(10, 4.5), sharey=True)
    #fig, ax = plt.subplots(1, 3, figsize=(15, 4.5), sharey=True)

    def linreg(x,y): # give coefficients and R^2 score from linear regression
        x = x.reshape(-1, 1)
        model = LinearRegression().fit(x,y)
        y_pred = model.predict(x)
        m = model.coef_[0]
        b = model.intercept_
        r2 = r2_score(y, y_pred)
        return y_pred, m, b, r2

    (pred_anom_bef, m_bef, b_bef, r2_bef) = linreg(index_bef_arr, era5_bef_arr)
    (pred_anom_aft, m_aft, b_aft, r2_aft) = linreg(index_aft_arr, era5_aft_arr)
    #(pred_anom_3, m3, b3, r2_3) = linreg(index_bef_arr, era5_aft_arr)

    ax[0].scatter(index_bef_arr, era5_bef_arr)
    ax[0].plot(index_bef_arr, pred_anom_bef)
    ax[0].scatter(index_bef_arr[14:27], era5_bef_arr[14:27],label="1960-1980",color="green")
    ax[0].scatter(index_bef_arr[27:38], era5_bef_arr[27:38],label="1980-2000",color="orange")
    ax[0].text(0.5,-3.3,"y = %.2fx + %.2f" % (m_bef, b_bef))
    ax[0].text(0.5,-3.8,"$R^2$: %.2f" % r2_bef)
    ax[0].legend()
    ax[0].set_title('Before SSWs, [-40,-1] days', fontsize=14)

    ax[1].scatter(index_aft_arr, era5_aft_arr)
    ax[1].plot(index_aft_arr, pred_anom_aft)
    ax[1].scatter(index_aft_arr[14:27], era5_aft_arr[14:27],label="1960-1980",color="green")
    ax[1].scatter(index_aft_arr[27:38], era5_aft_arr[27:38],label="1980-2000",color="orange")
    ax[1].text(0.5,-3.3,"y = %.2fx + %.2f" % (m_aft, b_aft))
    ax[1].text(0.5,-3.8,"$R^2$: %.2f" % r2_aft)
    ax[1].legend()
    ax[1].set_title('After SSWs, [0,60] days', fontsize=14)

    """ax[2].scatter(index_bef_arr, era5_aft_arr)
    ax[2].plot(index_bef_arr, pred_anom_3)
    ax[2].scatter(index_bef_arr[14:27], era5_aft_arr[14:27],label="1960-1980",color="green")
    ax[2].scatter(index_bef_arr[27:38], era5_aft_arr[27:38],label="1980-2000",color="orange")
    ax[2].text(0.5,-3.3,"y = %.2fx + %.2f" % (m3, b3))
    ax[2].text(0.5,-3.8,"$R^2$: %.2f" % r2_3)
    ax[2].legend()
    ax[2].set_title('After-SSW Precip vs. Before-SSW Index', fontsize=14)"""

    for i in range(2):
        ax[i].axhline(0, color="black")
        ax[i].axvline(0, color="black")
        ax[i].set_xlim(-2.1,2.1)
        ax[i].set_ylim(-4.3,4.3)
        ax[i].set_xlabel(f"Average {index_str} index")
        ax[i].set_ylabel("Area-averaged anomaly (mm/d)")

    plt.suptitle(f"Precip anomalies in {region} versus {index_str}", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()
    pyl.savefig(path)

index_vs_prec_anom(36, 44, 350, 359, index_data.NAO_N40N1, index_data.NAO_P0P60,
    "NAO", "Iberia", "/local1/storage1/jml559/ssw-hydro/NAO_iberia_regr.pdf")
index_vs_prec_anom(36, 44, 350, 359, index_data.Nino34SST_N40N1, index_data.Nino34SST_N40N1,
    "Nino3.4 SST anomaly", "Iberia", "/local1/storage1/jml559/ssw-hydro/Nino34SST_iberia_regr.pdf")
index_vs_prec_anom(36, 44, 350, 359, index_data.NPacSST_N40N1, index_data.NPacSST_N40N1,
    "N Pac SST anomaly", "Iberia", "/local1/storage1/jml559/ssw-hydro/NPacSST_iberia_regr.pdf")

index_vs_prec_anom(55, 70, 4, 20, index_data.NAO_N40N1, index_data.NAO_P0P60,
    "NAO", "Scandinavia", "/local1/storage1/jml559/ssw-hydro/NAO_scandinavia_regr.pdf")
index_vs_prec_anom(55, 70, 4, 20, index_data.Nino34SST_N40N1, index_data.Nino34SST_N40N1,
    "Nino3.4 SST anomaly", "Scandinavia", "/local1/storage1/jml559/ssw-hydro/Nino34SST_scandinavia_regr.pdf")
index_vs_prec_anom(55, 70, 4, 20, index_data.NPacSST_N40N1, index_data.NPacSST_N40N1,
    "N Pac SST anomaly", "Scandinavia", "/local1/storage1/jml559/ssw-hydro/NPacSST_scandinavia_regr.pdf")

index_vs_prec_anom(45, 55, 225, 238, index_data.NAO_N40N1, index_data.NAO_P0P60,
    "NAO", "Pac NW", "/local1/storage1/jml559/ssw-hydro/NAO_PacNW_regr.pdf")
index_vs_prec_anom(45, 55, 225, 238, index_data.Nino34SST_N40N1, index_data.Nino34SST_N40N1,
    "Nino3.4 SST anomaly", "Pac NW", "/local1/storage1/jml559/ssw-hydro/Nino34SST_PacNW_regr.pdf")
index_vs_prec_anom(45, 55, 225, 238, index_data.NPacSST_N40N1, index_data.NPacSST_N40N1,
    "N Pac SST anomaly", "Pac NW", "/local1/storage1/jml559/ssw-hydro/NPacSST_PacNW_regr.pdf")



# capture these first
# then mark 1960-1980 (green) - 14:27
# 1980-2000 (orange) - 27:38 
# legend 