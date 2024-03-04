import pygeode as pyg
import pylab as pyl; pyl.ion();
import numpy as np
import matplotlib.pyplot as plt

#patt = "$Y$m$d"
path = "/local1/storage1/ECMWF/ERA5/sst/" 
path2 = "/local1/storage1/jml559/scripts/" 
path3 = "/local1/storage1/jml559/era5/"

year_list = [path+'era5_%d_sst_daym.nc' % a for a in range(1940,2022)] # daym = daily mean

ds = pyg.openall(year_list)
#print(ds)

def remove_leap(v): 
    return pyg.timeutils.removeleapyears(v, omitdoy_leap=[182])
	# omits the 182nd day of the year during leap years

def compute_climatology(sst, yrs): 
    if yrs is None:
	    yrs = (1980, 2021) # climatology base period # change as needed
	    fn = path3 + '%s_climatology.nc' % sst # make a path, fn = filename 
    else:
	    fn = path3 + '%s_climatology_%dto%d.nc' % (sst, yrs[0], yrs[1])
    time = ('1 Jan %d' % yrs[0], '31 Dec %d' % yrs[1])

    #prectot_r = remove_leap(prectot_r)
    #prectot_r = pyg.dailymean(ds.vardict[prectot]).rename(prectot)
    #print(prectot_r) # no hh:mm:dd

    prectot_r = remove_leap(ds.vardict[sst]) 
    prectot_r = pyg.dailymean(prectot_r).rename(sst)

    #print(prectot_r) 
    prectot_r = prectot_r(time = time)
    prectot_c = pyg.climatology(prectot_r).rename('SST_CLIM').load()
    prectot_cs = prectot_c.fft_smooth('time', 4) # retains first 4 harmonic functions 
    #print(prectot_cs)
    #return None
    pyg.save(fn, prectot_cs)

""" prectot_cs = compute_climatology('sst', (2000,2019)) # change years as needed
prectot_cs_2 = compute_climatology('sst', (1980,1999))
prectot_cs_3 = compute_climatology('sst', (1960,1979))
prectot_cs_4 = compute_climatology('sst', (1947,1959))  """

# read ssw_dates.txt
# get a list of dates, with each date/entry as a string 
# lines 2 to 48
# Note! Will need a new list of SSW dates for era5 """

def compute_composite(v,i1,i2,climo_fn):  
   file = open(path2+'ssw_dates.txt','r')
   content = file.readlines()
   dates = content[i1:i2]
   #print(dates)
   #print(len(dates))

   #yrs = (1980, 2020) # not needed???
   #vc = compute_climatology(v, yrs) # not needed???
   file2 = pyg.open(climo_fn)  
   vclim = pyg.dailymean(file2.SST_CLIM)

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
   tp_anom = vcomp.rename("tp_anom") # REPLACE TP WITH SST
   tp_anom = tp_anom.transpose("time","event","latitude","longitude")
   return tp_anom  

""" tp_comp_1 = compute_composite(ds.tp,38,53,path+"tp_climatology_2000to2019.nc") 
fn1 = path + "tp_composite_2000to2019.nc"
print(fn1)
pyg.save(fn1, tp_comp_1) """

""" tp_comp_2 = compute_composite(ds.tp,27,38,path+"tp_climatology_1980to1999.nc") 
fn2 = path + "tp_composite_1980to1999.nc"
print(fn2)
pyg.save(fn2, tp_comp_2)

tp_comp_3 = compute_composite(ds.tp,14,27,path+"tp_climatology_1960to1979.nc") 
fn3 = path + "tp_composite_1960to1979.nc"
print(fn3)
pyg.save(fn3, tp_comp_3) """

""" tp_comp_4 = compute_composite(ds.tp,7,14,path+"tp_climatology_1947to1959.nc") 
fn4 = path + "tp_composite_1947to1959.nc"
print(fn4)
pyg.save(fn4, tp_comp_4) """