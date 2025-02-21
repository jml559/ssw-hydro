import pygeode as pyg
import cartopy.crs as ccrs
#import cartopy.util as cu 
import pylab as pyl; pyl.ion();
import numpy as np
import matplotlib.pyplot as plt
import random 

path = "/local1/storage1/jml559/era5/tp/"

year_list = [path+'era5_*%d*.nc' % a for a in range(198,203)] 
ds = pyg.openall(year_list) 

# climatology plot for tp; original data in m/h
""" ds_clim = pyg.open(path + "tp_DJFM_climatology_1940to2020.nc") ###
cm = pyg.clfdict(cdelt=2, min=0, ndiv=5, nl=1, nf=5, style='seq', cmap=pyl.cm.viridis, extend='max')
pyl.ioff()
ax = pyg.showvar(1000*24*ds_clim.TP_CLIM.mean("time"), **cm)
ax.axes[0].setp(title = "DJFM daily precip climatology (1940-2020), ERA5") ###
#ax.axes[1].setp(title = "mm/d")
pyl.ion()
ax.render() 
ax.axes[1].ax.set_title("mm/d", y=1.05, fontsize=12) 

path = "/local1/storage1/jml559/ssw-hydro/"
fn = "ERA5_1940to2020_precip_climo_DJFM.pdf" ###
pyl.savefig(path + fn) """

# climatology plot; polar projection focusing on NH 
""" ds_clim = pyg.open(path + "tp_DJFM_climatology_1940to2020.nc") ###
cm = pyg.clfdict(cdelt=1.5, min=0, ndiv=5, nl=1, nf=5, style='seq', cmap=pyl.cm.viridis, extend='max')
pyl.ioff()
map = dict(projection = "NorthPolarStereo")
ax = pyg.showvar(1000*24*ds_clim.TP_CLIM.mean("time"), map=map, **cm)
ax.axes[0].set_extent([0,359,20,90],crs=ccrs.PlateCarree())
ax.axes[0].setp(title = "DJFM daily precip climatology (1940-2020), ERA5") ###
pyl.ion()
ax.render() 
ax.axes[1].ax.set_title("mm/d", y=1.05, fontsize=12) 

path = "/local1/storage1/jml559/ssw-hydro/"
fn = "ps_ERA5_1940to2020_precip_climo_DJFM.pdf" ###
pyl.savefig(path + fn) """

""" pyl.ioff()
#ax2 = pyg.showvar(1000*24*61*prectot_comp_after_ssw, **cm)
map = dict(projection = "NorthPolarStereo")
ax2 = pyg.showvar(1000*24*61*prectot_comp_after_ssw, map=map, **cm)
ax2.axes[0].set_extent([0,359,20,90],crs=ccrs.PlateCarree()) # restrict domain to 20N to 90N """


# climatology differences
""" ds_1 = pyg.open(path + "remapcon2_tp_DJFM_climatology_2000to2020.nc") ###
ds_base = pyg.open("mrm_DJFM_1980to2020.nc")
#ds_base = pyg.open(path + "tp_DJFM_climatology_1940to2020.nc") # base period
#n_days = 120
cm = pyg.clfdict(cdelt=0.5, ndiv=6, nl=0, nf=2, style='seq', cmap=pyl.cm.BrBG, extend='both') # both
diff = 1000*24*ds_1.TP_CLIM.mean("time") - ds_base.MRM
pyl.ioff()
map = dict(projection = "NorthPolarStereo")

ax = pyg.showvar(diff, map=map, **cm) 
ax.axes[0].set_extent([0,359,20,90],crs=ccrs.PlateCarree())
ax.axes[0].setp(title = "ERA-5 DJFM precip climo (2000-2020 minus 1980-2020 MRM)") ###
#ax.axes[1].setp(title = "mm/d")
pyl.ion()
ax.render() 
ax.axes[1].ax.set_title("mm/d", y=1.05, fontsize=12) 

path = "/local1/storage1/jml559/ssw-hydro/"
fn = "ps_ERA5_2000to2020_minus_1980to2020_precip_MRM_DJFM.pdf" ###
pyl.savefig(path + fn) """

# parameters - change as needed
n_events = 25 ###
n_lat = 180
n_lon = 360 # (180,360) if regridded
N_resamples = 10000 

ds_comp = pyg.open("/local1/storage1/jml559/era5/remapcon2_tp_OctToMay_composite_1980to2020_rel_1980to2020.nc") ### change name as needed
#print(ds_comp)
"""ds_bef = pyg.open("/local1/storage1/jml559/era5/remapcon2_before_SSWs_OctToMay_eventlatlon_1940to2020.nc") 
ds_aft = pyg.open("/local1/storage1/jml559/era5/remapcon2_after_SSWs_OctToMay_eventlatlon_1940to2020.nc") """

prec_anom_before = np.zeros((n_events, n_lat, n_lon))
prec_anom_after = np.zeros((n_events, n_lat, n_lon))

prec_anom_before = ds_comp.tp_anom(time=(-40,0)).nanmean('time')[:]
prec_anom_after = ds_comp.tp_anom(time=(0,61)).nanmean('time')[:] 
"""prec_anom_before = ds_bef.prectotcorr_comp[:]
prec_anom_after = ds_aft.prectotcorr_comp[:]"""

mean_anom_r_bef = np.zeros((N_resamples, n_lat, n_lon)) # array of (N_resamples) mean values 
mean_anom_r_aft = np.zeros((N_resamples, n_lat, n_lon))

resample_bef = np.zeros((n_events, n_lat, n_lon)) # resample array to store the n_events values
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
        p_aft_wet[i,j] = (mean_anom_r_aft[:,i,j]<0).sum() / N_resamples 

