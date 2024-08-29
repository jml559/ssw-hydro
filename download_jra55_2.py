#!/usr/bin/env python
#################################################################
# Python Script to retrieve 2 online Data files of 'd628000',
# total 3.6G. This script uses 'requests' to download data.
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

dspath = 'https://request.rda.ucar.edu/dsrqst/LEE754696/'
filelist = [
'TarFiles/anl_land.225_soilw.reg_tl319.2020010100_2020013118-319.2020060100_2020063018.lee754696.nc.tar',
'TarFiles/anl_land.225_soilw.reg_tl319.2020070100_2020073118-319.2021010100_2021013118.lee754696.nc.tar']
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
