import pygeode as pyg
import pylab as pyl; pyl.ion();
import numpy as np
import matplotlib.pyplot as plt

#patt = "$Y$m$d"
path = "/local1/storage1/jml559/era5/" 
path2 = "/local1/storage1/jml559/scripts/"

year_list = [path+'era5_*%d*.nc' % a for a in range(194,203)] 

ds = pyg.openall(year_list)
#print(ds)

def remove_leap(v): 
    return pyg.timeutils.removeleapyears(v, omitdoy_leap=[182])
	# omits the 182nd day of the year during leap years

def compute_climatology(tp, yrs): 
    if yrs is None:
	    yrs = (1980, 2021) # climatology base period # change as needed
	    fn = path + '%s_climatology.nc' % tp # make a path, fn = filename 
    else:
	    fn = path + '%s_climatology_%dto%d.nc' % (tp, yrs[0], yrs[1])
    time = ('1 Jan %d' % yrs[0], '31 Dec %d' % yrs[1])

    #prectot_r = remove_leap(prectot_r)
    #prectot_r = pyg.dailymean(ds.vardict[prectot]).rename(prectot)
    #print(prectot_r) # no hh:mm:dd

    prectot_r = remove_leap(ds.vardict[tp])
    prectot_r = pyg.dailymean(prectot_r).rename(tp)

    #print(prectot_r) 
    prectot_r = prectot_r(time = time)
    prectot_c = pyg.climatology(prectot_r).rename('TP_CLIM').load()
    prectot_cs = prectot_c.fft_smooth('time', 4) # retains first 4 harmonic functions 
    #print(prectot_cs)
    #return None
    pyg.save(fn, prectot_cs)

#prectot_cs = compute_climatology('tp', (2000,2019)) # change years as needed
#prectot_cs_2 = compute_climatology('tp', (1980,1999))
#prectot_cs_3 = compute_climatology('tp', (1960,1979))
#prectot_cs_4 = compute_climatology('tp', (1947,1959))  

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

# read ssw_dates.txt
# get a list of dates, with each date/entry as a string 
# lines 2 to 48
# Note! Will need a new list of SSW dates for era5 """

""" def compute_composite(v,i1,i2,climo_fn):  
   file = open(path2+'ssw_dates.txt','r')
   content = file.readlines()
   dates = content[i1:i2]
   #print(dates)
   #print(len(dates))

   #yrs = (1980, 2020) # not needed???
   #vc = compute_climatology(v, yrs) # not needed???
   file2 = pyg.open(climo_fn)  
   vclim = pyg.dailymean(file2.TP_CLIM)

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
   tp_anom = vcomp.rename("tp_anom")
   tp_anom = tp_anom.transpose("time","event","latitude","longitude")
   return tp_anom """

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

 
#print(prectot_comp)
#pyg.showvar(prectot_comp(time=(-40,0), lat=40, lon=-70)) 


# 1958 to 1980 SSWs (relative to 1980-2021 climatology)
""" year_list = [path+'era5_*%d*.nc' % a for a in range(195,199)] 
ds = pyg.openall(year_list)
 
def remove_leap(v): 
    return pyg.timeutils.removeleapyears(v, omitdoy_leap=[182])

def compute_composite(v):  
   file = open(path2+'ssw_dates.txt','r')
   content = file.readlines()
   dates = content[7:22]
   #print(dates)
   #print(len(dates))

   #yrs = (1980, 2020) # not needed???
   #vc = compute_climatology(v, yrs) # not needed???
   file2 = pyg.open(path+'tp_climatology_1980to2021.nc')  
   vclim = pyg.dailymean(file2.TP_CLIM)

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
   tp_anom = vcomp.rename("tp_anom")
   return tp_anom 
#tp_comp = compute_composite(ds.tp(time=("1 Jan 1958", "31 Dec 1980")))

#fn2 = path + 'tp_composite_1958to1980_rel_1980to2021clim.nc'
#pyg.save(fn2, tp_comp)  """

# need to rerun 
# tp_composite_2001to2021_rel_2001to2021clim.nc
# file contents got corrupted 
""" def compute_composite(v):  
   file = open(path2+'ssw_dates.txt','r')
   content = file.readlines()
   dates = content[33:48] # change as needed
   #print(dates)
   #print(len(dates))

   #yrs = (1980, 2020) # not needed???
   #vc = compute_climatology(v, yrs) # not needed???
   file2 = pyg.open(path+'tp_climatology_2001to2021.nc') # climatology file - change as needed
   vclim = pyg.dailymean(file2.TP_CLIM)

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
   tp_anom = vcomp.rename("tp_anom")
   tp_anom = tp_anom.transpose("time","event","latitude","longitude").axes # include!
   return tp_anom 
tp_comp = compute_composite(ds.tp(time=("1 Jan 2001", "31 Dec 2021"))) # change as needed

fn2 = path + 'tp_composite_2001to2021_rel_2001to2021clim.nc' # change filename as needed
pyg.save(fn2, tp_comp) """

# 20-year SST anomalies relative to whole period climatology, DJFM season 
def compute_DJFM_climatology(tp, yrs):
    if yrs is None:
	    yrs = (1980, 2021) # climatology base period # change as needed
	    fn = path + '%s_climatology.nc' % tp # make a path, fn = filename 
    else:
        def sel(var):
            return var(time=("1 Dec %d" % yrs[0],"1 Apr %d" % yrs[1]),l_month=(12,1,2,3))
        fn = path + '%s_DJFM_climatology_%dto%d.nc' % (tp, yrs[0], yrs[1])

    prectot_r = remove_leap(ds.vardict[tp])  
    prectot_r = sel(prectot_r)
    prectot_r = pyg.dailymean(prectot_r).rename(tp)

    #print(prectot_r) 
    prectot_c = pyg.climatology(prectot_r).rename('TP_CLIM').load()
    prectot_cs = prectot_c.fft_smooth('time', 4) # retains first 4 harmonic functions 
    #print(prectot_cs)
    #return None
    pyg.save(fn, prectot_cs)

tp_1 = compute_DJFM_climatology('tp', (1940,1960))
tp_2 = compute_DJFM_climatology('tp', (1960,1980))
tp_3 = compute_DJFM_climatology('tp', (1980,2000))
tp_4 = compute_DJFM_climatology('tp', (2000,2020))
tp_5 = compute_DJFM_climatology('tp', (1940,2020))

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