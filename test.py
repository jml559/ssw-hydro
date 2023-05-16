import pygeode as pyg
import numpy as np
import pylab as pyl; pyl.ion();
from matplotlib import pyplot as plt
from pygeode.tutorial import t1
from pygeode.tutorial import t2

### 1. GETTING STARTED
# gives a plot of temperature of dataset t1
plt.ion()
#pyg.showvar(t1.Temp) 

#print(t2) 

Tc = pyg.climatology(t2.Temp) # computes the climatology of temp in t2 dataset
Tcz = Tc.mean('lon') # computes the zonal mean
#print(Tcz)

Tcp = Tc - Tcz # compute anomaly from zonal mean 
Tcp = Tcp.rename("T'") # Rename variable to T'
#print(Tcp) # prints info about Tcp 

#pyg.showvar(Tcp(pres=1000, time='15 Jun 00')) 
#pyg.showvar(Tcp(pres=850, time='10 Oct 00')) 

'''
pyg.save('scripts/file.nc', t1) # saves dataset as a netCDF file
ds = pyg.open('scripts/file.nc')
print(ds)
'''

### 2. BASIC OPERATIONS
t_av = t1.Temp.mean('lon') # Fast: no computations carried out
#print(t_av[:])

# Example of selecting subsets
#print(t1.Temp(lat=(30, 50), lon=(100, 180)))
#print(t1.Temp(lat=(0,90),lon=(180,360)))

# We can take a look at the latitude (and longitude) grid points for reference
# These will return the array for each 
#print(t1.Temp.lat[:])
#print(t1.Temp.lon[:])

#print(t1.Temp(lat=12))
#print(t1.Temp(lon=180))

#print(t1.Temp(i_lat=1).lat) # index-based
#be careful; index 0 starts from the LAST value in the array

#print(t1.Temp(i_lat=-5).lat) 
#apparently north is negative here 

#print(t1.Temp(l_lat=(-25, 0, 60, 92)).lat.values)


#print(t2.time.startdate)
#print(t2.time.values)
#print(t2.Temp(time=8).time)
#print(t2.Temp(time=('12 Dec 2013', '18 Jan 2014')).time) # select a range of dates
#print(t2.Temp(year = 2013).time) # select all elements in year 2013
#print(t2.Temp(l_month = (1, 2, 12)).time) # select all elements in Jan, Feb, or Dec

# Plots and graphs; arithmetic
#pyg.showvar(pyg.log(t1.Temp))     # Plot the natural logarithm of Temp
#pyg.showvar(pyg.sind(t1.lat))     # Compute the sine of latitude (sind = input in degrees)

#pyg.showvar(t1.Temp > 280., clevs=np.arange(-0.1, 1.11, 0.1))

# Broadcasting
#print((t2.U + t2.Temp).axes)   # No broadcasting required
#print((t2.lat + t2.lon).axes)  # Broadcast to (lat, lon)
#print((t2.lon + t2.lat).axes)  # Broadcast to (lon, lat)
#print((t2.lon + t2.Temp).axes)  # Broadcast to (time, pres, lat, lon)

# Broadcasting restricts longitude axis to subset
#print((t2.Temp(lon=(0, 180)) - t2.Temp).lon) 

# Subsetted longitude axes are not compatible:
#try: print((t2.Temp(lon=(0, 180)) + t2.Temp(lon=(120, 240))).lon)
#except ValueError as e: print(e)

#print(t2.Temp.mean('pres', pyg.Lon))
#print(t2.Temp.mean('time', pyg.Lon))
#print(t2.Temp.mean('pres', 'lat', 'lon'))
#print(t2.Temp.mean('lon'))
#print(t2.Temp.mean(pyg.Lon)) # gives same output/average as previous line
#print(t2.Temp.mean(3)) # gives same output/average as previous line

# Computing the (weighted by default) average over the subset of a domain
#print(t2.Temp(m_lat=(70, 90))) # selects all latitudes over 70 to 90 N and performs an average 

#print(t2.Temp.lat.weights) # prints the weights; pygeode weights latitude with cosine 
# since area near poles is smaller 

# Computing the unweighted average 
#print(t2.Temp.mean('lat', weights=False))

# Specifying custom weights
#print(t2.Temp.mean('lat', weights=pyg.sind(t2.Temp.lat)))
# full list of axis reductions: https://pygeode.github.io/var.html#reduce-list

# Reshaping variables
#print(t2.Temp.axes)
#print(t2.Temp.transpose('lon', 'lat', 'pres', 'time').axes) # reorders the axes

