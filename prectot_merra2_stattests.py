import pygeode as pyg
import pylab as pyl; pyl.ion();
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
import random 

# compute composite before and after SSWs
""" file = open('ssw_dates_exc2018.txt','r')
content = file.readlines()
dates = content[0:26] """
n_events = 27 # make arbitrary; not a constant # len(dates) ?
n_lat = 361
n_lon = 576
# Note!!! - change this manually until I figure this out

ds_comp = pyg.open("/local1/storage1/jml559/merra2/prectot_composite.nc")
#ds_comp = pyg.open("/local1/storage1/jml559/merra2/prectot_composite_exc2018.nc") 

# initialize arrays, set lat and lon
prec_anom_before = np.zeros((n_events, n_lat, n_lon))
prec_anom_after = np.zeros((n_events, n_lat, n_lon))

#print(ds_comp.event)
#def anom_before(lat1,lat2,lon1,lon2):
prec_anom_before = ds_comp.prectot_anom(time=(-40,0)).nanmean('time')[:]
prec_anom_after = ds_comp.prectot_anom(time=(0,61)).nanmean('time')[:]
#print(prec_anom_before.shape)

N_resamples = 10000 
mean_anom_r_bef = np.zeros((N_resamples, n_lat, n_lon)) # array of (N_resamples) mean values 
mean_anom_r_aft = np.zeros((N_resamples, n_lat, n_lon))

resample_bef = np.zeros((n_events, n_lat, n_lon)) # resample array to store the 27 values
resample_aft = np.zeros((n_events, n_lat, n_lon))

# print(prec_anom_before) # some duplicate values
# print(resample_bef)

# before SSWs 
for h in range(N_resamples):
    #for i in range(n_events):
    r = np.random.randint(0,n_events,n_events)
    resample_bef = prec_anom_before[r,:,:]
    mean_anom_r_bef[h,:,:] = np.mean(resample_bef,0) # np.mean(0) - averaged over n_events
#print(mean_anom_r_bef[:,0,90])

# after SSWs # edit/modify
for h in range(N_resamples):
    r2 = np.random.randint(0,n_events,n_events)
    resample_aft = prec_anom_after[r2,:,:]
    mean_anom_r_aft[h,:,:] = np.mean(resample_aft,0)
    
# generate histogram
""" n_bins = 50
plt.hist(mean_anom_r_bef,n_bins,color='purple')
fig1 = pyl.figure()
plt.show()

plt.hist(mean_anom_r_aft,n_bins,color='blue')
fig2 = pyl.figure()
plt.show() """

# calculate a p-value for every grid point
p_bef_dry = np.zeros((n_lat,n_lon)) # for dry anoms
p_aft_dry = np.zeros((n_lat,n_lon))
p_bef_wet = np.zeros((n_lat,n_lon)) # for wet anoms
p_aft_wet = np.zeros((n_lat,n_lon))
#sig_bef = np.zeros((n_lat,n_lon)) # to keep track of type of sig anom for each point
#sig_aft = np.zeros((n_lat,n_lon))

# new p-value approach: p is the proportion of samples greater than 0 
## p = number of resamples greater than 0 at each point / number of resamples
## p > 0.975 (sig pos), p < 0.025 (sig neg) # two tailed p = 0.05 sig level 
#p_bef[:,:] = len(mean_anom_r_bef[:,:,:] > 0) / N_resamples
#p_bef[:,:] = (mean_anom_r_bef[:,:,:]>0).sum() / N_resamples
#p_bef[:,:] = len(mean_anom_r_bef[mean_anom_r_bef[:,:,:] > 0]) / N_resamples
for i in range(n_lat):
    for j in range(n_lon):
        p_bef_dry[i,j] = (mean_anom_r_bef[:,i,j]>0).sum() / N_resamples
        p_aft_dry[i,j] = (mean_anom_r_aft[:,i,j]>0).sum() / N_resamples
        p_bef_wet[i,j] = (mean_anom_r_bef[:,i,j]<0).sum() / N_resamples
        p_aft_wet[i,j] = (mean_anom_r_aft[:,i,j]<0).sum() / N_resamples
        """ if p_bef[i,j] > 0.975:
            sig_bef[i,j] = 1
        if p_bef[i,j] < 0.025:
            sig_bef[i,j] = -1
        if p_aft[i,j] > 0.975:
            sig_aft[i,j] = 1
        if p_aft[i,j] < 0.025:
            sig_aft[i,j] = -1 """

# significance maps
#pyg.showvar(pyg.Var((ds_comp.lat,ds_comp.lon),values=sig_bef,name='sig_bef'),nl=0)
#pyg.showvar(pyg.Var((ds_comp.lat,ds_comp.lon),values=sig_aft,name='sig_aft'),nl=0)

# try to get stippling/hatching (as most papers show significance)
# remove contours for masked map - or make the contours white for non-significant 
# pyg.vcontour - alpha = 0.5, color='w', levels=[-0.5,0.5] 

