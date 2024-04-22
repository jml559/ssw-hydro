import pygeode as pyg
import cartopy.crs as ccrs
import pylab as pyl; pyl.ion();
import numpy as np
import matplotlib.pyplot as plt
import random 

path = "/local1/storage1/jml559/jra55/tprat/"

year_list = [path+"fcst_*319.%d*_%d*.nc" % (a,a) for a in range(1958,2024)] # (1958,2024)
ds = pyg.openall(year_list)

# climatology plot; original data in mm/d
""" ds_clim = pyg.open(path + "TPRAT_climatology_1980to2021.nc")
ds_clim_avg_3h6h = ds_clim.TP_CLIM.mean("forecast_time1").mean("time")
ax = pyg.showvar(365*ds_clim_avg_3h6h) # **cm
ax.axes[0].setp(title = "Annual precip climatology (1980-2021), JRA55 total precip")
ax.axes[1].setp(title = "mm")
pyl.ion()
ax.render() """

""" ds_clim = pyg.open(path + "TPRAT_DJFM_climatology_1960to2020.nc") ###
ds_clim_avg_3h6h = ds_clim.TP_CLIM.mean("forecast_time1").mean("time")
cm = pyg.clfdict(cdelt=2, min=0, ndiv=5, nl=1, nf=5, style='seq', cmap=pyl.cm.viridis, extend='max')
pyl.ioff()
ax = pyg.showvar(ds_clim_avg_3h6h, **cm)
ax.axes[0].setp(title = "DJFM daily precip climatology (1980-2021), JRA-55") ###
# wrong, should be 1960-2020
pyl.ion()
ax.render()
ax.axes[1].ax.set_title("mm/d", y=1.05, fontsize=12)

path = "/local1/storage1/jml559/ssw-hydro/"
fn = "JRA55_1980to2020_precip_climo_DJFM.pdf" ###
pyl.savefig(path + fn) """

# climatology plot; polar projection focusing on NH 
ds_clim = pyg.open(path + "TPRAT_DJFM_climatology_1960to2020.nc") ###
ds_clim_avg_3h6h = ds_clim.TP_CLIM.mean("forecast_time1").mean("time")
cm = pyg.clfdict(cdelt=1.5, min=0, ndiv=5, nl=1, nf=5, style='seq', cmap=pyl.cm.viridis, extend='max')
pyl.ioff()
map = dict(projection = "NorthPolarStereo")
ax = pyg.showvar(ds_clim_avg_3h6h, map=map, **cm)
ax.axes[0].set_extent([0,359,20,90],crs=ccrs.PlateCarree())
ax.axes[0].setp(title = "DJFM daily precip climatology (1960-2020), JRA-55") ###
pyl.ion()
ax.render() 
ax.axes[1].ax.set_title("mm/d", y=1.05, fontsize=12) 

path = "/local1/storage1/jml559/ssw-hydro/"
fn = "ps_JRA55_1960to2020_precip_climo_DJFM.pdf" ###
pyl.savefig(path + fn) 



# climatology differences
""" ds_1 = pyg.open(path + "TPRAT_GDS4_SFC_ave3h_DJFM_climatology_1960to1980.nc")
ds_base = pyg.open(path + "TPRAT_GDS4_SFC_ave3h_DJFM_climatology_1960to1980.nc") # fix
cm = pyg.clfdict(cdelt=500, ndiv=6, nl=0, nf=5, style='seq', cmap=pyl.cm.BrBG, extend='max')
diff = 365*(ds_base.TP_CLIM.mean("forecast_time1").mean("time") - ds_1.TP_CLIM.mean("forecast_time1").mean("time"))
pyl.ioff()

ax = pyg.showvar(diff, **cm) 
ax.axes[0].setp(title = "JRA-55 precip climo (2001-2021 minus 1980-2000)")
ax.axes[1].setp(title = "mm")
pyl.ion()
ax.render() 

path = "/local1/storage1/jml559/ssw-hydro/"
fn = "ERA5_2000to2021_minus_1980to2000_precip_climo.pdf"
pyl.savefig(path + fn) """

