import pygeode as pyg
import pylab as pyl; pyl.ion();
import numpy as np
import matplotlib.pyplot as plt

path = "/local1/storage1/ECMWF/ERA5/sst/" 
path_s = "/local1/storage1/jml559/scripts/" 
path_e = "/local1/storage1/jml559/era5/"

year_list = [path+'era5_%d_sst_daym.nc' % a for a in range(1940,2022)] # daym = daily mean
ds = pyg.openall(year_list)
#print(ds)

# omits the 182nd day of the year during leap years
def remove_leap(v): 
    return pyg.timeutils.removeleapyears(v, omitdoy_leap=[182])
	
# computes full year climatology
def compute_climatology(sst, yrs): 
    if yrs is None:
	    yrs = (1980, 2021) # climatology base period # change as needed
	    fn = path_e + '%s_climatology.nc' % sst # make a path, fn = filename 
    else:
	    fn = path_e + '%s_climatology_%dto%d.nc' % (sst, yrs[0], yrs[1])
    time = ('1 Jan %d' % yrs[0], '31 Dec %d' % yrs[1])

    prectot_r = remove_leap(ds.vardict[sst]) 
    prectot_r = pyg.dailymean(prectot_r).rename(sst)
     
    prectot_r = prectot_r(time = time)
    prectot_c = pyg.climatology(prectot_r).rename('SST_CLIM').load()
    prectot_cs = prectot_c.fft_smooth('time', 4) # retains first 4 harmonic functions 
    pyg.save(fn, prectot_cs)

""" prectot_cs = compute_climatology('sst', (2000,2019)) # change years as needed
prectot_cs_2 = compute_climatology('sst', (1980,1999))
prectot_cs_3 = compute_climatology('sst', (1960,1979))
prectot_cs_4 = compute_climatology('sst', (1947,1959))  """







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
   sst_anom = vcomp.rename("sst_anom") 
   sst_anom = sst_anom.transpose("time","event","latitude","longitude")
   return sst_anom  

""" comp_1 = compute_composite(ds.sst,38,53,path3+"sst_climatology_2000to2019.nc")
fn1 = path3 + "sst_composite_2000to2019.nc"
pyg.save(fn1, comp_1)

comp_2 = compute_composite(ds.sst,27,38,path3+"sst_climatology_1980to1999.nc")
fn2 = path3 + "sst_composite_1980to1999.nc"
pyg.save(fn2, comp_2)

comp_3 = compute_composite(ds.sst,14,27,path3+"sst_climatology_1960to1979.nc")
fn3 = path3 + "sst_composite_1960to1979.nc"
pyg.save(fn3, comp_3) 

comp_4 = compute_composite(ds.sst,1,14,path3+"sst_climatology_1940to1959.nc")
fn4 = path3 + "sst_composite_1940to1959.nc"
pyg.save(fn4, comp_4) """

# calculate also a composite from 1940-2019, but for different base periods
# probably not what I intended to do - delete?
""" comp_5 = compute_composite(ds.sst,1,53,path3+"sst_climatology_2000to2019.nc")
fn5 = path3 + "sst_composite_1940to2019_rel_2000to2019clim.nc"
pyg.save(fn5, comp_5)

comp_6 = compute_composite(ds.sst,1,53,path3+"sst_climatology_1980to1999.nc")
fn6 = path3 + "sst_composite_1940to2019_rel_1980to1999clim.nc"
pyg.save(fn6, comp_6)

comp_7 = compute_composite(ds.sst,1,53,path3+"sst_climatology_1960to1979.nc")
fn7 = path3 + "sst_composite_1940to2019_rel_1960to1979clim.nc"
pyg.save(fn7, comp_7)

comp_8 = compute_composite(ds.sst,1,53,path3+"sst_climatology_1940to1959.nc")
fn8 = path3 + "sst_composite_1940to2019_rel_1940to1959clim.nc"
pyg.save(fn8, comp_8) """

# 20-year SST anomalies relative to whole period climatology, DJFM season 
def compute_DJFM_climatology(sst, yrs):
    if yrs is None:
	    yrs = (1980, 2021) # climatology base period # change as needed
	    fn = path3 + '%s_climatology.nc' % sst # make a path, fn = filename 
    else:
        def sel(var):
            return var(time=("1 Dec %d" % yrs[0],"1 Apr %d" % yrs[1]),l_month=(12,1,2,3))
        fn = path3 + '%s_DJFM_climatology_%dto%d.nc' % (sst, yrs[0], yrs[1])

    prectot_r = remove_leap(ds.vardict[sst])  
    prectot_r = sel(prectot_r)
    prectot_r = pyg.dailymean(prectot_r).rename(sst)

    #print(prectot_r) 
    prectot_c = pyg.climatology(prectot_r).rename('SST_CLIM').load()
    prectot_cs = prectot_c.fft_smooth('time', 4) # retains first 4 harmonic functions 
    #print(prectot_cs)
    #return None
    pyg.save(fn, prectot_cs)

""" sst_1 = compute_DJFM_climatology('sst', (1940,1960))
sst_2 = compute_DJFM_climatology('sst', (1960,1980))
sst_3 = compute_DJFM_climatology('sst', (1980,2000))
sst_4 = compute_DJFM_climatology('sst', (2000,2020)) 
sst_5 = compute_DJFM_climatology('sst', (1940,2020)) """

# consult era5 comp and plots files for what to do next
# essentially plotting four anomaly maps

""" def compute_DJF_climatology(tp, yrs): 
    if yrs is None:
	    yrs = (1980, 2021) # climatology base period # change as needed
	    fn = path + '%s_climatology.nc' % tp # make a path, fn = filename 
    else:
        def sel(var):
            return var(time=("1 Dec %d" % yrs[0],"1 Mar %d" % yrs[1]),l_month=(12,1,2)) 
        fn = path + '%s_DJF_climatology_%dto%d.nc' % (tp, yrs[0], yrs[1])
	
    prectot_r = remove_leap(ds.vardict[tp])
    prectot_r = sel(prectot_r)
    prectot_r = pyg.dailymean(prectot_r).rename(tp)

    #print(prectot_r) 
    prectot_c = pyg.climatology(prectot_r).rename('TP_CLIM').load()
    prectot_cs = prectot_c.fft_smooth('time', 4) # retains first 4 harmonic functions 
    #print(prectot_cs)
    #return None
    pyg.save(fn, prectot_cs)

#prectot_cs = compute_DJF_climatology('tp', (2000,2020))
prectot_2 = compute_DJF_climatology('tp', (1980,2000))
prectot_3 = compute_DJF_climatology('tp', (1960,1980))
prectot_4 = compute_DJF_climatology('tp', (1940,1960)) """