# significance maps before SSWs
prectot_comp_before_ssw = ds_comp.tp_anom(time=(-40,0)).nanmean('time','event').load() #nanmean('time','event')
#prectot_comp_before_ssw = ds_bef.prectotcorr_comp.nanmean("event").load()
sigmask_bef_dry = (1 - 0.5*pyg.Var((ds_comp.latitude,ds_comp.longitude),values=p_bef_dry)) * pyg.sign(prectot_comp_before_ssw)
sigmask_bef_wet = (1 - 0.5*pyg.Var((ds_comp.latitude,ds_comp.longitude),values=p_bef_wet)) * pyg.sign(prectot_comp_before_ssw)
#cm = pyg.clfdict(cdelt=12.5, nf=4, nl=0, ndiv=4, style='div', cmap=pyl.cm.BrBG, extend='both') 
#cm = pyg.clfdict(cdelt=10, nf=4, nl=0, ndiv=3, style='div', cmap=pyl.cm.BrBG, extend='both') 
cm = pyg.clfdict(cdelt=0.2, nf=2, nl=0, ndiv=6, style='seq', cmap=pyl.cm.BrBG, extend='both') 

pyl.ioff()
#ax1 = pyg.showvar(1000*24*40*prectot_comp_before_ssw, **cm) # check
map = dict(projection = "NorthPolarStereo")
ax1 = pyg.showvar(1000*24*prectot_comp_before_ssw, map=map, **cm) # map=map
ax1.axes[0].set_extent([0,359,20,90],crs=ccrs.PlateCarree()) # restrict domain to 20N to 90N

pyg.vsigmask(sigmask_bef_dry, ax1.axes[0], mjsig = 0.975, mjsigp = dict(visible=False), nsigp = dict(alpha=0.3, color='w', hatch=None)) #nsig = not significant
pyg.vsigmask(sigmask_bef_wet, ax1.axes[0], mjsig = 0.975, mjsigp = dict(visible=False), nsigp = dict(alpha=0.3, color='w', hatch=None))
pyg.vsigmask(sigmask_bef_dry, ax1.axes[0], mjsig = 0.975) #nsigp, #mjsigp = dict(alpha = 0, hatch = None)
pyg.vsigmask(sigmask_bef_wet, ax1.axes[0], mjsig = 0.975) #nsigp = dict(alpha = 0.6, color = 'w', hatch = None)

ax1.axes[0].setp(title = "Precip anomaly 40-1 days before SSWs \n(95% significance stippled), ERA5 total precip")
pyl.ion()
ax1.render() 
ax1.axes[1].ax.set_title("mm/d", y=1.05, fontsize=12) 

#fn1 = "r2_ERA5_before_SSWs_1947to1959_rel_1947to1959clim.pdf" # change as needed
#pyl.savefig(fn1) 

fn1 = "ps_ERA5_before_SSWs_OctToMay_1980to2020_rel_1980to2020.pdf" ### change as needed 
path2 = "/local1/storage1/jml559/ssw-hydro/regridded-plots/"
#path2 = "/local1/storage1/jml559/ssw-hydro/"
pyl.savefig(path2 + fn1) 

# after SSWs
prectot_comp_after_ssw = ds_comp.tp_anom(time=(0,61)).nanmean('time','event').load()
#prectot_comp_after_ssw = ds_aft.prectotcorr_comp.nanmean("event").load() 
sigmask_aft_dry = (1 - 0.5*pyg.Var((ds_comp.latitude,ds_comp.longitude),values=p_aft_dry)) * pyg.sign(prectot_comp_after_ssw)
sigmask_aft_wet = (1 - 0.5*pyg.Var((ds_comp.latitude,ds_comp.longitude),values=p_aft_wet)) * pyg.sign(prectot_comp_after_ssw)
#cm = pyg.clfdict(cdelt=20, nf=4, nl=0, ndiv=4, style='div', cmap=pyl.cm.BrBG, extend='both')
#cm = pyg.clfdict(cdelt=15, nf=4, nl=0, ndiv=3, style='div', cmap=pyl.cm.BrBG, extend='both') 

pyl.ioff()
#ax2 = pyg.showvar(1000*24*61*prectot_comp_after_ssw, **cm)
map = dict(projection = "NorthPolarStereo")
ax2 = pyg.showvar(1000*24*prectot_comp_after_ssw, map=map, **cm) # map=map
ax2.axes[0].set_extent([0,359,20,90],crs=ccrs.PlateCarree()) # restrict domain to 20N to 90N

pyg.vsigmask(sigmask_aft_dry, ax2.axes[0], mjsig = 0.975, mjsigp = dict(visible=False), nsigp = dict(alpha=0.3, color='w', hatch=None)) 
pyg.vsigmask(sigmask_aft_wet, ax2.axes[0], mjsig = 0.975, mjsigp = dict(visible=False), nsigp = dict(alpha=0.3, color='w', hatch=None))
pyg.vsigmask(sigmask_aft_dry, ax2.axes[0], mjsig = 0.975) 
pyg.vsigmask(sigmask_aft_wet, ax2.axes[0], mjsig = 0.975) 

ax2.axes[0].setp(title = "Precip anomaly 0-60 days after SSWs \n(95% significance stippled), ERA5 total precip") 
pyl.ion()
ax2.render()
ax2.axes[1].ax.set_title("mm/d", y=1.05, fontsize=12) 

fn2 = "ps_ERA5_after_SSWs_OctToMay_1980to2020_rel_1980to2020.pdf" ### change as needed
pyl.savefig(path2 + fn2) 

