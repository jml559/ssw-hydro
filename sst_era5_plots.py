import pygeode as pyg
import cartopy.crs as ccrs 
import pylab as pyl; pyl.ion();
import numpy as np
import matplotlib.pyplot as plt
import random 

path = "/local1/storage1/jml559/era5/"

# parameters - change as needed
n_events = 15
n_lat = 181
n_lon = 360
N_resamples = 10000 

ds_comp = pyg.open(path + "sst_composite_2000to2019.nc") # change name as needed
print(ds_comp)

sst_anom_before = np.zeros((n_events, n_lat, n_lon))
sst_anom_after = np.zeros((n_events, n_lat, n_lon))

sst_anom_before = ds_comp.sst_anom(time=(-40,0)).nanmean('time')[:]
sst_anom_after = ds_comp.sst_anom(time=(0,61)).nanmean('time')[:]

mean_anom_r_bef = np.zeros((N_resamples, n_lat, n_lon)) # array of (N_resamples) mean values 
mean_anom_r_aft = np.zeros((N_resamples, n_lat, n_lon))

resample_bef = np.zeros((n_events, n_lat, n_lon)) # resample array to store the 27 values
resample_aft = np.zeros((n_events, n_lat, n_lon))

# before SSWs 
for h in range(N_resamples):
    r = np.random.randint(0,n_events,n_events)
    resample_bef = sst_anom_before[r,:,:]
    mean_anom_r_bef[h,:,:] = np.mean(resample_bef,0) 

# after SSWs 
for h in range(N_resamples):
    r2 = np.random.randint(0,n_events,n_events)
    resample_aft = sst_anom_after[r2,:,:]
    mean_anom_r_aft[h,:,:] = np.mean(resample_aft,0)

# calculate a p-value for every grid point
p_bef_cold = np.zeros((n_lat,n_lon)) # for cold anoms
p_aft_cold = np.zeros((n_lat,n_lon))
p_bef_warm = np.zeros((n_lat,n_lon)) # for warm anoms
p_aft_warm = np.zeros((n_lat,n_lon))

for i in range(n_lat):
    for j in range(n_lon):
        p_bef_cold[i,j] = (mean_anom_r_bef[:,i,j]>0).sum() / N_resamples
        p_aft_cold[i,j] = (mean_anom_r_aft[:,i,j]>0).sum() / N_resamples
        p_bef_warm[i,j] = (mean_anom_r_bef[:,i,j]<0).sum() / N_resamples
        p_aft_warm[i,j] = (mean_anom_r_aft[:,i,j]<0).sum() / N_resamples 

# significance maps before SSWs 
sst_comp_before_ssw = ds_comp.sst_anom(time=(-40,0)).nanmean('time','event').load() #nanmean('time','event')
sigmask_bef_cold = (1 - 0.5*pyg.Var((ds_comp.latitude,ds_comp.longitude),values=p_bef_cold)) * pyg.sign(sst_comp_before_ssw)
sigmask_bef_warm = (1 - 0.5*pyg.Var((ds_comp.latitude,ds_comp.longitude),values=p_bef_warm)) * pyg.sign(sst_comp_before_ssw)
cm = pyg.clfdict(cdelt=0.4, nf=4, nl=0, ndiv=3, style='div', extend='both') 

pyl.ioff()
ax1 = pyg.showvar(sst_comp_before_ssw, **cm)

#map = dict(projection = "NorthPolarStereo")
#ax1 = pyg.showvar(1000*24*40*prectot_comp_before_ssw, map=map, **cm)
#ax1.axes[0].set_extent([0,359,20,90],crs=ccrs.PlateCarree()) # restrict domain to 20N to 90N

pyg.vsigmask(sigmask_bef_cold, ax1.axes[0], mjsig = 0.975, mjsigp = dict(visible=False), nsigp = dict(alpha=0.3, color='w', hatch=None)) #nsig = not significant
pyg.vsigmask(sigmask_bef_warm, ax1.axes[0], mjsig = 0.975, mjsigp = dict(visible=False), nsigp = dict(alpha=0.3, color='w', hatch=None))
pyg.vsigmask(sigmask_bef_cold, ax1.axes[0], mjsig = 0.975) #nsigp, #mjsigp = dict(alpha = 0, hatch = None)
pyg.vsigmask(sigmask_bef_warm, ax1.axes[0], mjsig = 0.975) #nsigp = dict(alpha = 0.6, color = 'w', hatch = None)

ax1.axes[0].setp(title = "SST anomaly 40-1 days before SSWs \n(95% significance stippled), ERA5")
ax1.axes[1].setp(title = "$\degree C$") 
pyl.ion()
ax1.render() 

#fn1 = "r2_ERA5_before_SSWs_1947to1959_rel_1947to1959clim.pdf" # change as needed
#pyl.savefig(fn1) 

fn1 = "sst_ERA5_before_SSWs_2000to2019_rel_2000to2019clim.pdf" # change as needed
path2 = "/local1/storage1/jml559/ssw-hydro/regridded-plots/"
pyl.savefig(path2 + fn1) 

# after SSWs
sst_comp_after_ssw = ds_comp.sst_anom(time=(0,61)).nanmean('time','event').load()
sigmask_aft_cold = (1 - 0.5*pyg.Var((ds_comp.latitude,ds_comp.longitude),values=p_aft_cold)) * pyg.sign(sst_comp_after_ssw)
sigmask_aft_warm = (1 - 0.5*pyg.Var((ds_comp.latitude,ds_comp.longitude),values=p_aft_warm)) * pyg.sign(sst_comp_after_ssw)

pyl.ioff()
ax2 = pyg.showvar(sst_comp_after_ssw, **cm)

#ax2 = pyg.showvar(1000*24*61*prectot_comp_after_ssw, **cm)
#map = dict(projection = "NorthPolarStereo")
#ax2 = pyg.showvar(1000*24*61*prectot_comp_after_ssw, map=map, **cm)
#ax2.axes[0].set_extent([0,359,20,90],crs=ccrs.PlateCarree()) # restrict domain to 20N to 90N

pyg.vsigmask(sigmask_aft_cold, ax2.axes[0], mjsig = 0.975, mjsigp = dict(visible=False), nsigp = dict(alpha=0.3, color='w', hatch=None)) 
pyg.vsigmask(sigmask_aft_warm, ax2.axes[0], mjsig = 0.975, mjsigp = dict(visible=False), nsigp = dict(alpha=0.3, color='w', hatch=None))
pyg.vsigmask(sigmask_aft_cold, ax2.axes[0], mjsig = 0.975) 
pyg.vsigmask(sigmask_aft_warm, ax2.axes[0], mjsig = 0.975) 

ax2.axes[0].setp(title = "SST anomaly 0-60 days after SSWs \n(95% significance stippled), ERA5")
ax2.axes[1].setp(title = "$\degree C$") 
pyl.ion()
ax2.render()

fn2 = "sst_ERA5_after_SSWs_2000to2019_rel_2000to2019clim.pdf" # change as needed
pyl.savefig(path2 + fn2)

