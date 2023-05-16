# composite anomaly plots

import pygeode as pyg
import cartopy.crs as ccrs
import cartopy.util as cu 
import pylab as pyl; pyl.ion();
import numpy as np
import matplotlib.pyplot as plt

#cm = pyg.clfdict(style='seq', min=0, cdelt=0.00005, ndiv=5, nl=1, nf=5, extend="max")

ds_comp = pyg.open("/local1/storage1/jml559/merra2/prectot_composite.nc")
#ds_comp = pyg.open("/local1/storage1/jml559/merra2/prectot_composite_exc2018.nc") 

lon1 = -30
lon2 = -0.1
lat1 = 30
lat2 = 50

prectot_comp_before_ssw = ds_comp.prectot_anom(time=(-40,0),lon=(lon1,lon2),lat=(lat1,lat2)).nanmean('time','event') #nanmean('time','event')
pyg.showvar(prectot_comp_before_ssw, ndiv=4, nf=8)

prectot_comp_after_ssw = ds_comp.prectot_anom(time=(0,61),lon=(lon1,lon2),lat=(lat1,lat2)).nanmean('time','event')
pyg.showvar(prectot_comp_after_ssw, ndiv=4, nf=8)

# good idea to use nanmean when computing composites
# some events at the start of the period may have a day -40 outside of the dataset 

# make plots of:
# -40 to 0 
# 0 to 60


# next steps: stat sig tests
# 1) t-test: is the sample at a given grid point statistically different than zero?
# ^assumes Gaussian
# 2) Monte Carlo/bootstrap test. 
# original sample of 28 
# re-sampling: take the samples and re-sample them with replacement, many times
# if, say, 99% resamples show an anomaly > 0, it's unlikely to be random 
# it's still possible some of the signal is due to other modes of clim var
# such as ENSO. SSWs more likely in strong El Nino/La Nina years - but nonlinear

# what to show for Thursday's presentation???
# brief overview of research - accurate?
# results/plots - recent figures, as well as precip climo from Dec last year?