import pygeode as pyg
import cartopy.crs as ccrs
import pylab as pyl; pyl.ion();
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

patt = "$Y$m$d"
path = "/local1/storage1/jml559/merra2/" 
path_s = "/local1/storage1/jml559/ssw-hydro/"

year_list = [path+'prectotcorr/MERRA2_*%d[0-9]*.nc' % a for a in range(198,203)] # check
ds = pyg.open_multi(year_list, pattern=patt)

# omits the 182nd day of the year during leap years
def remove_leap(v): 
    return pyg.timeutils.removeleapyears(v, omitdoy_leap=[182])

# computes full year climatology 
def compute_climatology(prectotcorr, yrs): 
    if yrs is None:
        yrs = (1981, 2020)
        fn = path + '%s_climatology.nc' % prectotcorr # make a path, fn = filename 
    else:
        fn = path + '%s_climatology_%dto%d.nc' % (prectotcorr, yrs[0], yrs[1])
    time = ('1 Jan %d' % yrs[0], '31 Dec %d' % yrs[1])

    prectot_r = remove_leap(ds.vardict[prectotcorr])
    prectot_r = pyg.dailymean(prectot_r).rename(prectotcorr)
    #print(prectot_r) 

    prectot_r = prectot_r(time = time)
    prectot_c = pyg.climatology(prectot_r).rename('PRECTOTCORR_CLIM') #.load()
    prectot_cs = prectot_c.fft_smooth('time', 4) # retains first 4 harmonic functions 
    pyg.save(fn, prectot_cs)

""" prectot_cs = compute_climatology('PRECTOTCORR', (2000,2019)) # change as needed 
prectot_cs_2 = compute_climatology('PRECTOTCORR', (1980,1999)) """

# computes a climatology from 1 Oct <startyear> to 31 May <endyear> for ONDJFMAM only 
def compute_OctToMay_climatology(prectotcorr, yrs):
    if yrs is None:
	    yrs = (1980, 2021) # climatology base period # change as needed
	    fn = path + '%s_climatology.nc' % prectotcorr # make a path, fn = filename 
    else:
        def sel(var):
            return var(time=("1 Oct %d" % yrs[0],"31 May %d" % yrs[1]),l_month=(10,11,12,1,2,3,4,5))
        fn = path + '%s_OctToMay_climatology_%dto%d.nc' % (prectotcorr, yrs[0], yrs[1])

    prectot_r = remove_leap(ds.vardict[prectotcorr])  
    prectot_r = sel(prectot_r)
    prectot_r = pyg.dailymean(prectot_r).rename(prectotcorr)
    #print(prectot_r) 

    prectot_c = pyg.climatology(prectot_r).rename('PRECTOTCORR_CLIM').load()
    prectot_cs = prectot_c.fft_smooth('time', 4) # retains first 4 harmonic functions 
    #print(prectot_cs)
    #print(fn)
    #return None
    pyg.save(fn, prectot_cs)

"""for start_year in range(1980, 2001, 10):
    compute_OctToMay_climatology('PRECTOTCORR', (start_year, start_year + 20))
    print(f"{start_year} to {start_year + 20} Oct-May climo is done") """






# computes composite based on a fixed climatology
def compute_composite(v,i1,i2,climo_fn): 
    # get list of date strings from ssw_dates.txt 
    file = open(path_s+'ssw_dates.txt','r')
    content = file.readlines()
    dates = content[i1:i2] 
    #print(dates)
    #print(len(dates))

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
def compute_composite_v2(v,i1,i2,bef_fn,aft_fn):
    file = open(path_s+'ssw_dates.txt','r')
    content = file.readlines()
    dates = content[i1:i2]

    climo_files = [path+"PRECTOTCORR_OctToMay_climatology_1980to2000.nc",
     path+"PRECTOTCORR_OctToMay_climatology_1990to2010.nc",
     path+"PRECTOTCORR_OctToMay_climatology_2000to2020.nc"]  
    
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
        
        w0[i] = np.where(year < 1990, 1, np.where((1990 <= year) & (year <= 2000), 
            1 - 0.1 * (year - 1990), 0))
        w1[i] = np.where((1990 <= year) & (year <= 2000), 0.1 * (year - 1990),
            np.where((2000 <= year) & (year <= 2010), 1 - 0.1 * (year - 2000), 0))
        w2[i] = np.where(year >= 2010, 1, np.where((2000 <= year) & (year <= 2010), 
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
        vc = (w0[i]*pyg.dailymean(file_90.PRECTOTCORR_CLIM) 
            + w1[i]*pyg.dailymean(file_00.PRECTOTCORR_CLIM) 
            + w2[i]*pyg.dailymean(file_10.PRECTOTCORR_CLIM)) # already in time, lat, lon
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

    """return before
    return after""" # uncomment these when running the first time 

    pyg.save(bef_fn, before)
    print("Done saving before")
    pyg.save(aft_fn, after) # comment out when running the first time
    print("Done saving after")

"""compute_composite_v2(ds.PRECTOTCORR,28,39,
    path+"before_SSWs_OctToMay_1980to2000.nc",
    path+"after_SSWs_OctToMay_1980to2000.nc") 

compute_composite_v2(ds.PRECTOTCORR,39,53,
    path+"before_SSWs_OctToMay_2000to2020.nc",
    path+"after_SSWs_OctToMay_2000to2020.nc") """

# includes event dimension (run separately)
compute_composite_v2(ds.PRECTOTCORR,28,53,
    path+"before_SSWs_OctToMay_eventlatlon_1980to2020.nc",
    path+"after_SSWs_OctToMay_eventlatlon_1980to2020.nc") 





 