import pygeode as pyg
import pylab as pyl; pyl.ion();
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

#patt = "$Y$m$d"
path = "/local1/storage1/jml559/era5/" 
path_s = "/local1/storage1/jml559/scripts/"

year_list = [path+'tp/era5_*%d*.nc' % a for a in range(194,203)] 

ds = pyg.openall(year_list)
#print(ds)

def remove_leap(v): 
    return pyg.timeutils.removeleapyears(v, omitdoy_leap=[182])
	# omits the 182nd day of the year during leap years

""" def compute_climatology(tp, yrs): 
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
#prectot_cs_4 = compute_climatology('tp', (1947,1959))  """

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

def compute_composite(v,i1,i2,climo_fn):  
   file = open(path_s+'ssw_dates.txt','r')
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
   vrd = vrd(l_month=(1,2,3,12)) # DJFM only
   
   va = vrd - vclim # va = anomaly
   """print("va:")
   print(va)
   print("vrd:")
   print(vrd)
   print("vclim:")
   print(vclim)"""

   vcomp = va.composite(l_time = dates, evlen = 140, evoff = 40)
   tp_anom = vcomp.rename("tp_anom")
   tp_anom = tp_anom.transpose("time","event","latitude","longitude")
   return tp_anom 

"""tp_comp_1 = compute_composite(ds.tp,39,53,path+"tp/tp_DJFM_climatology_2000to2020.nc") 
fn1 = path + "tp_DJFM_composite_2000to2020.nc"
print(fn1)
pyg.save(fn1, tp_comp_1) 

tp_comp_2 = compute_composite(ds.tp,28,39,path+"tp/tp_DJFM_climatology_1980to2000.nc") 
fn2 = path + "tp_DJFM_composite_1980to2000.nc"
print(fn2)
pyg.save(fn2, tp_comp_2)

tp_comp_3 = compute_composite(ds.tp,15,28,path+"tp/tp_DJFM_climatology_1960to1980.nc") 
fn3 = path + "tp_DJFM_composite_1960to1980.nc"
print(fn3)
pyg.save(fn3, tp_comp_3) 

tp_comp_4 = compute_composite(ds.tp,2,15,path+"tp/tp_DJFM_climatology_1940to1960.nc") 
fn4 = path + "tp_DJFM_composite_1940to1960.nc"
print(fn4)
pyg.save(fn4, tp_comp_4)"""

#print(prectot_comp)
#pyg.showvar(prectot_comp(time=(-40,0), lat=40, lon=-70)) 

