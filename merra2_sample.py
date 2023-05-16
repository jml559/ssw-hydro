import pygeode as pyg
import numpy as np
import pylab as pyl; pyl.ion();
from matplotlib import pyplot as plt

import sys
import json
import urllib3
import certifi
import requests
from time import sleep
from http.cookiejar import CookieJar
import urllib.request
from urllib.parse import urlencode

import getpass

# ds = data sample
ds = pyg.open('MERRA2_400.tavg1_2d_flx_Nx.20220929.SUB.nc')
print(ds)

#pyg.showvar(ds.PRECTOT(time='05:30 29 Sep 2022'),cdelt=0.001,style="seq",min=0,nf=5,fig=1)
pyg.showvar(ds.PRECTOT.sum('time'),cdelt=0.005,style="seq",min=0,nf=5,ndiv=5,nl=1,fig=1)