# parameters
""" n_events = 15 # adjust as needed
n_lat = 180
n_lon = 360
N_resamples = 10000 

ds_comp = pyg.open(path + "remapscon2_Lon360Lat180_TPRAT_composite_2000to2019_rel_2000to2019clim.nc") # change name as needed
#print(ds_comp)
#tp_anom = ds_comp.tp_anom.mean("forecast_time1") # average across 3 and 6 h
tp_anom = ds_comp.tp_anom

prec_anom_before = np.zeros((n_events, n_lat, n_lon))
prec_anom_after = np.zeros((n_events, n_lat, n_lon))

prec_anom_before = tp_anom(time=(-40,0)).nanmean('time')[:]
prec_anom_after = tp_anom(time=(0,61)).nanmean('time')[:]

mean_anom_r_bef = np.zeros((N_resamples, n_lat, n_lon)) # array of (N_resamples) mean values 
mean_anom_r_aft = np.zeros((N_resamples, n_lat, n_lon))

resample_bef = np.zeros((n_events, n_lat, n_lon)) # resample array to store the 27 values
resample_aft = np.zeros((n_events, n_lat, n_lon))

# before SSWs 
for h in range(N_resamples):
    r = np.random.randint(0,n_events,n_events)
    resample_bef = prec_anom_before[r,:,:]
    mean_anom_r_bef[h,:,:] = np.mean(resample_bef,0) 

# after SSWs 
for h in range(N_resamples):
    r2 = np.random.randint(0,n_events,n_events)
    resample_aft = prec_anom_after[r2,:,:]
    mean_anom_r_aft[h,:,:] = np.mean(resample_aft,0)

# calculate a p-value for every grid point
p_bef_dry = np.zeros((n_lat,n_lon)) # for dry anoms
p_aft_dry = np.zeros((n_lat,n_lon))
p_bef_wet = np.zeros((n_lat,n_lon)) # for wet anoms
p_aft_wet = np.zeros((n_lat,n_lon))

for i in range(n_lat):
    for j in range(n_lon):
        p_bef_dry[i,j] = (mean_anom_r_bef[:,i,j]>0).sum() / N_resamples
        p_aft_dry[i,j] = (mean_anom_r_aft[:,i,j]>0).sum() / N_resamples
        p_bef_wet[i,j] = (mean_anom_r_bef[:,i,j]<0).sum() / N_resamples
        p_aft_wet[i,j] = (mean_anom_r_aft[:,i,j]<0).sum() / N_resamples """

# significance maps before SSWs
""" prectot_comp_before_ssw = tp_anom(time=(-40,0)).nanmean('time','event').load() #nanmean('time','event')
sigmask_bef_dry = (1 - 0.5*pyg.Var((tp_anom.Lat,tp_anom.Lon),values=p_bef_dry)) * pyg.sign(prectot_comp_before_ssw)
sigmask_bef_wet = (1 - 0.5*pyg.Var((tp_anom.Lat,tp_anom.Lon),values=p_bef_wet)) * pyg.sign(prectot_comp_before_ssw)
#cm = pyg.clfdict(cdelt=12.5, nf=4, nl=0, ndiv=4, style='div', cmap=pyl.cm.BrBG, extend='both') 
cm = pyg.clfdict(cdelt=10, nf=4, nl=0, ndiv=3, style='div', cmap=pyl.cm.BrBG, extend='both') 

pyl.ioff()
#ax1 = pyg.showvar(40*prectot_comp_before_ssw, **cm) 
map = dict(projection = "NorthPolarStereo")
ax1 = pyg.showvar(40*prectot_comp_before_ssw, map=map, **cm)
ax1.axes[0].set_extent([0,359,20,90],crs=ccrs.PlateCarree()) # restrict domain to 20N to 90N

pyg.vsigmask(sigmask_bef_dry, ax1.axes[0], mjsig = 0.975, mjsigp = dict(visible=False), nsigp = dict(alpha=0.3, color='w', hatch=None)) #nsig = not significant
pyg.vsigmask(sigmask_bef_wet, ax1.axes[0], mjsig = 0.975, mjsigp = dict(visible=False), nsigp = dict(alpha=0.3, color='w', hatch=None))
pyg.vsigmask(sigmask_bef_dry, ax1.axes[0], mjsig = 0.975) #nsigp, #mjsigp = dict(alpha = 0, hatch = None)
pyg.vsigmask(sigmask_bef_wet, ax1.axes[0], mjsig = 0.975) #nsigp = dict(alpha = 0.6, color = 'w', hatch = None)

ax1.axes[0].setp(title = "Precip anomaly 40-1 days before SSWs \n(95% significance stippled), JRA-55 total precip")
ax1.axes[1].setp(title = "mm") 
pyl.ion()
ax1.render() 

fn1 = "ps_JRA55_before_SSWs_2000to2019_rel_2000to2019clim.pdf" # change as needed
path2 = "/local1/storage1/jml559/ssw-hydro/regridded-plots/"
pyl.savefig(path2 + fn1) """

