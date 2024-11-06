import pygeode as pyg
import cartopy.crs as ccrs
import pylab as pyl; pyl.ion();

patt = "$Y$m$d"
path = "/local1/storage1/jml559/merra2/"

year_list = [path+'%d0s/M*%d[0-9]*.nc' % (a,a) for a in range(198,203)]
#print(year_list)

ds = pyg.open_multi(year_list, pattern=patt)
#print(ds)

""" for i in range(7):
    start_year = 1940 + 10*i 
    end_year = start_year + 20
    decadal_mean[i] = ds.PRECTOT(year=(start_year, )) """


mean_all = ds.PRECTOT(year=(1980,2021)).mean("time") #.load()
pyg.save("prectot_merra2_clima",mean_all)
#print(mean_all)
#cm = pyg.clfdict(cdelt=100, cmap=pyl.cm.BrBG)
#pyg.showvar(3600*24*365*mean_all, **cm) # mean annual precip (mm)






'''
mean_1980s = ds.PRECTOT(year=(1980,1989)).mean("time").load()
print(mean_1980s)
pyg.save("prectot_merra2_1980s.nc",mean_1980s)
'''

'''
mean_1990s = ds.PRECTOT(year=(1990,1999))#.mean("time").load()
print(mean_1990s.time)
#pyg.save("prectot_merra2_1990s.nc",mean_1990s)

mean_2000s = ds.PRECTOT(year=(2000,2009))#.mean("time").load()
#pyg.save("prectot_merra2_2000s.nc",mean_2000s)

mean_2010s = ds.PRECTOT(year=(2010,2019))#.mean("time").load()
#pyg.save("prectot_merra2_2010s.nc",mean_2010s)

mean_2020s = ds.PRECTOT(year=(2020,2021)).mean("time").load()
pyg.save("prectot_merra2_2020s.nc",mean_2020s)
'''

# 1) compute means for each decade and save into a file (see what I did above)
# 2) **make plots (see prectot_merra2_plots.py file) and pygeode-tutorial
# 3) try to change the colorscale on the plots

# check the 2020-2021 files (are there duplicates, missing ones, any issues?)
# No issues found 

