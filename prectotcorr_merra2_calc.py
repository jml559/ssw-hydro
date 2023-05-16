import pygeode as pyg
import cartopy.crs as ccrs
import pylab as pyl; pyl.ion();

patt = "$Y$m$d"
path = "/local1/storage1/jml559/merra2/prectotcorr/"

year_list = [path+'MERRA2_*%d[0-9]*.nc' % a for a in range(198,203)]
#print(year_list)

ds = pyg.open_multi(year_list, pattern=patt)
#print(ds)

mean_pcorr = ds.PRECTOTCORR(year=(1980,2021)).mean("time").load()
#pyg.save("prectot_merra2_clima",mean_all)
#print(mean_pcorr) 
pyg.save("prectotcorr_merra2.nc",mean_pcorr)



