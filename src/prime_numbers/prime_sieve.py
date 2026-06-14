from abc import ABC
from array import array
from collections.abc import Generator
from itertools import repeat
from numbers import Real
from math import isqrt
from typing import runtime_checkable, Protocol, Self

C = 67 # composite
P = 80 # prime
# both variables are ASCII code, it is useful to represent primes and composites in __str__ and __bytes__
# Also makes good beacons in the code without verbose


@runtime_checkable
class SupportsPrime(Protocol):
    primes: int


class PrimeSieveBase(ABC):
    """
    Abstract base class for PrimeSieve and PrimeSieveSlice. Regroups dunders and methods that are common to both class.
    """
    _sieve: array
    _n_primes: int
    _n_composites: int

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Real):
            return self._n_primes < float(other)
        elif isinstance(other, SupportsPrime):
            return self._n_primes < other.primes
        else:
            return NotImplemented

    def __le__(self, other: object):
        if isinstance(other, Real):
            return self._n_primes <= float(other)
        elif isinstance(other, SupportsPrime):
            return self._n_primes <= other.primes
        else:
            return NotImplemented

    def __gt__(self, other: object) -> bool:
        if isinstance(other, Real):
            return self._n_primes > other
        elif isinstance(other, SupportsPrime):
            return self._n_primes > other.primes
        else:
            return NotImplemented

    def __ge__(self, other: object) -> bool:
        if isinstance(other, Real):
            return self._n_primes >= other
        elif isinstance(other, SupportsPrime):
            return self._n_primes >= other.primes
        else:
            return NotImplemented

    @property
    def composites(self) -> int:
        return self._n_composites

    @property
    def primes(self) -> int:
        return self._n_primes


class PrimeSieve(PrimeSieveBase):
    """
    A class whose objects are Eratosthenes's sieve.

    Can:

    - return the number of primes from 0 to n (0 included, n excluded)
    - return the number of composite from 0 to n
    - return whether a number within its range is prime (True) or composite (False)
    - return a slice (PrimeSieveSlice object) with the same properties
    """
    def __init__(self, n: int) -> None:
        self.n = n
        self._sieve = array('B', [P] * n)
        self._sieve[0] = self._sieve[1] = C

        self._sift()

        self._n_composites = self._sieve.count(C)
        self._n_primes = self._sieve.count(P)

    def _sift(self):
        """
        Executes order 66.
        Just kidding, executes Eratosthenes's algorithm on _sieve.
        """
        limit = isqrt(self.n) + 1

        self._sieve[4::2] = array('B', [C] * len(self._sieve[4::2]))

        for i in range(3, limit, 2):
            if self._sieve[i] == P:
                begin = i*i
                step = 2*i
                length: int = len(self._sieve[begin::step])
                self._sieve[begin::step] = array('B', repeat(C, length))

    def __eq__(self, other):
        if isinstance(other, PrimeSieve):
            return self.n == other.n
        else:
            return NotImplemented

    def __repr__(self):
        return f"PrimeSieve(n={self.n})"

    def __str__(self) -> str:
        """
        Return a string representing the sieve, such as str[n] = "P" if n is prime and "C" if composite
        For instance, str(PrimeSieve(10)) returns 'CCPPCPCPCC'
        """
        return self._sieve.tobytes().decode()

    def __bytes__(self) -> bytes:
        """
        Return a byte array representing the sieve, such as bytes[n] = b'P' if n is prime and b'C' if composite.
        For instance, bytes(PrimeSieve(10)) return b'CCPPCPCPCC'
        """
        return self._sieve.tobytes()

    def __bool__(self) -> bool:
        return bool(self._sieve)

    def __len__(self):
        return len(self._sieve)

    def __contains__(self, key: int):
        if not isinstance(key, int):
            return False
        else:
            return 0 <= key < len(self._sieve)

    def __getitem__(self, i: int | slice) -> bool | Self:
        """
        If an integer is given, returns its primality as True if prime or False if composite.
        If a slice is given, returns a PrimeSieveSlice object, which contains the range of number given by the slice.
        :param i: either an integer whose primality is to be tested or a slice
        :return: Either the primality of a number as a boolean (True if prime) or a PrimeSieveSlice
        """
        if isinstance(i, int):
            return self._sieve[i] == P
        elif isinstance(i, slice):
            return PrimeSieveSlice(self._sieve, i)
        else:
            raise TypeError(f"Type {type(i).__name__} is not supported")

    def __iter__(self) -> Generator[tuple[int, bool], None, None]:
        """
        Yields every number from 0 to n and True if the number is prime, False otherwise.
        For instance: (0, False), (1, False), (2, True), ..., (n-1, primality(n-1))
        :return: a Generator yielding a number and its primality as a boolean
        """
        for number, is_prime in enumerate(self._sieve):
            yield number, is_prime == P


