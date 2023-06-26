## Computing standard deviation of arrays with mpi4py

This standard deviation calculator using mpi4py builds on top of the beautiful [MPI tutorial](https://github.com/mpitutorial/mpitutorial/tree/gh-pages/tutorials/mpi-reduce-and-allreduce/code) explaining the basic MPI collective communication routines.

The [supporting writeup](https://mpitutorial.com/tutorials/mpi-reduce-and-allreduce/) shows how the mean and standard deviation of numbers can be calculated using MPI.
This leads to a natural question: In mpi4py, how can the result of one scattered calculation be reused in a subsequent scattered calculation, basically utilizing the same communicator?
One such use case is the calculation of standard deviation which requires the knowledge of the mean of the samples.

Here is a note on the calculation of standard deviation using [`numpy.std`](https://numpy.org/doc/stable/reference/generated/numpy.std.html) routine:
> The standard deviation is the square root of the average of the squared deviations from the mean, i.e., `std = sqrt(mean(x))`, where `x = abs(a - a.mean())**2`.

As it can be seen, the first step of calculating the mean of the samples is a prerequisite for the second step of calculating the standard deviation. 

In our case, we consider `a` as arrays.
For a small sample size (i.e., number of arrays) and a small size of arrays, the usual way to obtain the mean and standard deviation is by using the NumPy routines [`numpy.mean`](https://numpy.org/doc/stable/reference/generated/numpy.mean.html) and [`numpy.std`](https://numpy.org/doc/stable/reference/generated/numpy.std.html).
However, in a parallel implementation where the sample and/or array sizes are large, it is more computationally efficient to (1) use the calculated mean during the standard deviation calculation instead of recalculating it, and (2) store the sample during the mean calculation to avoid reloading the sample during the standard deviation calculation.

These methods have been implemented in the parallel computation script.
A serial script is also provided which uses the NumPy routines to verify the results of the parallel computation and compare the elapsed times.
The element-wise standard deviation calculation is performed on randomly sampled NumPy arrays.

PS: The parallel script is compatible with cases where the number of samples is not divisible by the number of processes.

### Run 

The slurm submission script can be used to run the scripts
```
sbatch runscript.slurm
```

### Output
```
Generating dummy data ...
Time elapsed:  164957 ms
==============================
Running serial script ...
Mean:  [[5.0028527  5.00365992 4.97916552]
 [5.04849867 4.9980646  5.03206646]
 [4.99554776 5.00845768 5.02780605]
 ...
 [5.01122506 4.97549703 4.97647117]
 [5.02473242 4.97633701 5.02926336]
 [5.05241078 5.02850346 4.97638916]]
Standard deviation:  [[0.1424992  0.13906888 0.1280675 ]
 [0.12587326 0.1452911  0.13690477]
 [0.14622958 0.14540251 0.16003446]
 ...
 [0.1342657  0.157672   0.17471566]
 [0.1477725  0.1465435  0.14231573]
 [0.15484877 0.14018003 0.15221547]]
Time with 1 thread:  26065 ms
==============================
Running parallel script ...
Mean:  [[5.0028527  5.00365992 4.97916552]
 [5.04849867 4.9980646  5.03206646]
 [4.99554776 5.00845768 5.02780605]
 ...
 [5.01122506 4.97549703 4.97647117]
 [5.02473242 4.97633701 5.02926336]
 [5.05241078 5.02850346 4.97638916]]
Standard deviation:  [[0.1424992  0.13906888 0.1280675 ]
 [0.12587326 0.1452911  0.13690477]
 [0.14622958 0.14540251 0.16003446]
 ...
 [0.1342657  0.157672   0.17471566]
 [0.1477725  0.1465435  0.14231573]
 [0.15484877 0.14018003 0.15221547]]
Time  with  16  threads:  2746 ms
==============================
DONE!
Runtime: 196.288695675
```