#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Nishant Kumar
# Created Date: 20/06/2023
# ---------------------------------------------------------------------------
""" 
Calculate row-wise standard deviation in parallel
"""
import os
import sys
import numpy as np 
import pandas as po
import time

from mpi4py import MPI

#--------------------------------------------------
outDIR = "./out"

#- Number of rows of dummy array
ns = 1000000
#- Number of columns of dummy array
nv = 3
#- Number dummy arrays
nt = 51
#--------------------------------------------------

mpi_comm = MPI.COMM_WORLD
mpi_rank = mpi_comm.Get_rank()
mpi_size = mpi_comm.Get_size()

mpi_comm.Barrier()
start_time = time.time()

#- List of dummy files
dummyFILES = [os.path.join(outDIR, 'dummy_{0:05d}.csv'.format(t)) for t in range(nt)]
    
if mpi_rank == 0:
    #- Determine the size of each sub-task
    v, res = divmod(nt, mpi_size)
    taskSizePerRank = [v+1 if p<res else v for p in range(mpi_size)]
    #- Determine starting and ending indices of each sub-task
    startIndPerTask = [sum(taskSizePerRank[:p]) for p in range(mpi_size)]
    endIndPerTask = [sum(taskSizePerRank[:p+1]) for p in range(mpi_size)] 
    #- Split list of file indicies into list of arrays
    fileInd = np.arange(nt).tolist()
    fileIndPerRank = [fileInd[startIndPerTask[p]:endIndPerTask[p]] for p in range(mpi_size)]
else:
    fileIndPerRank = None

fileIndPerRank = mpi_comm.scatter(fileIndPerRank, root=0)
ntPerRank = len(fileIndPerRank)

#- Initialize
nsv = ns*nv
dummyArrayPerRank = np.zeros((nsv, ntPerRank))
sumPerRank = np.zeros(nsv)
sumAllRanks = np.zeros(nsv) #- NOTE: Defined for all ranks because of Allreduce
#-
sumDevPerRank = np.zeros(nsv)
sumDevAllRanks = np.zeros(nsv)

#- Step 1: Get mean
# print("Processor ", mpi_rank, " is processing ", len(fileIndPerRank), " indicies from", fileIndPerRank[0]," to ", fileIndPerRank[-1], flush=True)

for i in range(ntPerRank):
    dummyArrayPerRank[:,i] = po.read_csv(dummyFILES[fileIndPerRank[i]], 
                                         header=None, 
                                         delimiter="\t").to_numpy().reshape(nsv)
    sumPerRank += dummyArrayPerRank[:,i]

mpi_comm.Barrier()

avgg = np.empty(nsv)
mpi_comm.Allreduce(sumPerRank, sumAllRanks, op=MPI.SUM)
if mpi_rank == 0:
    avgg = sumAllRanks/nt
mpi_comm.Bcast([avgg, MPI.DOUBLE], root=0)

#- Step 2: Get deviation from mean
for i in range(ntPerRank):
    sumDevPerRank += (dummyArrayPerRank[:,i] - avgg)**2

mpi_comm.Barrier()

mpi_comm.Reduce(sumDevPerRank, sumDevAllRanks, op=MPI.SUM, root=0)

#- DONE!
if mpi_rank == 0:
    print("Mean: ", avgg.reshape((ns, nv)))
    print("Standard deviation: ", np.sqrt(sumDevAllRanks/nt).reshape((ns, nv)))
    print("Time  with ", mpi_size, " threads: ", int((time.time() - start_time) * 1000), "ms")
