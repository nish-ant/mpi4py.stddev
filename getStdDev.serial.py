#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Nishant Kumar
# Created Date: 20/06/2023
# ---------------------------------------------------------------------------
""" 
Calculate row-wise standard deviation in series
"""
import os
import sys
import numpy as np 
import pandas as po
import time

#--------------------------------------------------
outDIR = "./out"

#- Number of rows of dummy array
ns = 1000000
#- Number of columns of dummy array
nv = 3
#- Number dummy arrays
nt = 51

#--------------------------------------------------

#- List of dummy files
dummyFILES = [os.path.join(outDIR, 'dummy_{0:05d}.csv'.format(t)) for t in range(nt)]

#- Test
start_time = time.time()
nsv = int(ns*nv)
dummyArray = np.zeros((nsv, nt))
for i in range(nt):
    dummyArray[:,i] = po.read_csv(dummyFILES[i],
                                  header=None,
                                  delimiter="\t").to_numpy().reshape(nsv)
avgg = np.mean(dummyArray, axis=1)
stdDev = np.std(dummyArray, axis=1)

print("Mean: ", avgg.reshape((ns, nv)))
print("Standard deviation: ", stdDev.reshape((ns, nv)))
print("Time with 1 thread: ", int((time.time() - start_time) * 1000), "ms")
