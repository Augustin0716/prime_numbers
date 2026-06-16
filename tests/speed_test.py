from itertools import accumulate
import matplotlib.pyplot as plt
from time import time_ns
from typing import Callable

from src.prime_numbers import prime_generator, __primes, __unordered_primes

if __name__ == "__main__":
    temp_primes: list[int] = __primes
    temp_unordered_primes: set[int] = __unordered_primes
    __primes = [] # resetting so the test works properly
    __unordered_primes = set() # idem
    # Testing for 10^n, 2.10^n and 5.10^n with n in {1, 2, 3, 4, 5}
    n_primes: list[int] = [j * 10 ** i for i in range(1, 5) for j in (1, 2, 5)]

    cal_time: list[float] = []  # First calculation
    redo_time: list[float] = []  # Cache reading

    to_millis: Callable[[int], float] = lambda a: a / 1_000_000
    # Time tests
    for n in n_primes:
        # 1. First measure with calculation
        begin = time_ns()
        for j in prime_generator(n):
            pass
        end = time_ns()

        cal_time.append(to_millis(end - begin))

        # 2. Following measures for reading time
        temp_redo = []
        for _ in range(3):  # 3 essais pour faire une moyenne propre
            begin = time_ns()
            for k in prime_generator(n):
                pass
            end = time_ns()
            temp_redo.append(to_millis(end - begin))

        # Average for better precision
        redo_time.append(sum(temp_redo) / len(temp_redo))
        print(f"Time for {n=} primes calculated")

    # Data manipulation
    cal_time = list(accumulate(cal_time)) # since

    # Result in the terminal
    print(f"{'N':<6} | {'Calculation time (ms)':<20} | {'Cache Reading time (ms)':<20}")
    print("-" * 60)
    for i, n in enumerate(n_primes):
        print(f"{n:<6} | {cal_time[i]:<20.4f} | {redo_time[i]:<20.4f}")

    # MatPlotLib plot
    plt.figure(figsize=(10, 6))

    plt.plot(n_primes, cal_time, label="First run (Generation)", marker='o', color='red', linewidth=2)
    plt.plot(n_primes, redo_time, label="Following run (Cache pkl)", marker='s', color='green', linewidth=2)

    plt.xscale('log')
    plt.xlabel("Number of primes (n)", fontsize=12)
    plt.ylabel("Run time (milliseconds)", fontsize=12)
    plt.title("Time taken to generate or read n primes", fontsize=14, fontweight='bold')
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.legend(fontsize=11)

    plt.show()
    # if more numbers have been generated before, we put them back, else the 50,000 primes will be saved as is
    if len(__primes) < len(temp_primes):
        __primes = temp_primes
    __unordered_primes = temp_unordered_primes # putting the set back as is, since it should be empty.
