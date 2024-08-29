#!/usr/bin/env python
#################################################################
# Python Script to retrieve 3 online Data files of 'd640000',
# total 4.08G. This script uses 'requests' to download data.
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

dspath = 'https://request.rda.ucar.edu/dsrqst/LEE754702/'
filelist = [
'TarFiles/754702.snod-sfc-an-gauss.jra3q.anl_snow.0_1_11.snod-sfc-an-gauss.1947090118_1947093018-1975100118_1975103118.nc.tar',
'TarFiles/754702.snod-sfc-an-gauss.jra3q.anl_snow.0_1_11.snod-sfc-an-gauss.1975110118_1975113018-2005010118_2005013118.nc.tar',
'TarFiles/754702.snod-sfc-an-gauss.jra3q.anl_snow.0_1_11.snod-sfc-an-gauss.2005020118_2005022818-2021010118_2021013118.nc.tar']
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