class PrimeSieveSlice(PrimeSieveBase):
    def __init__(self, sieve: array, number_range: slice):
        self._sieve = sieve # it gets the whole object (as a shallow copy, no data created here)
        self._slice = slice(
            number_range.start if number_range.start is not None else 0,
            number_range.stop if number_range.stop is not None else len(self._sieve),
            number_range.step if number_range.step is not None else 1
        ) # a completely defined slice is needed for later
        self._numbers: range = range(self._slice.start, self._slice.stop, self._slice.step)

        self._n_primes = self._sieve[self._slice].count(P)
        self._n_composites = len(self._numbers) - self._n_primes # not slicing _sieve twice

    def __eq__(self, other):
        if isinstance(other, PrimeSieveSlice):
            return self._numbers == other._numbers
        elif isinstance(other, PrimeSieve):
            return self._numbers == range(other.n)
        else:
            return NotImplemented

    def __repr__(self):
        """Return repr(self). It should be noted that eval(repr(self)) raises an error."""
        return f"PrimeSieveSlice[{self._slice.start}:{self._slice.stop}:{self._slice.step}]"

    def __str__(self):
        """
        Returns a string representing the sieve slice, such as str[n] = "P" if n is prime and "C" if composite.
        """
        return self._sieve[self._slice].tobytes().decode()

    def __bytes__(self) -> bytes:
        """
        Returns a byte array representing the sieve slice, such as str[n] = b'P' if n is prime and b'C' if composite.
        """
        return self._sieve[self._slice].tobytes()

    def __bool__(self):
        return bool(self._numbers) > 0

    def __len__(self) -> int:
        return len(self._numbers)

    def __contains__(self, key):
        if not isinstance(key, int):
            return False
        else:
            return key in self._numbers

    def __getitem__(self, i: int | slice) -> bool | Self:
        """
        If an integer is given, returns its prime as True if prime or False if composite.
        If a slice is given, returns a PrimeSieveSlice object, which contains the range of number given by the slice.
        It should be noted that PrimeSieve(n)[s1][s2] is equal to PrimeSieve(n)[s2][s1].
        :param i: either an integer whose primality is to be tested or a slice
        :return: either the primality of i as a boolean (True if prime) or a PrimeSieveSlice
        """
        if isinstance(i, int):
            index: int = self._numbers[i] # real index
            return self._sieve[index] == P
        elif isinstance(i, slice):
            # using the slice on the range _numbers allows us to get the "real" slice
            r = self._numbers[i]
            s = slice(r.start, r.stop, r.step)
            return PrimeSieveSlice(self._sieve, s)
        else:
            raise TypeError(f"Type {type(i).__name__} is not supported")

    def __iter__(self) -> Generator[tuple[int, bool], None, None]:
        """
        Yields every number from 0 to n and True if the number is prime, False otherwise.
        :return: a Generator yielding a number and its primality as a boolean
        """
        for number in self._numbers:
            yield number, self._sieve[number] == P

    @property
    def slice_(self) -> slice:
        return self._slice
