import pygeode as pyg
import cartopy.crs as ccrs
import pylab as pyl; pyl.ion();
import numpy as np
import matplotlib.pyplot as plt

patt = "$Y$m$d"
path = "/local1/storage1/jml559/merra2/" # check
path_s = "/local1/storage1/jml559/scripts/"

year_list = [path+'prectotcorr/MERRA2_*%d[0-9]*.nc' % a for a in range(198,203)] # check

ds = pyg.open_multi(year_list, pattern=patt)

def remove_leap(v): 
    return pyg.timeutils.removeleapyears(v, omitdoy_leap=[182])
	# omits the 182nd day of the year during leap years

""" def compute_climatology(prectotcorr, yrs): 
    if yrs is None:
	    yrs = (1981, 2020) # yrs is a tuple # climatology base period
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

prectot_cs = compute_climatology('PRECTOTCORR', (2000,2019)) # change as needed 
prectot_cs_2 = compute_climatology('PRECTOTCORR', (1980,1999)) """

""" def compute_DJF_climatology(prectotcorr, yrs):
    if yrs is None:
	    yrs = (1981, 2020) # yrs is a tuple # climatology base period
	    fn = path + '%s_climatology.nc' % prectotcorr # make a ppth, fn = filename 
    else:
        def sel(var):
            return var(time=("1 Dec %d" % yrs[0],"1 Mar %d" % yrs[1]),l_month=(12,1,2)) 
        fn = path + '%s_DJF_climatology_%dto%d.nc' % (prectotcorr, yrs[0], yrs[1])
        #time = 
    #time = (("1 Dec %d" % yrs[0],"1 Mar %d" % yrs[1]),l_month=(12,1,2))
    #time = ds.PRECTOTCORR(time=("1 Dec %d" % yrs[0],"1 Mar %d" % yrs[1]),l_month=(12,1,2)).time # adjust 28 or 29 Feb as needed

    prectot_r = remove_leap(ds.vardict[prectotcorr]) 
    prectot_r = sel(prectot_r)
    prectot_r = pyg.dailymean(prectot_r).rename(prectotcorr)

    #print(prectot_r)
    #prectot_r = prectot_r(time = time) 
    prectot_c = pyg.climatology(prectot_r).rename('PRECTOTCORR_CLIM') #.load()
    prectot_cs = prectot_c.fft_smooth('time', 4) # retains first 4 harmonic functions 
    #print(prectot_cs)
    #return None
    pyg.save(fn, prectot_cs) 

#prectot_cs = compute_DJF_climatology("PRECTOTCORR", (2000,2020))
#prectot_cs = compute_DJF_climatology("PRECTOTCORR", (1980,2000)) """

# read ssw_dates.txt
# get a list of dates, with each date/entry as a string 
# lines 2 to 48

def compute_composite(v,i1,i2,climo_fn): 
   file = open(path_s+'ssw_dates.txt','r')
   content = file.readlines()
   dates = content[i1:i2] # change as needed
   #print(dates)
   #print(len(dates))

   #yrs = (1980, 2020) # not needed???
   #vc = compute_climatology(v, yrs) # not needed???
   file2 = pyg.open(climo_fn)  # check file
   # 'PRECTOTCORR_DJF_climatology_2000to2020.nc'
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
   prectotcorr_anom = prectotcorr_anom.transpose("time","event","lat","lon")
   return prectotcorr_anom 

prectotcorr_comp_1 = compute_composite(ds.PRECTOTCORR,38,53,path+"PRECTOTCORR_climatology_2000to2019.nc")
fn1 = path + "PRECTOTCORR_composite_2000to2019_rel_2000to2019clim.nc"
print(fn1)
pyg.save(fn1, prectotcorr_comp_1) 

prectotcorr_comp_2 = compute_composite(ds.PRECTOTCORR,27,38,path+"PRECTOTCORR_climatology_1980to1999.nc")
fn2 = path + "PRECTOTCORR_composite_1980to1999_rel_1980to1999clim.nc"
print(fn2)
pyg.save(fn2, prectotcorr_comp_2)





