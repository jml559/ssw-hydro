import pygeode as pyg
import pylab as pyl; pyl.ion();
import numpy as np

# open filepaths
path_merra2 = "/local1/storage1/jml559/merra2/remapcon2_PRECTOTCORR_OctToMay_climatology_2000to2020.nc"
path_era5 = "/local1/storage1/jml559/era5/remapcon2_tp_OctToMay_climatology_2000to2020.nc"
path_jra55 = "/local1/storage1/jml559/jra55/tprat/remapcon2_TPRAT_GDS4_SFC_ave3h_OctToMay_climatology_2000to2020.nc"

ds_merra2 = pyg.open(path_merra2)
ds_era5 = pyg.open(path_era5)
ds_jra55 = pyg.open(path_jra55)

# convert all to mm/d
ds_merra2 = 3600*24*ds_merra2.PRECTOTCORR_CLIM.mean("time")
ds_era5 = 1000*24*ds_era5.TP_CLIM.mean("time")
ds_jra55 = ds_jra55.TP_CLIM.mean("time") #.mean("forecast_time1")

#pyg.showvar(3600*24*ds_merra2.PRECTOTCORR_CLIM(time=0))
#pyg.showvar(1000*24*ds_era5.TP_CLIM(time=0))
#pyg.showvar(ds_jra55.TP_CLIM.mean("forecast_time1")) 

# multi-reanalysis mean 
mrm = (1/3)*(ds_merra2 + ds_era5 + ds_jra55)
mrm_arr = np.where(mrm[:,:] < 0, np.nan, mrm[:,:])

lat = pyg.Lat(np.linspace(-89.5, 89.5, 180))
lon = pyg.Lon(np.linspace(0, 359, 360))

MRM = pyg.Var((lat, lon), values=mrm_arr, name="MRM")
pyg.save("mrm_OctToMay_2000to2020.nc", MRM)
print("Saved")
#pyg.showvar(MRM)










#mrm_array = np.array(mrm)
#print(mrm_array.shape)
#mrm_array = np.where(mrm_array < 0, np.nan, mrm_array)
#print(mrm_array)

#mrm = pyg.Var(mrm_array, name="mrm")
#print(mrm)

#mrm[mrm < 0] = np.nan
#print(mrm)
#print(mrm)
#print(mrm.min())
#pyg.showvar(mrm)

"""print(ds_merra2.PRECTOTCORR_CLIM)
print(ds_jra55.TP_CLIM.mean("forecast_time1"))
print(ds_era5)"""
#print(pyg.open("/local1/storage1/yd385/forJonathan/remapscon2_Lon360Lat180_tp_climatology_1980to2021.nc").lon[:])

