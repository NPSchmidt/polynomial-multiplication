import argparse
import cmath
import random
import timeit

try:
    _ = list[int]
    List = list
except TypeError:
    # Python < 3.9 support
    from typing import List


def prod_naive(a: List[int], b: List[int]) -> List[int]:
    p = [0] * (len(a) + len(b) - 1)
    for k, a_k in enumerate(a):
        for j, b_j in enumerate(b):
            p[k + j] += a_k * b_j
    return p


def prod_fft(a: List[int], b: List[int]) -> List[int]:
    def evaluate_fft(a: List[int]) -> List[int]:
        n = len(a)
        if n == 1:
            return a
        # Coefficients with even indices
        a_g = a[::2]
        # Coefficients with odd indices
        a_u = a[1::2]
        # Evaluate recursively
        y_g = evaluate_fft(a_g)
        y_u = evaluate_fft(a_u)
        # Calculate principal root of unity
        omega = cmath.exp(complex(imag=2*cmath.pi/n))
        omega_current = 1
        # Create result vector of length n
        y = [0] * n
        n_half = n // 2
        for k in range(n_half):
            # Fill result vector
            y[k] = y_g[k] + omega_current * y_u[k]
            y[n_half + k] = y_g[k] - omega_current * y_u[k]
            omega_current *= omega
        return y

    def interpolate_ifft(y: List[int]) -> List[int]:
        n = len(y)
        if n == 1:
            return y
        y_g = y[::2]
        y_u = y[1::2]
        # Coefficients with even indices
        a_g = interpolate_ifft(y_g)
        # Coefficients with odd indices
        a_u = interpolate_ifft(y_u)
        # Calculate inverse of principal root of unity
        omega = cmath.exp(complex(imag=-2*cmath.pi/n))
        omega_current = 1
        # Create result vector of length n
        a = [0] * n
        n_half = n // 2
        for k in range(n_half):
            # Fill result vector
            a[k] = a_g[k] + omega_current * a_u[k]
            a[n_half + k] = a_g[k] - omega_current * a_u[k]
            omega_current *= omega
        return a

    n = len(a)
    assert n == len(b)
    # Double the size of the coefficient representations by filling them up with zeros
    # and convert them to point-value representations
    y_a = evaluate_fft(a + [0]*n)
    y_b = evaluate_fft(b + [0]*n)
    n *= 2
    # Pointwise multiplication of the point-value representations
    y_p = [y_a_k * y_b_j for y_a_k, y_b_j in zip(y_a, y_b)]
    # Convert the point-value representation of the product back to a coefficient representation
    p_times_n = interpolate_ifft(y_p)
    # Divide every element in p_times_n by n to compute the result p
    return list(map(lambda x: x / n, p_times_n))


def generate_coefficients(n):
    return random.choices(range(-10, 10), k=n)


def main(args):
    def print_result(impl_name: str, result_list: List[float]):
        print(f'{impl_name}:\n'
              f'Minimum: {min(result_list)} seconds\n'
              f'Average: {sum(result_list) / len(result_list)} seconds\n'
              f'All:     {result_list}\n')

    k = args.k
    n = 2**k
    number = args.number
    repeat = args.repeat
    print(f'Running polynomial multiplication with n={n}=2^{k} {number} times with {repeat} repetitions\n')

    print('Start naive implementation:')
    t_naive = timeit.repeat('prod_naive(a, b)', repeat=repeat, number=number,
                            setup='a = generate_coefficients(n); b = generate_coefficients(n)',
                            # Pass all locals and globals so all used functions are visible
                            globals={**locals(), **globals()})
    print_result('Naive implementation', t_naive)

    print('Start FFT:')
    t_fft = timeit.repeat('prod_fft(a,b)', repeat=repeat, number=number,
                          setup='a = generate_coefficients(n); b = generate_coefficients(n)',
                          # Pass all locals and globals so all used functions are visible
                          globals={**locals(), **globals()})
    print_result('FFT implementation', t_fft)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', default=8, type=int, help='n=2^k will be the degree-bound of the polynomial')
    parser.add_argument('--number', default=100, type=int, help='The number of executions for one repeat')
    parser.add_argument('--repeat', default=1, type=int, help='The number of repeats timeit.repeat')
    main(parser.parse_args())
