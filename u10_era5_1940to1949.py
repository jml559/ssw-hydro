# compute a time series of U10 winds at 60 deg N from ERA-5 1940 to 1949
# then find SSW dates
import pygeode as pyg
import numpy as np
from pygeode import composite, eof, climat, plot as pl
from numpy import *
import matplotlib
from pylab import *
from datetime import *
import os.path

# get zonal mean zonal wind at 60 N
path = "/local1/storage1/jml559/era5/"
ds = pyg.open(path + "1940s_u10.nc")
u10 = ds.u(lat=60).mean("longitude")  
#pyg.showvar(u10)

def findSSWs(n_uz, perpjan = False, pres=10, nsep=20, verbose=True):
# {{{
   ''' Returns central dates of stratospheric sudden warmings according to the definition
         of Charlton & Polvani J Clim 2007 20:449. '''

   if n_uz.hasaxis('pres'):
      uzl = n_uz(pres=pres, lat=60)
      z = uzl.pres.values[0]
   else:
      uzl = n_uz(lat=60)
      z = pres

   # Compute anomalies of daily averaged data
   #duz = composite.time_ave(uzl, 'd')
   #duz = climat.dailymean(uzl)
   us = uzl.squeeze()[:]

   def printDates(ssws):
      for i, s in enumerate(ssws):
         print(uzl.time.formatvalue(s, '$D $b $Y\t')),
         if i % 8 == 5: print
      print

   # Find all transitions from westerlies to easterlies
   issws = where((us[1:] < 0) & (us[:-1] > 0))[0] + 1
   ssws = uzl.time.values[issws]
   if verbose:
      print('Wind reversals (%d): ' % len(ssws))
      printDates(ssws)
   
   # Select only those in extended winter (NDJFM)
   if not perpjan:
      ssws_d = uzl.time.val_as_date(ssws)
      ssws_mw = [s for s, m in zip(ssws, ssws_d['month']) if m in [11, 12, 1, 2, 3]]
      #ssws_mw = ssws[doy(ssws) < 151]
   else:
      ssws_mw = ssws

   if verbose:
      print('Mid-winter reversals (%d): ' % len(ssws_mw))
      printDates(ssws_mw)

   if len(ssws_mw) == 0:
      print('No ssws found.')
      return array([])

   # Eliminate those not preceeded by nsep days of westerlies
   ssws_nr = []
   for s in ssws_mw:
      iv = where(uzl.time.values == s)[0][0] - 1
      dt = uzl.time.val_as_date(uzl.time.values[iv + 1])
      lw = uzl.time.val_as_date(uzl.time.values[iv])      # date of last easterlies
      discard = False
      while uzl.time.date_diff(dt, lw, 'days') < nsep and iv >= 0:
         if us[iv] <= 0.: 
            discard = True
            break
         iv -= 1
         dt = uzl.time.val_as_date(uzl.time.values[iv])

      if not discard: ssws_nr.append(s)

   # Eliminate those which occur within 60 days of a previous reversal
   #ssws_nr = ssws_mw[0:1]
   #for s in ssws_mw[1:]:
      #dt = uzl.time.val_as_date(s)
      #lr = uzl.time.val_as_date(ssws_nr[-1])
      #if uzl.time.date_diff(lr, dt, units='days') > nsep: 
         #ssws_nr.append(s)

   if verbose:
      print('Separated mid-winter reversals (%d): ' % len(ssws_nr))
      printDates(ssws_nr)

   if len(ssws_nr) == 0:
      print('No ssws found.')
      return array([])

   # Select those for which westerlies occur for at least 10 consecutive days prior to the
   # subsequent April 30th
   if not perpjan:
      ssws_nf = []
      for s in ssws_nr:
         iv = where(uzl.time.values == s)[0][0]
         dt = uzl.time.val_as_date(uzl.time.values[iv])
         lw = dt     # date of last easterlies
         while dt['month'] in [11, 12, 1, 2, 3, 4]:
            #print iv, dt['month'], us[iv]

            if us[iv] <= 0:
               # If the winds are easterly, update last date of easterlies
               lw = uzl.time.val_as_date(uzl.time.values[iv])

            ds = uzl.time.date_diff(lw, dt, units='days')
            #print ds

            if ds >= 10.:
               # If more than 10 days have passed, this isn't a final warming
               ssws_nf.append(s)
               break

            iv += 1
            if iv >= len(uzl.time): # We've run off the end of the time series; 
               break                # don't include this ssw
            dt = uzl.time.val_as_date(uzl.time.values[iv])
   else:
      ssws_nf = ssws_nr

   if verbose:
      print('Warmings; no final warmings (%d): ' % len(ssws_nf))
      printDates(ssws_nf)

   if len(ssws_nf) == 0:
      print('No ssws found.')
   else:
      print('%d ssws found.' % len(ssws_nf))

   return array(ssws_nf)
# }}} 

SSWs_1940s = findSSWs(u10)
print(SSWs_1940s)

# verify the 1940s dates with later decades to ensure this code is working as expected