import pygeode as pyg
import cartopy.crs as ccrs
import pylab as pyl; pyl.ion();
import numpy as np
import matplotlib.pyplot as plt

patt = "$Y$m$d"
path = "/local1/storage1/jml559/era5/" # check

# Test comment

year_list = [path+'era5_*%d*.nc' % a for a in range(198,203)]
# climatology - do 1980 to 2021 (MERRA2)
# composites - exact same as MERRA2 for now

ds = pyg.open_multi(year_list, pattern=patt)

def remove_leap(v): 
    return pyg.timeutils.removeleapyears(v, omitdoy_leap=[182])
	# omits the 182nd day of the year during leap years

def compute_climatology(prectotcorr, yrs): 
    if yrs is None:
	    yrs = (1940, 2022) # yrs is a tuple # climatology base period # ask
	    fn = path + '%s_climatology.nc' % prectotcorr # make a path, fn = filename 
    else:
	    fn = path + '%s_climatology_%dto%d.nc' % (prectotcorr, yrs[0], yrs[1])
    time = ('1 Jan %d' % yrs[0], '31 Dec %d' % yrs[1])

    #prectot_r = remove_leap(prectot_r)
    #prectot_r = pyg.dailymean(ds.vardict[prectot]).rename(prectot)
    #print(prectot_r) # no hh:mm:dd

    prectot_r = remove_leap(ds.vardict[prectotcorr])
    prectot_r = pyg.dailymean(prectot_r).rename(prectotcorr)

    #print(prectot_r) 
    prectot_r = prectot_r(time = time)
    prectot_c = pyg.climatology(prectot_r).rename('PRECTOTCORR_CLIM') #.load()
    prectot_cs = prectot_c.fft_smooth('time', 4) # retains first 4 harmonic functions 
    #print(prectot_cs)
    #return None
    pyg.save(fn, prectot_cs)

prectot_cs = compute_climatology('PRECTOTCORR', (1980,2021))

# read ssw_dates.txt
# get a list of dates, with each date/entry as a string 
# lines 2 to 48
# Note! Will need a new list of SSW dates for era5

def compute_composite(v): # original - do not modify
   file = open('ssw_dates.txt','r')
   content = file.readlines()
   dates = content[21:48]
   print(dates)
   #print(len(dates))

   #yrs = (1980, 2020) # not needed???
   #vc = compute_climatology(v, yrs) # not needed???
   file2 = pyg.open(path+'PRECTOTCORR_climatology_1980to2021.nc')  # naming issue
   vclim = pyg.dailymean(file2.PRECTOTCORR_CLIM)

   vr = remove_leap(v)
   vrd = pyg.dailymean(vr).rename(vr.name)
   
   va = vrd - vclim # va = anomaly
   print("va:")
   print(va)
   print("vrd:")
   print(vrd)
   print("vclim:")
   print(vclim)

   vcomp = va.composite(l_time = dates, evlen = 140, evoff = 40)
   prectotcorr_anom = vcomp.rename("prectotcorr_anom")
   return prectotcorr_anom 
prectotcorr_comp = compute_composite(ds.PRECTOTCORR) 

fn2 = path + 'prectotcorr_composite.nc'
print(fn2)
pyg.save(fn2, prectotcorr_comp)  
#print(prectot_comp)
#pyg.showvar(prectot_comp(time=(-40,0), lat=40, lon=-70))