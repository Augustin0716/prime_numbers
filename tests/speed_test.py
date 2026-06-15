import matplotlib.pyplot as plt
from time import time_ns

from src.prime_numbers import prime_generator

if __name__ == "__main__":
    # Testing for 10^n, 2.10^n and 5.10^n with n in {1, 2, 3, 4, 5}
    n_primes: list[int] = [j * 10 ** i for i in range(1, 5) for j in (1, 2, 5)]

    cal_time: list[float] = []  # First calculation
    redo_time: list[float] = []  # Cache reading

    for n in n_primes:
        # 1. First measure with calculation
        begin = time_ns()
        for j in prime_generator(n):
            pass
        end = time_ns()
        # ms conversion
        cal_time.append((end - begin) / 1_000_000)

        # 2. Following measures for reading time
        temp_redo = []
        for _ in range(3):  # 3 essais pour faire une moyenne propre
            begin = time_ns()
            for k in prime_generator(n):
                pass
            end = time_ns()
            temp_redo.append((end - begin) / 1_000_000)

        # Average for better precision
        redo_time.append(sum(temp_redo) / len(temp_redo))
        print(f"Time for {n=} primes calculated")

    # Result in the terminal
    print(f"{'N':<10} | {'Calculation time (ms)':<20} | {'Cache Reading time (ms)':<20}")
    print("-" * 58)
    for i, n in enumerate(n_primes):
        print(f"{n:<10} | {cal_time[i]:<20.4f} | {redo_time[i]:<20.4f}")

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
