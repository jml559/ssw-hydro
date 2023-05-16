import pygeode as pyg
import pylab as pyl; pyl.ion();
import numpy as np
import matplotlib.pyplot as plt

# composites, except removing 2018

patt = "$Y$m$d"
path = "/local1/storage1/jml559/merra2/"
year_list = [path+'%d0s/M*%d[0-9]*.nc' % (a,a) for a in range(198,203)]
ds = pyg.open_multi(year_list, pattern=patt)

def remove_leap(v): 
    return pyg.timeutils.removeleapyears(v, omitdoy_leap=[182])

# is this even needed?

def compute_composite(v):
   file = open('ssw_dates_exc2018.txt','r')
   content = file.readlines()
   dates = content[0:26]

   file2 = pyg.open(path+'PRECTOT_climatology_1980to2021.nc')  
   vclim = pyg.dailymean(file2.PRECTOT_CLIM)

   vr = remove_leap(v)
   vrd = pyg.dailymean(vr).rename(vr.name)
   
   va = vrd - vclim # va = anomaly
   """ print("va:")
   print(va)
   print("vrd:")
   print(vrd)
   print("vclim:")
   print(vclim)  """

   vcomp = va.composite(l_time = dates, evlen = 140, evoff = 40)
   prectot_anom = vcomp.rename("prectot_anom")
   return prectot_anom 
prectot_comp = compute_composite(ds.PRECTOT) 

fn2 = path + 'prectot_composite_exc2018.nc'
pyg.save(fn2, prectot_comp)