# significance maps before SSWs
""" prectot_comp_before_ssw = ds_comp.prectot_anom(time=(-40,0)).nanmean('time','event').load() #nanmean('time','event')
sigmask_bef_dry = (1 - 0.5*pyg.Var((ds_comp.lat,ds_comp.lon),values=p_bef_dry)) * pyg.sign(prectot_comp_before_ssw)
sigmask_bef_wet = (1 - 0.5*pyg.Var((ds_comp.lat,ds_comp.lon),values=p_bef_wet)) * pyg.sign(prectot_comp_before_ssw)
cm = pyg.clfdict(cdelt=12.5, nf=4, nl=0, ndiv=4, style='div', cmap=pyl.cm.BrBG, extend='both') 

pyl.ioff()
ax1 = pyg.showvar(3600*24*40*prectot_comp_before_ssw, **cm)

pyg.vsigmask(sigmask_bef_dry, ax1.axes[0], mjsig = 0.975, mjsigp = dict(visible=False), nsigp = dict(alpha=0.3, color='w', hatch=None)) #nsig = not significant
pyg.vsigmask(sigmask_bef_wet, ax1.axes[0], mjsig = 0.975, mjsigp = dict(visible=False), nsigp = dict(alpha=0.3, color='w', hatch=None))
pyg.vsigmask(sigmask_bef_dry, ax1.axes[0], mjsig = 0.975) #nsigp, #mjsigp = dict(alpha = 0, hatch = None)
pyg.vsigmask(sigmask_bef_wet, ax1.axes[0], mjsig = 0.975) #nsigp = dict(alpha = 0.6, color = 'w', hatch = None)

ax1.axes[0].setp(title = "Precip anomaly 40-1 days before SSWs (95% significance stippled)")
ax1.axes[1].setp(title = "mm") 
pyl.ion()
ax1.render() """ 

# significance maps after SSWs
prectot_comp_after_ssw = ds_comp.prectot_anom(time=(0,61)).nanmean('time','event').load()
sigmask_aft_dry = (1 - 0.5*pyg.Var((ds_comp.lat,ds_comp.lon),values=p_aft_dry)) * pyg.sign(prectot_comp_after_ssw)
sigmask_aft_wet = (1 - 0.5*pyg.Var((ds_comp.lat,ds_comp.lon),values=p_aft_wet)) * pyg.sign(prectot_comp_after_ssw)
cm = pyg.clfdict(cdelt=20, nf=4, nl=0, ndiv=4, style='div', cmap=pyl.cm.BrBG, extend='both')

pyl.ioff()
ax2 = pyg.showvar(3600*24*61*prectot_comp_after_ssw, **cm)

pyg.vsigmask(sigmask_aft_dry, ax2.axes[0], mjsig = 0.975, mjsigp = dict(visible=False), nsigp = dict(alpha=0.3, color='w', hatch=None)) 
pyg.vsigmask(sigmask_aft_wet, ax2.axes[0], mjsig = 0.975, mjsigp = dict(visible=False), nsigp = dict(alpha=0.3, color='w', hatch=None))
pyg.vsigmask(sigmask_aft_dry, ax2.axes[0], mjsig = 0.975) 
pyg.vsigmask(sigmask_aft_wet, ax2.axes[0], mjsig = 0.975) 

ax2.axes[0].setp(title = "Precip anomaly 0-60 days after SSWs (95% significance stippled)")
ax2.axes[1].setp(title = "mm") 
pyl.ion()
ax2.render()

# not needed
""" t_bef = (np.mean(mean_anom_r_bef,0))/(np.std(mean_anom_r_bef,0)*np.sqrt(N_resamples))
p_bef = st.t.sf(abs(t_bef), df=N_resamples-1)
sig_bef[(p_bef<0.05) & (t_bef>0)] = 1 # Make sure to use the right p-value!
sig_bef[(p_bef<0.05) & (t_bef<0)] = -1 

t_aft = (np.mean(mean_anom_r_aft,0))/(np.std(mean_anom_r_aft,0)*np.sqrt(N_resamples)) #t_aft all the same
p_aft = st.t.sf(abs(t_aft), df=N_resamples-1) # p_aft all the same
sig_aft[(p_aft>0.975) & (t_aft>0)] = 1 # bug - shows all zeros
sig_aft[(p_aft>0.975) & (t_aft<0)] = -1 """






# compute confidence intervals
""" p5 = int((0.05*N_resamples)-1)
p95 = int((0.95*N_resamples)-1)
p1 = int((0.01*N_resamples)-1)
p99 = int((0.99*N_resamples)-1)

sorted_bef = np.sort(mean_anom_r_bef)
CI95_bef = (sorted_bef[p5],sorted_bef[p95]) # 95% confidence interval 
CI99_bef = (sorted_bef[p1],sorted_bef[p99]) # 99% confidence interval
print("longitude:", (lon1,lon2), "latitude:", (lat1,lat2))
print("CI95_bef:", CI95_bef) 
print("CI99_bef:", CI99_bef)

sorted_aft = np.sort(mean_anom_r_aft)
CI95_aft = (sorted_aft[p5],sorted_aft[p95])
CI99_aft = (sorted_aft[p1],sorted_aft[p99])
print("CI95_aft:", CI95_aft)
print("CI99_aft:", CI99_aft)  """

# find a way to index a tuple, if possible; otherwise change to nparray
# turn into a p-value map, and get stippling 

# pick a fixed longitude, and figure out where duplication is happening









#CI_bef = st.norm.interval(alpha=0.95, loc=np.mean(mean_anom_r_bef), scale=st.sem(mean_anom_r_bef))
#print(CI_bef)



# review code, try to print stuff and run it
# generate histogram, write code to find 95% CI
# next steps


    #mean_anom_r_bef = # sum(prec_anom_r) / len(prec_anom_r)

    #anom_r_bef[i] = prec_anom_before[r]
    #anom_r_aft[i] = prec_anom_after[r]
     
    # now have two samples.
    # "control": n = 27 or 28, mean 0
    # "resampled": n = 1000, mean mean_anom_r_bef (or aft)

    # return confidence interval? result of stats test?
    # assume normal populations or not - if not, do a t-test?



    #for each event (loop)
    # compute before SSW anomaly and after SSW anomaly at the grid box

# compute composites for a few boxes
# stippling to show significance on maps 
# - does pygeode happen to have anything on this?