""" fn2 = "JRA55_before_SSWs_1980to2021_prectot_comp.nc"
pyg.save(40*prectot_comp_before_ssw, fn2) # save composite to file

fn3 = "JRA55_before_SSWs_1980to2021_sigmask_bef_dry.nc"
pyg.save(sigmask_bef_dry, fn3)

fn4 = "JRA55_before_SSWs_1980to2021_sigmask_bef_wet.nc"
pyg.save(sigmask_bef_wet, fn4) """ # repeat for after SSWs (and other datasets)

# after SSWs
""" prectot_comp_after_ssw = tp_anom(time=(0,61)).nanmean('time','event').load()
sigmask_aft_dry = (1 - 0.5*pyg.Var((tp_anom.Lat,tp_anom.Lon),values=p_aft_dry)) * pyg.sign(prectot_comp_after_ssw)
sigmask_aft_wet = (1 - 0.5*pyg.Var((tp_anom.Lat,tp_anom.Lon),values=p_aft_wet)) * pyg.sign(prectot_comp_after_ssw)
#cm = pyg.clfdict(cdelt=20, nf=4, nl=0, ndiv=4, style='div', cmap=pyl.cm.BrBG, extend='both')
cm = pyg.clfdict(cdelt=15, nf=4, nl=0, ndiv=3, style='div', cmap=pyl.cm.BrBG, extend='both') 

pyl.ioff()
map = dict(projection = "NorthPolarStereo")
ax2 = pyg.showvar(61*prectot_comp_after_ssw, map=map, **cm)
ax2.axes[0].set_extent([0,359,20,90],crs=ccrs.PlateCarree())

pyg.vsigmask(sigmask_aft_dry, ax2.axes[0], mjsig = 0.975, mjsigp = dict(visible=False), nsigp = dict(alpha=0.3, color='w', hatch=None)) 
pyg.vsigmask(sigmask_aft_wet, ax2.axes[0], mjsig = 0.975, mjsigp = dict(visible=False), nsigp = dict(alpha=0.3, color='w', hatch=None))
pyg.vsigmask(sigmask_aft_dry, ax2.axes[0], mjsig = 0.975) 
pyg.vsigmask(sigmask_aft_wet, ax2.axes[0], mjsig = 0.975) 

ax2.axes[0].setp(title = "Precip anomaly 0-60 days after SSWs \n(95% significance stippled), JRA-55 total precip")
ax2.axes[1].setp(title = "mm") 
pyl.ion()
ax2.render() 

fn2 = "ps_JRA55_after_SSWs_2000to2019_rel_2000to2019clim.pdf" # change as needed
pyl.savefig(path2 + fn2) """









