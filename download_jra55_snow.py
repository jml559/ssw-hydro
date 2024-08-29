#!/usr/bin/env python
#################################################################
# Python Script to retrieve 11 online Data files of 'd628000',
# total 18.85G. This script uses 'requests' to download data.
#
# Highlight this script by Select All, Copy and Paste it into a file;
# make the file executable and run it on command line.
#
# You need pass in your password as a parameter to execute
# this script; or you can set an environment variable RDAPSWD
# if your Operating System supports it.
#
# Contact rdahelp@ucar.edu (RDA help desk) for further assistance.
#################################################################


import sys, os
import requests

def check_file_status(filepath):
    sys.stdout.write('\r')
    sys.stdout.flush()
    size_mb = int(os.stat(filepath).st_size)/ 1000**2
    sys.stdout.write('Downloaded %.1f MB' % (size_mb,))
    sys.stdout.flush()

dspath = 'https://request.rda.ucar.edu/dsrqst/LEE754697/'
filelist = [
'TarFiles/anl_snow.066_snowd.reg_tl319.1958010118_1958123118-319.1963010118_1963123118.lee754697.nc.tar',
'TarFiles/anl_snow.066_snowd.reg_tl319.2015040118_2015043018-319.2020120118_2020123118.lee754697.nc.tar',
'TarFiles/anl_snow.066_snowd.reg_tl319.1964010118_1964123118-319.1969010118_1969123118.lee754697.nc.tar',
'TarFiles/anl_snow.066_snowd.reg_tl319.1970010118_1970123118-319.1975010118_1975123118.lee754697.nc.tar',
'TarFiles/anl_snow.066_snowd.reg_tl319.1976010118_1976123118-319.1981010118_1981123118.lee754697.nc.tar',
'TarFiles/anl_snow.066_snowd.reg_tl319.1982010118_1982123118-319.1987010118_1987123118.lee754697.nc.tar',
'TarFiles/anl_snow.066_snowd.reg_tl319.1988010118_1988123118-319.1993010118_1993123118.lee754697.nc.tar',
'TarFiles/anl_snow.066_snowd.reg_tl319.1994010118_1994123118-319.1999010118_1999123118.lee754697.nc.tar',
'TarFiles/anl_snow.066_snowd.reg_tl319.2000010118_2000123118-319.2005010118_2005123118.lee754697.nc.tar',
'TarFiles/anl_snow.066_snowd.reg_tl319.2006010118_2006123118-319.2011010118_2011123118.lee754697.nc.tar',
'TarFiles/anl_snow.066_snowd.reg_tl319.2012010118_2012123118-319.2015030118_2015033118.lee754697.nc.tar']
for file in filelist:
    filename=dspath+file
    file_base = os.path.basename(file)
    print('Downloading',file_base)
    req = requests.get(filename, allow_redirects=True, stream=True)
    with open(file_base, 'wb') as outfile:
        chunk_size=1048576
        for chunk in req.iter_content(chunk_size=chunk_size):
            outfile.write(chunk)
            check_file_status(file_base)
    print()
