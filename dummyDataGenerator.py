#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Nishant Kumar
# Created Date: 20/06/2023
# ---------------------------------------------------------------------------
""" 
Generate csv files with dummy data 
"""
import os
import numpy as np 
from pathlib import Path
import time

np.random.seed(seed=10)

#--------------------------------------------------
#- Output directory
outDIR = "./out"

#- Number of rows of dummy array
ns = 1000000
#- Number of columns of dummy array
nv = 3
#- Number dummy arrays
nt = 51

#- Mean and standard deviation of Gaussian distribution 
#- NOTE: The distribution is used to draw random samples
dummyMean = 5.0
dummyStd = 0.15

#--------------------------------------------------

#- Make output directory
Path(outDIR).mkdir(parents=True, exist_ok=True)

#- Loop to geenrate and save dummy data
start_time = time.time()
for i in range(nt):
    dummyArray = np.random.normal(loc=dummyMean, 
                                  scale=dummyStd, 
                                  size=(ns, nv))
    dummyFILE = os.path.join(outDIR, 'dummy_{0:05d}.csv'.format(i))
    np.savetxt(dummyFILE, dummyArray, delimiter='\t')
print("Time elapsed: ", int((time.time() - start_time) * 1000), "ms")