# The logPAxis method returns a log-pressure axis with a given scale height
#print(t2.Temp.replace_axes(pres=t2.pres.logPAxis(H=7000)).axes)

# Squeeze: removal of degenerate axes
#print(t2.Temp(time = 4, lon = 20))
#print(t2.Temp(time = 4, lon = 20).squeeze()) # squeeze all degenerate axes
#print(t2.Temp(time = 4, lon = 20).squeeze('time')) # squeeze only the time axis
#above returns 18 E since lon = 20 is closest to this. 
#print(t2.Temp.lon[:])

# Select a single value then squeeze the time axis
#print(t2.Temp.squeeze(time = 4))

# Select a single value and sqeeze the time axis using a selection prefix
#print(t2.Temp(s_time = 4, lon = (20, 40)))



### 3. VARIABLE AND FILE INPUT/OUTPUT

## 3.1. Basics
## Weird - below code runs properly in VS Code with
## 'scripts/file.nc', and in Terminal with just 'file.nc'. 
## An error results in Terminal and VS Code, respectively
#ds = pyg.open('scripts/file.nc')
#print(ds)
#print(ds.lat.weights)

## 3.2. Overriding Metadata
#pyg.save('file_nometa.nc', t1, cfmeta=False)
#ds2 = pyg.open('file_nometa.nc')
#print(ds2) 

#pyg.showvar(ds2.Temp) 

dt = dict(lat = pyg.Lat, lon = pyg.regularlon(60)) # how to make the axes proper again
#print(pyg.open('file_nometa.nc', dimtypes=dt))
 
#kwargs = dict(units='days', startdate = dict(year=2001, month=1, day=1)) # what does this do?
#dt2 = dict(lon = (pyg.StandardTime, kwargs))
#print(pyg.open('file_nometa.nc', dimtypes=dt2))

# renaming variables
#nm = dict(lon = 'Longitude', Temp='Temperature')
#print(pyg.open('file_nometa.nc', namemap=nm, dimtypes=dt))

# 3.3 Reading from Multiple Datasets
# produces 10 datasets, each with a year of data 
#for y in range(2011, 2021):
#    pyg.save('temp_zm_y%d.nc' % y, t2.Temp(year=y).mean('lon'))

#ds = pyg.openall('temp_zm_*.nc', namemap=dict(Temp='T'))
#print(ds.T)

# manipulating individual files
""" def opener(f):
    ds = pyg.open(f)
    if '2016' in f: # Replace the data in this file with a dummy value
        return pyg.Dataset([ds.Temp * 0 + 200.])
    else:
        return ds
ds = pyg.openall('temp_zm_*.nc', opener=opener)
pyg.showvar(ds.Temp(lat=15, pres=500)) """

""" patt = 'temp_zm_y(?P<year>[0-9]{4}).nc'
print(pyg.open_multi('temp_zm_*.nc', pattern=patt)) """

""" patt = 'temp_zm_y$Y.nc'
print(pyg.open_multi('temp_zm_*.nc', pattern=patt)) """

""" def f2d(fn):
    date = dict(month=1, day=1)
    date['year'] = int(fn[-7:-3]) # Extract the year from the filename and convert to an integer
    return date

print(pyg.open_multi('temp_zm_*.nc', file2date = f2d)) """

""" # 3.4. Saving to files
pyg.save('file_v4.nc', t1, version=4) """


### 4. PLOTTING

#pyg.showvar(t1.Temp(lat=45)) # line plot
#pyg.showvar(t1.Temp) # contour plot

#pyg.showvar(t2.Temp.mean('time', 'lat', 'lon'), 'k--', lw=3.) # vertical plot
#pyg.showvar(t2.Temp.mean('time', 'lat', 'lon'), transpose = True) # transposed plot

#pyg.showvar(t2.Temp(pres=200).mean('time'))
#pyg.showvar(t2.U(pres=200).mean('time'))

#pyg.showvar(t2.U(pres=200).mean('time'), style='seq', ndiv=3, nl=3, nf=6)
#pyg.showvar(t2.U(pres=200).mean('time'), style='div', cdelt=5., ndiv=2, nf=5, nozero=True)

#tm = t2.Temp.mean('time', 'lon')
#pyg.showlines([tm(lat=l) for l in [-60, -30, 0, 30, 60]])

tm = t2.Temp.mean('time')
pyg.showgrid([tm(pres=p) for p in [1000, 500, 200, 100]], ncol=2, style='seq', min=180, ndiv=5)
#pyg.showgrid([tm(pres=p) for p in [1000, 500, 200, 100]], ncol=2, style='seq', min=180, cdelt=30, ndiv=5)
# somehow there's an error for cdelt

