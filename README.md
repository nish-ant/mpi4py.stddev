## Computing standard deviation of numbers with mpi4py

This standard deviation calculator using mpi4py builds on top of the beautiful [MPI tutorial](https://github.com/mpitutorial/mpitutorial/tree/gh-pages/tutorials/mpi-scatter-gather-and-allgather/code).

The [supporting document](https://mpitutorial.com/tutorials/mpi-scatter-gather-and-allgather/) shows how the average of numbers can be calculated using MPI collective communication routines.
This leads to a natural question: how can the results of one scattered calculation be reused for subsequent scattered calculation while using the same communicator?
One such use case is calculation of standard deviation using the mean calculated in a previous step.

Here is a note on the calculation of standard deviation using [`numpy.std`](https://numpy.org/doc/stable/reference/generated/numpy.std.html):
> The standard deviation is the square root of the average of the squared deviations from the mean, i.e., `std = sqrt(mean(x))`, where `x = abs(a - a.mean())**2`.

As it can be seen, the mean over the whole range of data must be known before calculating the standard deviation.

The scripts for both the serial and parallel computations are provided.
The element-wise standard deviation calculation is performed on randomly sampled numpy arrays.
In addition, the parallel script also takes care of the cases when the number of arrays isn’t divisible by the number of processes.

## Output
```
Generating dummy data ...
Time elapsed:  172316 ms
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
Time with 1 thread:  25429 ms
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
Time  with  16  threads:  2702 ms
==============================
DONE!
Runtime: 202.262141461
```