def compute_composite_v2(v,i1,i2,bef_fn,aft_fn):
    file = open(path_s+'ssw_dates.txt','r')
    content = file.readlines()
    dates = content[i1:i2]

    climo_files = [f"{path}tp_OctToMay_climatology_{start}to{start+20}.nc"
     for start in range(1940, 2021, 10)]

    file_50 = pyg.open(climo_files[0])
    file_60 = pyg.open(climo_files[1])
    file_70 = pyg.open(climo_files[2])
    file_80 = pyg.open(climo_files[3])
    file_90 = pyg.open(climo_files[4])
    file_00 = pyg.open(climo_files[5])
    file_10 = pyg.open(climo_files[6])

    # extract year from each date string, and compute weights 
    years = [] 
    w0 = np.zeros(len(dates))
    w1 = np.zeros(len(dates))
    w2 = np.zeros(len(dates))
    w3 = np.zeros(len(dates))
    w4 = np.zeros(len(dates))
    w5 = np.zeros(len(dates))
    w6 = np.zeros(len(dates))

    for i, date in enumerate(dates):
        year = int(date.split()[-1])
        years.append(year)
        
        w0[i] = np.where(year < 1950, 1, np.where((1950 <= year) & (year <= 1960),
            1 - 0.1 * (year - 1950), 0))
        w1[i] = np.where((1950 <= year) & (year <= 1960), 0.1 * (year - 1950),
            np.where((1960 <= year) & (year <= 1970), 1 - 0.1 * (year - 1960), 0))
        w2[i] = np.where((1960 <= year) & (year <= 1970), 0.1 * (year - 1960),
            np.where((1970 <= year) & (year <= 1980), 1 - 0.1 * (year - 1970), 0))
        w3[i] = np.where((1970 <= year) & (year <= 1980), 0.1 * (year - 1970),
            np.where((1980 <= year) & (year <= 1990), 1 - 0.1 * (year - 1980), 0))
        w4[i] = np.where((1980 <= year) & (year <= 1990), 0.1 * (year - 1980),
            np.where((1990 <= year) & (year <= 2000), 1 - 0.1 * (year - 1990), 0))
        w5[i] = np.where((1990 <= year) & (year <= 2000), 0.1 * (year - 1990),
            np.where((2000 <= year) & (year <= 2010), 1 - 0.1 * (year - 2000), 0))
        w6[i] = np.where(year >= 2010, 1, np.where((2000 <= year) & (year <= 2010), 
            0.1 * (year - 2000), 0))

    vclim = []
    va = []
    vcomp_bef = []
    vcomp_aft = []

    vr = remove_leap(v)
    vrd = pyg.dailymean(vr).rename(vr.name)
    vrd = vrd(l_month=(10,11,12,1,2,3,4,5))

    for i in range(len(dates)):
        ax_ev = pyg.NamedAxis([i], 'event')
        vc = (w0[i]*pyg.dailymean(file_50.TP_CLIM) 
            + w1[i]*pyg.dailymean(file_60.TP_CLIM) 
            + w2[i]*pyg.dailymean(file_70.TP_CLIM)
            + w3[i]*pyg.dailymean(file_80.TP_CLIM)
            + w4[i]*pyg.dailymean(file_90.TP_CLIM)
            + w5[i]*pyg.dailymean(file_00.TP_CLIM)
            + w6[i]*pyg.dailymean(file_10.TP_CLIM)) # already in time, lat, lon
        vclim.append(vc)
        
        va_ = vrd - vc # va = anomaly
        va_ = va_.extend(0, ax_ev)
        va.append(va_)

        cdate = dates[i].strip() # central date 
        cdate_dt = datetime.strptime(cdate, "%d %b %Y")
        sdate_dt = cdate_dt - timedelta(days=40)
        edate_dt = cdate_dt + timedelta(days=61)
        sdate = sdate_dt.strftime("%d %b %Y")
        edate = edate_dt.strftime("%d %b %Y")

        vcomp_bef_ = va_(time=(sdate,cdate)).mean("time").rename("prectotcorr_comp") # [40,-1]
        vcomp_aft_ = va_(time=(cdate,edate)).mean("time").rename("prectotcorr_comp") # [0,60]
        vcomp_bef.append(vcomp_bef_)
        vcomp_aft.append(vcomp_aft_)

    # one composite for precursor and one for aftermath 
    """before = pyg.concatenate(vcomp_bef[i] for i in range(len(vcomp_bef))).mean("event")
    after = pyg.concatenate(vcomp_aft[i] for i in range(len(vcomp_aft))).mean("event")"""

    # including event dimension
    before = pyg.concatenate(vcomp_bef[i] for i in range(len(vcomp_bef)))
    after = pyg.concatenate(vcomp_aft[i] for i in range(len(vcomp_aft)))

    """print(before)
    print(after) """ # uncomment these when running the first time 

    pyg.save(bef_fn, before)
    print("Done saving before")
    pyg.save(aft_fn, after) # comment out when running the first time
    print("Done saving after") 

"""compute_composite_v2(ds.tp,2,15,path+"before_SSWs_OctToMay_1940to1960.nc",
                    path+"after_SSWs_OctToMay_1940to1960.nc")
compute_composite_v2(ds.tp,15,28,path+"before_SSWs_OctToMay_1960to1980.nc",
                    path+"after_SSWs_OctToMay_1960to1980.nc")
compute_composite_v2(ds.tp,28,39,path+"before_SSWs_OctToMay_1980to2000.nc",
                    path+"after_SSWs_OctToMay_1980to2000.nc") 
compute_composite_v2(ds.tp,39,53,path+"before_SSWs_OctToMay_2000to2020.nc",
                    path+"after_SSWs_OctToMay_2000to2020.nc")"""
compute_composite_v2(ds.tp,2,53,path+"before_SSWs_OctToMay_eventlatlon_1940to2020.nc",
                    path+"after_SSWs_OctToMay_eventlatlon_1940to2020.nc")





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

def compute_OctToMay_climatology(tp, yrs):
    if yrs is None:
	    yrs = (1980, 2021) # climatology base period # change as needed
	    fn = path + '%s_climatology.nc' % tp # make a path, fn = filename 
    else:
        def sel(var):
            return var(time=("1 Dec %d" % yrs[0],"1 Apr %d" % yrs[1]),l_month=(10,11,12,1,2,3,4,5))
        fn = path + '%s_OctToMay_climatology_%dto%d.nc' % (tp, yrs[0], yrs[1])

    prectot_r = remove_leap(ds.vardict[tp])  
    prectot_r = sel(prectot_r)
    prectot_r = pyg.dailymean(prectot_r).rename(tp)

    #print(prectot_r) 
    prectot_c = pyg.climatology(prectot_r).rename('TP_CLIM').load()
    prectot_cs = prectot_c.fft_smooth('time', 4) # retains first 4 harmonic functions 
    #print(prectot_cs)
    #return None
    pyg.save(fn, prectot_cs)

#compute_OctToMay_climatology('tp', (1980,2020))
#for i in range(7):
    #compute_OctToMay_climatology('tp', (10*i + 1940,10*i + 1960))

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

