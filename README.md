# Polynomial Multiplication

Python script which compares the execution times of a naive algorithm for polynomial multiplication and one which is implemented with the _Fast Fourier Transform_.

To get info for the Command line interface run:
```
python3 polynomial_multiplication.py --help
```
See also the [online documentation](https://docs.python.org/3/library/timeit.html#timeit.repeat) for the function `timeit.repeat` for details.

You can use `jobcommit.sh` to run the script on a [SLURM](https://slurm.schedmd.com/)-Cluster. Make sure you change the partition name to an appropriate value before you run the script. All command line arguments for `jobcommit.sh` are passed to the python script.