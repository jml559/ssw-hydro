### plots time series of area-averaged precip anoms vs. event for all three reanalyses

import pygeode as pyg
import cartopy.crs as ccrs
import pylab as pyl; pyl.ion();
import numpy as np
import matplotlib.pyplot as plt
import random 

path_e = "/local1/storage1/jml559/era5/"
path_m = "/local1/storage1/jml559/merra2/"
path_j = "/local1/storage1/jml559/jra55/"

# composites relative to a running climatology
era5_bef = pyg.open(path_e + "remapcon2_before_SSWs_OctToMay_eventlatlon_1940to2020.nc")
era5_aft = pyg.open(path_e + "remapcon2_after_SSWs_OctToMay_eventlatlon_1940to2020.nc")
merra2_bef = pyg.open(path_m + "remapcon2_before_SSWs_OctToMay_eventlatlon_1980to2020.nc")
merra2_aft = pyg.open(path_m + "remapcon2_after_SSWs_OctToMay_eventlatlon_1980to2020.nc")
jra55_bef = pyg.open(path_j + "remapcon2_before_SSWs_OctToMay_eventlatlon_1960to2020.nc")
jra55_aft = pyg.open(path_j + "remapcon2_after_SSWs_OctToMay_eventlatlon_1960to2020.nc")

# do I have composites (Oct to May) relative to a fixed climo?
# find them, or else make them

# plots time series of area-averaged precip anoms vs. event
def plot_ts(lat1, lat2, lon1, lon2):


# compute an area-averaged
# Iberia: 36°N-44°N, 10°W-1°W