import pygeode as pyg
import cartopy.crs as ccrs
import pylab as pyl; pyl.ion();
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

patt = "$Y$m$d"
path = "/local1/storage1/jml559/merra2/" # check
path_s = "/local1/storage1/jml559/scripts/"

year_list = [path+'prectotcorr/MERRA2_*%d[0-9]*.nc' % a for a in range(198,203)] # check

ds = pyg.open_multi(year_list, pattern=patt)

def remove_leap(v): 
    return pyg.timeutils.removeleapyears(v, omitdoy_leap=[182])
	# omits the 182nd day of the year during leap years

def compute_climatology(prectotcorr, yrs): 
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

""" prectot_cs = compute_climatology('PRECTOTCORR', (2000,2019)) # change as needed 
prectot_cs_2 = compute_climatology('PRECTOTCORR', (1980,1999)) """

"""def compute_DJF_climatology(prectotcorr, yrs): # DO NOT USE
    if yrs is None:
	    yrs = (1981, 2020) # yrs is a tuple # climatology base period
	    fn = path + '%s_climatology.nc' % prectotcorr # make a path, fn = filename 
    else:
        def sel(var):
            return var(time=("1 Dec %d" % yrs[0],"31 Mar %d" % yrs[1]),l_month=(12,1,2,3)) 
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
    pyg.save(fn, prectot_cs) """

#prectot_cs = compute_DJF_climatology("PRECTOTCORR", (2000,2020))
#prectot_cs = compute_DJF_climatology("PRECTOTCORR", (1980,2000)) 

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
    file2 = pyg.open(climo_fn)  
    vclim = pyg.dailymean(file2.PRECTOTCORR_CLIM)

    vr = remove_leap(v)
    vrd = pyg.dailymean(vr).rename(vr.name)
    vrd = vrd(l_month=(1,2,3,12)) # DJFM only
   
    va = vrd - vclim # va = anomaly
    print(va)
    """print("va:")
    print(va)
    print("vrd:")
    print(vrd)
    print("vclim:")
    print(vclim)"""

    """vcomp = va.composite(l_time = dates, evlen = 140, evoff = 40)
    prectotcorr_anom = vcomp.rename("prectotcorr_anom")
    prectotcorr_anom = prectotcorr_anom.transpose("time","event","lat","lon")
    return prectotcorr_anom"""

# linear interpolation/weighting of decadal moving average
def compute_composite_v2(v,i1,i2):
    file = open(path_s+'ssw_dates.txt','r')
    content = file.readlines()
    dates = content[i1:i2]

    climo_files = [path+"PRECTOTCORR_DJFM_climatology_1980to2000.nc",
     path+"PRECTOTCORR_DJFM_climatology_1990to2010.nc",
     path+"PRECTOTCORR_DJFM_climatology_2000to2020.nc"]
    
    file_90 = pyg.open(climo_files[0])
    file_00 = pyg.open(climo_files[1])
    file_10 = pyg.open(climo_files[2])

    # extract year from each date string, and compute weights 
    years = [] 
    w0 = np.zeros(len(dates))
    w1 = np.zeros(len(dates))
    w2 = np.zeros(len(dates))

    for i, date in enumerate(dates):
        year = int(date.split()[-1])
        years.append(year)
        
        """if year < 1990:
            w0[i] = 1
            w1[i] = 0
            w2[i] = 0"""
        
        w0[i] = np.where(year < 1990, 1, np.where((1990 <= year) & (year <= 2000), 
            1 - 0.1 * (year - 1990), 0))
        w1[i] = np.where((1990 <= year) & (year <= 2000), 0.1 * (year - 1990),
            np.where((2000 <= year) & (year <= 2010), 1 - 0.1 * (year - 2000), 0))
        w2[i] = np.where((2000 <= year) & (year <= 2010), 0.1 * (year - 2000),
            np.where((2010 <= year) & (year <= 2020), 1 - 0.1 * (year - 2010), 0))

    vclim = []
    vr = []
    va = []
    vcomp_bef = []
    vcomp_aft = []

    vr_ = remove_leap(v)
    vrd_ = pyg.dailymean(vr_).rename(vr_.name)

    for i in range(len(dates)):
        ax_ev = pyg.NamedAxis([i], 'event')
        vc = (w0[i]*pyg.dailymean(file_90.PRECTOTCORR_CLIM) 
            + w1[i]*pyg.dailymean(file_00.PRECTOTCORR_CLIM) 
            + w2[i]*pyg.dailymean(file_10.PRECTOTCORR_CLIM)) # already in time, lat, lon
        vclim.append(vc)
        
        va_ = vrd_ - vc # va = anomaly
        va_ = va_.extend(0, ax_ev)
        if i == 0: 
            print(w0[i])
            print(w1[i])
            print(w2[i])
            print(dates[i])
            print(va_.time)
            print(vc.time)
            print(va_(l_month=(12,1,2,3)).time + vc.time)
            """print(va_)
            print(vrd_)
            print(vclim[i])"""
        va.append(va_)

        cdate = dates[i].strip() # central date 
        cdate_dt = datetime.strptime(cdate, "%d %b %Y")
        sdate_dt = cdate_dt - timedelta(days=40)
        edate_dt = cdate_dt + timedelta(days=61)
        sdate = sdate_dt.strftime("%d %b %Y")
        edate = edate_dt.strftime("%d %b %Y")
        """if i == 0:
            print(sdate)
            print(edate)"""

        vcomp_bef_ = va_(time=(sdate,cdate)).mean("time").rename("prectotcorr_comp") # [40,-1]
        vcomp_aft_ = va_(time=(cdate,edate)).mean("time").rename("prectotcorr_comp") # [0,60]
        vcomp_bef.append(vcomp_bef_)
        vcomp_aft.append(vcomp_aft_)

    print("\n vcomp:")
    print(vcomp_bef[0])
    print(vcomp_aft[0]) 

    # convert time to yearless (but time has 121 values?)
    # va did have 2 time axes (somehow)

    # mean across events



    # mean_pcorr = ds.PRECTOTCORR(year=(1980,2021)).mean("time").load()
    
    # for each event 
    # pick -40 to 0 
    # pick days 0 to 60 - and compute a time average 
    # 

    """vcomp = va.composite(l_time = dates, evlen = 140, evoff = 40)
    prectotcorr_anom = vcomp.rename("prectotcorr_anom")
    prectotcorr_anom = prectotcorr_anom.transpose("time","event","lat","lon")
    return prectotcorr_anom"""

    # create weighting variables 
    # vclim = w50*vclim50 + ... 
    # vclim -> year, day, lat, lon 
    # TimeUtils function: timeutils.joinaxes() to collapse time axis
    # for ERA-5, e.g., the year will be a linear sequence of integers
    # c -> time, lat, lon

