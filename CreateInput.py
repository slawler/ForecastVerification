# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 10:53:31 2016

@author: slawler
"""

import os,tarfile, gzip
import pandas as pd

f_type = 'MPE'

ListPath  = '/home/slawler/Desktop/SREM2D/SREM2D_Files.txt'
grid_list = pd.read_csv(ListPath, sep = '\t', usecols = ['file']) 
comp_grids = list(pd.Series(grid_list['file']))

PATH = '/home/slawler/Desktop/SREM2D/working/test'
file_dir = os.path.join(PATH,'%s_SREM2D.txt' %f_type)
log_dir = os.path.join(PATH,'%s_LOG.txt' %f_type)

tarzip = 'ascii.tar.gz'
tar = tarfile.open(tarzip)
files = tar.getnames()
for i, f in enumerate(files):
    if f in comp_grids:
        print i, f         
        opengrid = tar.extractfile(f)       
        readgrid = pd.read_csv(opengrid, header = None, skiprows = 6)
        readgrid.to_csv(file_dir, mode = 'a', header = False, index = False)
        with open(file_dir,'a') as f_in: f_in.write('\n')
        with open(log_dir,'a') as log: log.write(f+'\n')
    else:
        continue
tar.close()
