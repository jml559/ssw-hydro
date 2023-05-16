import pygeode as pyg
import cartopy.crs as ccrs
import cartopy.util as cu 
import pylab as pyl; pyl.ion();

patt = "$Y$m$d"
path = "/local1/storage1/jml559/merra2/"

year_list = [path+'%d0s/M*%d[0-9]*.nc' % (a,a) for a in range(198,203)]
ds = pyg.open_multi(year_list, pattern=patt)
cm = pyg.clfdict(style='seq', min=0, cdelt=0.00005, ndiv=5, nl=1, nf=5, extend="max")

""" #ds_1980s = ds.PRECTOT(year=(1980,1989))
ds_1980s = pyg.open("prectot_merra2_1980s.nc")
#mean_1980s = ds_1980s.mean("time").load()
#mean_1980s_c = cu.add_cyclic_point(mean_1980s)
#pyg.showvar(mean_1980s_c)
pyg.showvar(ds_1980s.PRECTOT, style='seq', min=0, cdelt=0.00005, ndiv=5, nl=1, nf=5)  """

# AttributeError: 'ndim' not found in <Var 'PRECTOT'> with cyclic point

# Also, if I want to make changes to a plot, do I have to 
# reload the data and wait 10 minutes every time, or is there a
# faster way to do this? 
# There is a faster way! use the pyg.open() command and write a new 
# pyg.showvar line (see 1990s example below)


""" #ds_1990s = ds.PRECTOT(year=(1990,1999))
ds_1990s = pyg.open("prectot_merra2_1990s.nc")
#mean_1990s = ds_1990s.mean("time").load()
#pyg.showvar(mean_1990s, style='seq', min=0, cdelt=0.0001, ndiv=5, nl=3, nf=6)
pyg.showvar(ds_1990s.PRECTOT, style='seq', min=0, cdelt=0.00005, ndiv=5, nl=1, nf=5) """

#ds_2000s = ds.PRECTOT(year=(2000,2009))
#ds_2000s = pyg.open("prectot_merra2_2000s.nc")
#mean_2000s = ds_2000s.mean("time").load()
#pyg.showvar(mean_2000s)
#pyg.showvar(ds_2000s.PRECTOT, **cm)

""" #ds_2010s = ds.PRECTOT(year=(2010,2019))
ds_2010s = pyg.open("prectot_merra2_2010s.nc")
#mean_2010s = ds_2010s.mean("time").load()
#pyg.showvar(mean_2010s)
pyg.showvar(ds_2010s.PRECTOT, style='seq', min=0, cdelt=0.00005, ndiv=5, nl=1, nf=5)
#pyl.savefig("2010s_mean_precip.pdf") """

""" #ds_2020s = ds.PRECTOT(year=(2020,2021)) # originally had (2010,2019)
ds_2020s = pyg.open("prectot_merra2_2020s.nc")
#mean_2020s = ds_2020s.mean("time").load()
#pyg.showvar(mean_2020s)
pyg.showvar(ds_2020s.PRECTOT, style='seq', min=0, cdelt=0.00005, ndiv=5, nl=1, nf=5)  """

#cdelt = 0.00005
#ds_all = ds.PRECTOT(year=(1980,2021))

ds_all = pyg.open("/local1/storage1/jml559/merra2/PRECTOT_climatology_1980to2021.nc")
cm = pyg.clfdict(cdelt=500, min=0, ndiv=5, nl=1, nf=5, style='seq', cmap=pyl.cm.BrBG, extend='max')
pyl.ioff()
ax = pyg.showvar(3600*24*365*ds_all.PRECTOT_CLIM.mean("time"), **cm)
ax.axes[0].setp(title = "Annual precip climatology (1980-2021) (mm), PRECTOT")
ax.axes[1].setp(title = "mm")
pyl.ion()
ax.render()

