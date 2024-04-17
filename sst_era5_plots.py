import pygeode as pyg
import cartopy.crs as ccrs 
import pylab as pyl; pyl.ion();
import numpy as np
import matplotlib.pyplot as plt
import random 

path = "/local1/storage1/jml559/era5/"

# climatology differences
ds_1 = pyg.open(path + "sst_DJFM_climatology_1980to2000.nc")
ds_2 = pyg.open(path + "sst_DJFM_climatology_1940to2020.nc")
cm = pyg.clfdict(cdelt=0.4, nf=4, nl=0, ndiv=3, style='div', extend='both') 
diff = ds_1.SST_CLIM.mean("time") - ds_2.SST_CLIM.mean("time")
pyl.ioff()

ax = pyg.showvar(diff, **cm) 
ax.axes[0].setp(title = "ERA-5 DJFM SST climo (1980-2000 minus 1940-2020)")
#ax.axes[1].setp(title = "Anomaly ($^\circ$C)")
pyl.ion()
ax.render()
ax.axes[1].ax.set_title("Anomaly \n ($^\degree$C)", y=1.05, fontsize=10) # fontsize=12

path = "/local1/storage1/jml559/ssw-hydro/"
fn = "ERA5_1980to2000_minus_1940to2020_SST_climo_DJFM.pdf"
pyl.savefig(path + fn) 

# parameters - change as needed
""" n_events = 13
n_lat = 181
n_lon = 360
N_resamples = 10000 

ds_comp = pyg.open(path + "sst_composite_1940to1959.nc") # change name as needed
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

fn1 = "sst_ERA5_before_SSWs_1940to1959_rel_1940to1959clim.pdf" # change as needed
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

fn2 = "sst_ERA5_after_SSWs_1940to1959_rel_1940to1959clim.pdf" # change as needed
pyl.savefig(path2 + fn2) """


# Computation of Nino3.4 daily SST time series in composites
""" path = "/local1/storage1/jml559/jra55/" # can change; does not need to be ERA-5

def plot_nino_34_timeseries(fn1, n_events, title, fn2):
    ds = pyg.open(fn1)

    n_days = 140
    nino_34_ts = np.zeros((n_days, n_events))
    nino_34_ts = ds.sst_anom(latitude=(-5,5),longitude=(190,240)).nanmean("latitude").nanmean("longitude")[:]
    nino_34_ts_mean = nino_34_ts.mean(1) # mean across all (n_events) time series 

    time_axis = np.arange(-40, 100)

    #fig = plt.figure()
    #ax = fig.add_axes()
    pyl.ioff()
    fig, ax = plt.subplots(figsize=(7, 6))

    for i in range(n_events):
        ax.plot(time_axis, nino_34_ts[:,i], color="0.8", lw=1) 
    ax.plot(time_axis, nino_34_ts_mean, color="0.5", lw=2) 

    ax.set_xlabel('Days before or after SSW', fontsize=16)
    ax.set_ylabel('Daily Nino3.4 SST anomaly', fontsize=16)
    ax.set_ylim(-3,3)
    ax.set_title(title, fontsize=20, fontweight="bold") # please make the title a time period (e.g., "1940-1959")
    ax.tick_params(axis='both', which='major', labelsize=16)
    pyl.ion()
    pyl.savefig(fn2)

    #plt.show() #ax.render()

    #pyg.save(fn2, ax)
    #pyl.savefig(path + fn2) """

#path2 = "/local1/storage1/jml559/ssw-hydro/"
""" plot_nino_34_timeseries(path+"sst_composite_1940to1959.nc", 13, "1940-1959", path2+"sst_era5_timeseries_1940to1959.pdf")
plot_nino_34_timeseries(path+"sst_composite_1960to1979.nc", 13, "1960-1979", path2+"sst_era5_timeseries_1960to1979.pdf")
plot_nino_34_timeseries(path+"sst_composite_1980to1999.nc", 11, "1980-1999", path2+"sst_era5_timeseries_1980to1999.pdf")
plot_nino_34_timeseries(path+"sst_composite_2000to2019.nc", 15, "2000-2019", path2+"sst_era5_timeseries_2000to2019.pdf") """
#plot_nino_34_timeseries(path+"")