"""prectotcorr_comp_1 = compute_composite(ds.PRECTOTCORR,39,53,path+"PRECTOTCORR_DJFM_climatology_2000to2020.nc") # Dec 2000 - Mar 2020
fn1 = path + "PRECTOTCORR_DJFM_composite_2000to2020_rel_2000to2020clim.nc" ### """
#print(fn1)
#pyg.save(fn1, prectotcorr_comp_1)  

#prectotcorr = compute_composite(ds.PRECTOTCORR,39,53,path+"PRECTOTCORR_DJFM_climatology_2000to2020.nc")
#prectotcorr = compute_composite_v2(ds.PRECTOTCORR,37,53) # (28,53)

"""prectotcorr_comp_2 = compute_composite(ds.PRECTOTCORR,28,39,path+"PRECTOTCORR_DJFM_climatology_1980to2000.nc") # Dec 1980 - Mar 2000
fn2 = path + "PRECTOTCORR_DJFM_composite_1980to2000_rel_1980to2000clim.nc" ###
print(fn2)
pyg.save(fn2, prectotcorr_comp_2) """

def compute_OctToMay_climatology(prectotcorr, yrs):
    if yrs is None:
	    yrs = (1980, 2021) # climatology base period # change as needed
	    fn = path + '%s_climatology.nc' % prectotcorr # make a path, fn = filename 
    else:
        def sel(var):
            return var(time=("1 Dec %d" % yrs[0],"1 Apr %d" % yrs[1]),l_month=(10,11,12,1,2,3,4,5))
        fn = path + '%s_OctToMay_climatology_%dto%d.nc' % (prectotcorr, yrs[0], yrs[1])

    prectot_r = remove_leap(ds.vardict[prectotcorr])  
    prectot_r = sel(prectot_r)
    prectot_r = pyg.dailymean(prectot_r).rename(prectotcorr)

    #print(prectot_r) 
    prectot_c = pyg.climatology(prectot_r).rename('PRECTOTCORR_CLIM').load()
    prectot_cs = prectot_c.fft_smooth('time', 4) # retains first 4 harmonic functions 
    print(prectot_cs)
    print(fn)
    #return None
    pyg.save(fn, prectot_cs)


"""tp_1 = compute_DJFM_climatology('PRECTOTCORR', (1940,1960))
tp_2 = compute_DJFM_climatology('PRECTOTCORR', (1960,1980))
tp_3 = compute_DJFM_climatology('PRECTOTCORR', (1980,2000))
tp_4 = compute_DJFM_climatology('PRECTOTCORR', (2000,2020))
tp_5 = compute_DJFM_climatology('PRECTOTCORR', (1940,2020)) 
tp_6 = compute_DJFM_climatology('PRECTOTCORR', (1990,2010))"""
"""tp_1 = compute_OctToMay_climatology('PRECTOTCORR', (1980,2000))
tp_2 = compute_OctToMay_climatology('PRECTOTCORR', (1990,2010))
tp_3 = compute_OctToMay_climatology('PRECTOTCORR', (2000,2020))"""

"""for start_year in range(1950, 1991, 20):
    compute_DJFM_climatology('PRECTOTCORR', (start_year, start_year + 20))
    print(f"{start_year} to {start_year + 20} is done")"""

# only compute MERRA from 1980-2020 onwards

### FILES
# /local1/storage1/jml559/era5/tp/remapscon2_Lon360Lat180_tp_climatology_1980to2021.nc
# /local1/storage1/jml559/jra55/tprat/remapscon2_Lon360Lat180_TPRAT_climatology_1980to2021.nc
# not available for MERRA-2

# /local1/storage1/jml559/merra2/PRECTOTCORR_DJFM_climatology_1980to2020.nc
# JRA-55 
# ERA-5