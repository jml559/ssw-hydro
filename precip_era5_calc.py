import pygeode as pyg
import cartopy.crs as ccrs
import pylab as pyl; pyl.ion();

patt = "$Y"
path = "/local1/storage1/jml559/era5/"

year_list = [path+'era5_*%d*.nc' % a for a in range(194,203)]
#print(year_list)

ds = pyg.open_multi(year_list, pattern=patt)
#print(ds)

mean_tp = ds.tp(year=(1940,2022)).mean("time") # .load()
#print(mean_tp)
#pyg.save("precip_era5.nc", mean_tp)
#pyg.showvar(mean_tp)

# comment out below if running above script
# comment out above if running script for plot

# climatology plot - does not seem to work
""" ds_clim = pyg.open("precip_era5.nc")
#print(ds_clim)
#cm = pyg.clfdict(cdelt=500, min=0, ndiv=5, nl=1, nf=5, style='seq', cmap=pyl.cm.BrBG, extend='max')
pyl.ioff()
ax = pyg.showvar(ds_clim.tp)
#ax = pyg.showvar(1000*365*ds_clim.tp, **cm) # (m/day) * (1000 mm/m) * (365 d/1 y)
ax.axes[0].setp(title = "Annual precip climatology (1940-2022) (mm), ERA5")
ax.axes[1].setp(title = "mm")
pyl.ion()
ax.render() """

