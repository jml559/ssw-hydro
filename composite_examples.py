# Some examples of how to compute composites

def remove_leap(v): 
    return pyg.timeutils.removeleapyears(v, omitdoy_leap=[182])

def compute_climatology(v, yrs): # replace v with variable name (e.g., precip)
	if yrs is None:
		yrs = (1979, 2014) # yrs is a tuple
		fn = ppth + '%s_climatology.nc' % v # make a ppth 
	else:
		fn = ppth + '%s_climatology_%dto%d.nc' % (v, yrs[0], yrs[1])
	time = ('1 Jan %d' % yrs[0], '31 Dec %d' % yrs[1])

	vr = pyg.dailymean(ds.vardict[v]).rename(v)

	vr = remove_leap(vr)
	vr = vr(time = time)
	vc = pyg.climatology(vr).rename(v)
	vcs = vc.fft_smooth('time', 4) # retains first 4 harmonic functions 
	return vcs

def compute_composite(v, dates):
   yrs = (1980, 2020)
vc = compute_climatology(v, yrs)

   vr = remove_leap(v)
   vrd = pyg.dailymean(vr).rename(vr.name)
   
   va = vrd - vc

   vcomp = va.composite(l_time = dates, evlen = 140, evoff = 40)

   return vcomp