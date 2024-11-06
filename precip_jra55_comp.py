import pygeode as pyg
import cartopy.crs as ccrs
import pylab as pyl; pyl.ion();

path = "/local1/storage1/jml559/jra55/tprat/"
path2 = "/local1/storage1/jml559/scripts/"

year_list = [path+"fcst_*319.%d*_%d*.nc" % (a,a) for a in range(1958,2024)] # (1958,2024)
ds = pyg.openall(year_list)
#print(ds) # Data should be in 6 h data

def remove_leap(v): 
    return pyg.timeutils.removeleapyears(v, omitdoy_leap=[182])
	# omits the 182nd day of the year during leap years

""" def compute_climatology(tp, yrs): 
    if yrs is None:
	    yrs = (1980, 2021) # climatology base period 
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

prectot_cs = compute_climatology('TPRAT_GDS4_SFC_ave3h', (2000,2019)) # change as needed
prectot_cs_2 = compute_climatology('TPRAT_GDS4_SFC_ave3h', (1980,1999))
prectot_cs_3 = compute_climatology('TPRAT_GDS4_SFC_ave3h', (1960,1979)) """

# rename "TPRAT_climatology_1980to2021.nc" (or other start/end year) """

def compute_composite(v,i1,i2,climo_fn):  
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
   vrd = vrd(l_month=(1,2,3,12)) # DJFM only
   
   va = vrd - vclim # va = anomaly
   """print("va:")
   print(va)
   print("vrd:")
   print(vrd)
   print("vclim:")
   print(vclim)"""

   vcomp = va.composite(l_time = dates, evlen = 140, evoff = 40)
   vcomp = vcomp(forecast_time1 = 3).squeeze()
   tp_anom = vcomp.rename("tp_anom")
   return tp_anom 

#tp_comp = compute_composite(ds.TPRAT_GDS4_SFC_ave3h) # don't need to subset v
"""tp_comp_1 = compute_composite(ds.TPRAT_GDS4_SFC_ave3h,39,53,path+"TPRAT_DJFM_climatology_2000to2020.nc")
fn1 = path + 'TPRAT_DJFM_composite_2000to2020.nc'
print(fn1)
pyg.save(fn1, tp_comp_1) 

tp_comp_2 = compute_composite(ds.TPRAT_GDS4_SFC_ave3h,28,39,path+"TPRAT_DJFM_climatology_1980to2000.nc")
fn2 = path + 'TPRAT_DJFM_composite_1980to2000.nc'
print(fn2)
pyg.save(fn2, tp_comp_2) 

tp_comp_3 = compute_composite(ds.TPRAT_GDS4_SFC_ave3h,15,28,path+"TPRAT_DJFM_climatology_1960to1980.nc")
fn3 = path + 'TPRAT_DJFM_composite_1960to1980.nc'
print(fn3)
pyg.save(fn3, tp_comp_3) """

#print(prectot_comp)
#pyg.showvar(prectot_comp(time=(-40,0), lat=40, lon=-70)) 

# 1958 to 1980 SSWs (relative to 1980-2021 climatology)
""" year_list = [path+"fcst_*319.%d*_%d*.nc" % (a,a) for a in range(1958,1981)]
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
   file2 = pyg.open(path+'TPRAT_climatology_1980to2021.nc')  
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
tp_comp = compute_composite(ds.TPRAT_GDS4_SFC_ave3h) 

fn2 = path + 'TPRAT_composite_1958to1980_rel_1980to2021clim.nc' # edit as needed
pyg.save(fn2, tp_comp) """


""" year_list = [path+"fcst_*319.%d*_%d*.nc" % (a,a) for a in range(2001,2022)]
ds = pyg.openall(year_list)

def compute_composite(v):  
   file = open(path2+'ssw_dates.txt','r')
   content = file.readlines()
   dates = content[33:48] # change
   #print(dates)
   #print(len(dates))

   #yrs = (1980, 2020) # not needed???
   #vc = compute_climatology(v, yrs) # not needed???
   file2 = pyg.open(path+'TPRAT_climatology_2001to2021.nc') # change
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
tp_comp = compute_composite(ds.TPRAT_GDS4_SFC_ave3h) 

fn2 = path + 'TPRAT_composite_2001to2021_rel_2001to2021clim.nc' # edit as needed
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
    prectot_r = sel(prectot_r) # comment out?
    prectot_r = pyg.dailymean(prectot_r).rename(tp)

    #print(prectot_r) 
    prectot_c = pyg.climatology(prectot_r).rename('TP_CLIM').load()
    prectot_cs = prectot_c.fft_smooth('time', 4) # retains first 4 harmonic functions 
    #print(prectot_cs)
    #return None
    pyg.save(fn, prectot_cs)  

#tp_1 = compute_DJFM_climatology('TPRAT_GDS4_SFC_ave3h', (1940,1960)) # don't use
""" tp_2 = compute_DJFM_climatology('TPRAT_GDS4_SFC_ave3h', (1960,1980))
tp_3 = compute_DJFM_climatology('TPRAT_GDS4_SFC_ave3h', (1980,2000))
tp_4 = compute_DJFM_climatology('TPRAT_GDS4_SFC_ave3h', (2000,2020))
tp_5 = compute_DJFM_climatology('TPRAT_GDS4_SFC_ave3h', (1940,2020)) 
tp_6 = compute_DJFM_climatology('TPRAT', (1960,2020)) """
#tp_7 = compute_DJFM_climatology('TPRAT_GDS4_SFC_ave3h', (1980,2020))
tp_8 = compute_DJFM_climatology('TPRAT_GDS4_SFC_ave3h', (1970,1990))
tp_9 = compute_DJFM_climatology('TPRAT_GDS4_SFC_ave3h', (1990,2010))

# rename files











