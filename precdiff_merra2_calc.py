import pygeode as pyg
import cartopy.crs as ccrs
import pylab as pyl; pyl.ion();

""" patt = "$Y$m$d"
path1 = "/local1/storage1/jml559/merra2/"
path2 = "/local1/storage1/jml559/merra2/prectotcorr/"

year_list_1 = [path1+'%d0s/M*%d[0-9]*.nc' % (a,a) for a in range(198,203)]
year_list_2 = [path2+'MERRA2_*%d[0-9]*.nc' % a for a in range(198,203)]

ds1 = pyg.open_multi(year_list_1, pattern=patt)
ds2 = pyg.open_multi(year_list_2, pattern=patt)

mean1 = ds1.PRECTOT(year=(1980,2021)).mean("time")
mean2 = ds2.PRECTOTCORR(year=(1980,2021)).mean("time")
diff = mean1 - mean2
pyg.save("precdiff_merra2.nc", diff) """

# difference between PRECTOT - PRECTOTCORR 
ds = pyg.open("precdiff_merra2.nc")
cm = pyg.clfdict(cdelt=500, min=-1500, ndiv=3, nl=1, nf=5, style='div', cmap=pyl.cm.BrBG, extend='both')
pyl.ioff()
ax = pyg.showvar(3600*24*365*ds._PRECTOT_PRECTOTCORR_, **cm)
ax.axes[0].setp(title = "PRECTOT minus PRECTOTCORR climatology (1980-2021) (mm)")
ax.axes[1].setp(title = "mm")
pyl.ion()
ax.render()