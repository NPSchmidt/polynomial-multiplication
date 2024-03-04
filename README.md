# Polynomial Multiplication

Python script for a seminar paper which compares the execution times of two algorithms for polynomial multiplication. The first algorithm is a naive approach which uses the distributivity of (complex number) multiplication.The other one is a more efficient approach which uses _Fast Fourier Transform_.

The script has the following usage:
```
polynomial_multiplication.py [-h] [-k K] [--number NUMBER] [--repeat REPEAT]
```
with these meanings of the command line options:
```
  -h, --help       show the help message and exit
  -k K             n=2^k will be the degree-bound of the polynomial, default value: 8
  --number NUMBER  The number of executions for one repeat, default value: 100
  --repeat REPEAT  The number of repeats timeit.repeat, default value: 1
```
See also the [online documentation](https://docs.python.org/3/library/timeit.html#timeit.repeat) for the function `timeit.repeat` for details.

You can use `jobcommit.sh` to run the script on a [SLURM](https://slurm.schedmd.com/)-Cluster. Make sure you change the partition name to an appropriate value before you run the script. All command line arguments for `jobcommit.sh` are passed to the python script. So to reproduce the experiment from my seminar paper you can run, after replacing K with an integer between 6 and 12:
```
sbatch jobcommit.sh -k K --number 1000 --repeat 4
```