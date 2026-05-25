from itertools import accumulate
import matplotlib.pyplot as plt
from time import time_ns, time

from src.prime_numbers import *

def timeit(f):
    def timed(*args, **kw):
        ts = time_ns()
        result = f(*args, **kw)
        te = time_ns()
        return result
    return timed

if __name__ == "__main__":
    n_primes: list[int] = [10**i for i in range(2,5)]
    cal_time: list[int] = [0]*(l := len(n_primes))
    redo_time: list[int] = [0]*l
    c = []
    for i, n in enumerate(n_primes):
        begin = time_ns()
        for j in prime_generator(n):
            pass
        end = time_ns()
        cal_time[i] = end - begin
        for j in [0, 1, 2]:
            begin = time_ns()
            for k in prime_generator(n):
                pass
            end = time_ns()
            redo_time[j] = end - begin
    cal_time = list(accumulate(cal_time))

    print(cal_time)
    print(redo_time)

    plt.plot(n_primes,cal_time, 'r.', n_primes,redo_time, 'b.')
    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('Time (ns)')
    plt.xlabel('number of primes (log)')
    plt.legend()
    plt.title("Time taken to calculate prime numbers")
    plt.show()
