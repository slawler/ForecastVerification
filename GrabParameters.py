# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 20:04:01 2016
v4 with #1,#2 & #3 Tests
@author: slawler
"""

import pandas as pd
import numpy as np
import scipy.sparse as sp
from scipy import stats
import os
from matplotlib import pyplot as plt
from glob import glob
import linecache
'''
#--Testing Dataset
PATH     = '/home/slawler/Desktop/SREM2D/working/subset'
qpf_file = os.path.join(PATH,'QPF_SREM2D_part.txt')
mpe_file = os.path.join(PATH,'ordered_MPE_SREM2D_part.txt')
qpf_idx  = os.path.join(PATH,'SREM2D_Files_part.txt')
'''
#--Full Dataset
PATH     = '/home/slawler/Desktop/SREM2D/working'
qpf_file = os.path.join(PATH,'QPF_SREM2D.txt')
mpe_file = os.path.join(PATH,'ordered_MPE_SREM2D.txt')
qpf_idx  = os.path.join(PATH,'SREM2D_Files.txt')

read_qpf_idx = pd.read_csv(qpf_idx, usecols = ['file'])
grid_idx = list(pd.Series(read_qpf_idx['file']))
idx_dict  = {}

#---Make Dictionary of grids
lines = np.arange(0,10)
for i in range(0,len(grid_idx)):
    grid = lines + 10*i
    idx_dict[grid_idx[i]]=grid
       
    
#1. Probability of Detection    
#partial = grid_idx[0:300]#---sample for testing
#for g in grid_idx: #- Full Run when testing is complete
total_1 = 0; count_1 = 0
total_2 = 0; count_2 = 0
part3 = []
for i, g in enumerate(grid_idx):
    print i   
    df_mpe = pd.DataFrame(index=range(0,9),columns=[lines], dtype='float')
    df_qpf = pd.DataFrame(index=range(0,9),columns=[lines], dtype='float')   
    for l in range(9):
        CURRENT_LINE = idx_dict[g][l]
        mpe_grid_members = linecache.getline(mpe_file,CURRENT_LINE +1).split()
        qpf_grid_members = linecache.getline(qpf_file,CURRENT_LINE +1).split()         
        df_mpe.loc[l] = np.array(mpe_grid_members)
        df_qpf.loc[l] = np.array(qpf_grid_members)
        
    df_mpe = df_mpe.apply(pd.to_numeric)
    df_qpf = df_qpf.apply(pd.to_numeric)
    
    mpe_non0 = df_mpe[df_mpe > 0]
    mpe_0    = df_mpe[df_mpe == 0]
    x1,y1 = sp.coo_matrix(mpe_non0.notnull()).nonzero()
    x2,y2 = sp.coo_matrix(mpe_0.notnull()).nonzero()   
    a1 = (list(zip(x1,y1))); a2 = (list(zip(x2,y2)))
        
    for j, val in enumerate(a1):
        count_1 += 1
        obsvd = mpe_non0.loc[val[0],val[1]]
        fcast = df_qpf.loc[val[0],val[1]]
        try:        
            if fcast == 0:
                if j == 0:  #Skip if no values registerd (a2 is a null matrix)
                    print 'No Detect for grids Part 1', g 
                else:
                    continue
            else:
                total_1 +=1    
        except: 
            print 'These arent the drones youre looking for'
    

    for j, val in enumerate(a2):
        count_2 += 1
        obsvd  = mpe_0.loc[val[0],val[1]]
        fcast2 = df_qpf.loc[val[0],val[1]]
        try:        
            if fcast2 == 0:
                if j == 0: #Skip if no values registerd (a2 is a null matrix)
                    print 'No Detect for grids Part 2', g 
                else:
                    continue
            else:
                total_2 +=1
                part3.append(fcast2)
        except: 
            print 'These arent the drones youre looking for'
        

part1  =float(total_1)/float(count_1)
part2  =1 - float(total_2)/float(count_2)               
print total_1, count_1,part1 
print total_2, count_2,part2
nobs,minmax,mean,var,skew,kurt = stats.describe(part3) 
min = minmax[0] 
max = minmax[1]

P = stats.expon.fit(part3)
print P

rX = np.linspace(min,max,1000)
rP = stats.expon.pdf(rX, *P)

plt.hist(part3, normed=True)
plt.plot(rX, rP)

f = stats.expon.pdf(P)


'''
print stats.describe(part3)
DescribeResult(nobs=90, minmax=(0.0, 0.21166699999999999), mean=0.12770372222222223, variance=0.0029818122570118592, skewness=-0.051686256155266654, kurtosis=-0.8921117113187864)
'''
