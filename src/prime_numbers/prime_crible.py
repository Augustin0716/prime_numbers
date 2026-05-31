from abc import ABC
from array import array
from collections.abc import Generator
from numbers import Real
from math import isqrt
from typing import runtime_checkable, Protocol

C = 67 # composite
P = 80 # prime


@runtime_checkable
class SupportsPrime(Protocol):
    primes: int


class PrimeAttributes(Protocol):
    _crible: array
    _n_primes: None | int
    _n_composites: None | int


class PrimeCribleBase(ABC, PrimeAttributes):
    """
    Abstract base class for PrimeCrible and PrimeCribleSlice. Regroups dunders and methods that are common to both class.
    """
    def __str__(self) -> str:
        """
        Return a string representing the crible, such as str[n] = "P" if n is prime and "C" if composite
        For instance, str(PrimeCrible(10)) returns 'CCPPCPCPCC'
        """
        return self._crible.tobytes().decode("ascii")

    def __bytes__(self) -> bytes:
        """
        Return a byte array representing the crible, such as bytes[n] = b'P' if n is prime and b'C' if composite.
        For instance, bytes(PrimeCrible(10)) return b'CCPPCPCPCC'
        """
        return self._crible.tobytes()

    def __bool__(self) -> bool:
        return len(self._crible) > 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, (PrimeCribleSlice, PrimeCrible)):
            return NotImplemented
        else:
            return str(self) == str(other)

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, (PrimeCribleSlice, PrimeCrible)):
            return NotImplemented
        else:
            return str(self) != str(other)

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


class PrimeCrible(PrimeCribleBase):
    """
    A class whose objects are Eratosthenes's crible.

    Can:

    - return the number of primes from 0 to n (0 included, n excluded)
    - return the number of composite from 0 to n
    - return whether a number within its range is prime (True) or composite (False)
    - return a slice (PrimeCribleSlice object) with the same properties
    """
    def __init__(self, n: int) -> None:
        self.n = n
        self._crible = array('B', [P] * n)
        self._crible[0] = self._crible[1] = C

        self._n_primes: None | int = None
        self._n_composites: None | int = None

        self._sift()

    def _sift(self):
        """
        Executes order 66.
        Just kidding, executes Eratosthenes's algorithm on _crible.
        """
        limit = isqrt(self.n) + 1

        self._crible[4::2] = array('B', [C] * len(self._crible[4::2]))

        for i in range(3, limit + 1, 2):
            if self._crible[i] == P:
                b = i*i
                s = 2*i
                l: int = len(self._crible[b::s])
                self._crible[b::s] = array('B', [C] * l)

    def __repr__(self):
        return f"PrimeCrible(n={self.n})"

    def __contains__(self, item: int):
        if not isinstance(item, int):
            return False
        elif 0 <= item < len(self._crible):
            return True
        else:
            return False

    def __getitem__(self, n):
        if isinstance(n, int):
            return self._crible[n] == P
        elif isinstance(n, slice):
            if self._crible[n] == self._crible:
                return self
            else:
                return PrimeCribleSlice(self._crible, n)
        else:
            raise TypeError(f"Type {type(n).__name__} is not supported")

    def __iter__(self) -> Generator[tuple[int, bool], None, None]:
        """
        Yields every number from 0 to n and True if the number is prime, False otherwise.
        For instance: (0, False), (1, False), (2, True), ..., (n-1, primality(n-1))
        :return: a Generator yielding a number and its primality as a boolean
        """
        for number, is_prime in enumerate(self._crible):
            yield number, is_prime == P

    @property
    def composites(self) -> int:
        """Returns the number of composites from 0 to n"""
        if self._n_composites is None:
            self._n_composites = self._crible.count(C)
        return self._n_composites

    @property
    def primes(self) -> int:
        """Returns the number of primes from 0 to n"""
        if self._n_primes is None:
            self._n_primes = self._crible.count(P)
        return self._n_primes


class PrimeCribleSlice(PrimeCribleBase):
    def __init__(self, crible: array, number_range: slice):
        self._crible = crible
        self._slice = slice(
            number_range.start if number_range.start is not None else 0,
            number_range.stop if number_range.stop is not None else len(self._crible),
            number_range.step if number_range.step is not None else 1
        ) # a completely defined slice is needed for later
        self._numbers: range = range(self._slice.start, self._slice.stop, self._slice.step)

        self._n_primes: None | int = None
        self._n_composites: None | int = None

    @property
    def composites(self) -> int:
        if self._n_composites is None:
            self._n_composites = self._crible[self._slice].count(C)
        return self._n_composites

    @property
    def primes(self) -> int:
        if self._n_primes is None:
            self._n_primes = self._crible[self._slice].count(P)
        return self._n_primes

    @property
    def slice_(self):
        return self._slice

    def __len__(self) -> int:
        return len(self._numbers)

    def __repr__(self):
        return f"PrimeCribleSlice[{self._slice.start}:{self._slice.stop}:{self._slice.step}]"

    def __str__(self):
        return self._crible[self._slice].tobytes().decode("ascii")

    def __bytes__(self) -> bytes:
        return self._crible[self._slice].tobytes()

    def __iter__(self) -> Generator[tuple[int, bool], None, None]:
        for number in self._numbers:
            yield number, self._crible[number] == P

    def __getitem__(self, n: int | slice):
        if isinstance(n, int):
            index: int = self._numbers[n] # real index
            return self._crible[index] == P
        elif isinstance(n, slice):
            r: range = self._numbers[n]
            s = slice(r.start, r.stop, r.step)
            return PrimeCribleSlice(self._crible, s)
        else:
            raise TypeError(f"Type {type(n).__name__} is not supported")
