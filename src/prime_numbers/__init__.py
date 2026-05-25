from collections.abc import Generator

from .prime_crible import PrimeCrible

__all_ = [
    "is_prime",
    "prime_generator",
    "PrimeCrible"
]

__primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]

__unordered_primes: set[int] = set()

bases_to_add: dict[int, int | list[int]] = {
    2047: 2,
    1_373_653: 3,
    25_326_001: 5,
    3_215_031_751: 7,
    2_152_302_898_747: 11,
    3_474_749_660_383: 13,
    341_550_071_728_321: 17,
    3_825_123_056_546_413_051: [19, 23],
    318_665_857_834_031_151_167_461: [29, 31, 37],
    3_317_044_064_679_887_385_961_981: 41
}


def is_prime(n: int) -> bool:
    """
    Checks whether a number is prime, using Miller-Rabin algorithm.
    It is deterministic if n < 3317044064679887385961981. Above this threshold, there is a small chance for error.
    The least chance for error, the more time it needs to answer.
    :param n: number which is to be checked
    :return: True if n is prime, False otherwise
    """
    if n in __primes:
        return True
    elif n in __unordered_primes:
        return True
    elif n % 2 == 0:
        return False
    elif n < __primes[-1]:
        return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2

    bases = []

    for limit, base in bases_to_add.items():
        if isinstance(base, int):
            bases.append(base)
        else:
            bases += base
        if n <= limit:
            break
    else:
        print(f"Warning, the test is not deterministic for {n = }")

    for a in bases:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    __unordered_primes.add(n)
    return True


def prime_generator(n_primes: int = float("inf")) -> Generator[int, None, None]:
    """
    Yields n_primes primes numbers, starting from 2. If n_primes is not precised, it takes as default infinity, meaning
    the generator is infinite and will never raise StopIteration.
    :param n_primes: the number of primes to generate, by default +infinity
    :return: a generator that yields primes, either finite or infinite
    """
    dispensed: int = 0
    primes = iter(__primes)
    for p in primes:
        if dispensed > n_primes:
            return
        else:
            yield p

    candidate: int = __primes[-1]
    while dispensed < n_primes:
        candidate += 2
        if candidate in __unordered_primes:
            __primes.append(candidate)
            yield candidate
        if is_prime(candidate):
            dispensed += 1
            __primes.append(candidate)
            yield candidate


if __name__ == '__main__':
    number: int = 0
    gen = prime_generator()
    print(type(gen))
    while number < 500:
        number = next(gen)
        print(number)