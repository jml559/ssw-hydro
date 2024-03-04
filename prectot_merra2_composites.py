import pygeode as pyg
import cartopy.crs as ccrs
import pylab as pyl; pyl.ion();
import numpy as np
import matplotlib.pyplot as plt

patt = "$Y$m$d"
path = "/local1/storage1/jml559/merra2/"

year_list = [path+'%d0s/M*%d[0-9]*.nc' % (a,a) for a in range(198,203)]

ds = pyg.open_multi(year_list, pattern=patt)

def remove_leap(v): 
    return pyg.timeutils.removeleapyears(v, omitdoy_leap=[182])
	# omits the 182nd day of the year during leap years

""" def compute_climatology(prectot, yrs): 
    if yrs is None:
	    yrs = (1981, 2020) # yrs is a tuple # climatology base period
	    fn = path + '%s_climatology.nc' % prectot # make a ppth, fn = filename 
    else:
	    fn = path + '%s_climatology_%dto%d.nc' % (prectot, yrs[0], yrs[1])
    time = ('1 Jan %d' % yrs[0], '31 Dec %d' % yrs[1])

    #prectot_r = remove_leap(prectot_r)
    #prectot_r = pyg.dailymean(ds.vardict[prectot]).rename(prectot)
    #print(prectot_r) # no hh:mm:dd

    prectot_r = remove_leap(ds.vardict[prectot])
    prectot_r = pyg.dailymean(prectot_r).rename(prectot)

    #print(prectot_r) 
    prectot_r = prectot_r(time = time)
    prectot_c = pyg.climatology(prectot_r).rename('PRECTOT_CLIM') #.load()
    prectot_cs = prectot_c.fft_smooth('time', 4) # retains first 4 harmonic functions 
    #print(prectot_cs)
    #return None
    pyg.save(fn, prectot_cs)

#prectot_cs = compute_climatology('PRECTOT', (1980,2021)) """

def compute_DJF_climatology(prectot, yrs):
    if yrs is None:
	    yrs = (1981, 2020) # yrs is a tuple # climatology base period
	    fn = path + '%s_climatology.nc' % prectot # make a ppth, fn = filename 
    else:
	    fn = path + '%s_DJF_climatology_%dto%d.nc' % (prectot, yrs[0], yrs[1])
        time = 

        for i in range(1,len(yrs[1] - yrs[0])):
            time_slice = ('1 Dec %d' % yrs[0], '1 Feb %d' % 1+yrs[0]) # loop?







# read ssw_dates.txt
# get a list of dates, with each date/entry as a string 
# lines 2 to 48

def compute_composite(v): # original - do not modify
   file = open('ssw_dates.txt','r')
   content = file.readlines()
   dates = content[21:48]
   print(dates)
   print(len(dates))

   #yrs = (1980, 2020) # not needed???
   #vc = compute_climatology(v, yrs) # not needed???
   file2 = pyg.open(path+'PRECTOT_climatology_1980to2021.nc')  
   vclim = pyg.dailymean(file2.PRECTOT_CLIM)

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
   prectot_anom = vcomp.rename("prectot_anom")
   return prectot_anom 
prectot_comp = compute_composite(ds.PRECTOT) 

fn2 = path + 'prectot_composite.nc'
pyg.save(fn2, prectot_comp)
#print(prectot_comp)
#pyg.showvar(prectot_comp(time=(-40,0), lat=40, lon=-70))

'''
dailycomp = np.zeros(141) 
def avg_comp(start_day, end_day): # returns the average composite for a time interval
    for i in range(start_day, end_day+1):
        dailycomp[i - start_day] = prectot_comp(time=i)
    sumcomp = np.sum(dailycomp)
    #sumcomp = prectot_comp(time=-40) + prectot_comp(time=-39) + ...
    daylength = end_day - start_day # length of time interval
    ac = sumcomp/daylength
    return ac
    #ac = prectot_comp(time=(start_day,end_day))
'''

# make new script for plots
#prectot_comp_before_ssw = prectot_comp(time=(-40,-39)).nanmean('time','event')
#prectot_comp_before_ssw = prectot_comp(time=(-40,-39),event='4 Mar 1981').mean('time')
#pyg.showvar(prectot_comp_before_ssw, ndiv=3, nf=6)


### Composite generation for DJF mean only