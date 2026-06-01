from abc import ABC
from array import array
from collections.abc import Generator
from numbers import Real
from math import isqrt
from typing import runtime_checkable, Protocol

C = 67 # composite
P = 80 # prime
# both variables are ASCII code, it is useful to represent primes and composites in __str__ and __bytes__

@runtime_checkable
class SupportsPrime(Protocol):
    primes: int


class PrimeCribleBase(ABC):
    """
    Abstract base class for PrimeCrible and PrimeCribleSlice. Regroups dunders and methods that are common to both class.
    """
    _crible: array
    _n_primes: None | int
    _n_composites: None | int

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, (PrimeCribleSlice, PrimeCrible)):
            return NotImplemented
        else:
            return str(self) == str(other) # TODO: find a more robust identity

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

    @property
    def primes(self):
        return self._n_primes

    @property
    def composites(self):
        return self._n_composites


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

        self._sift()

        self._n_composites = self._crible.count(C)
        self._n_primes = self._crible.count(P)

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

    def __str__(self) -> str:
        """
        Return a string representing the crible, such as str[n] = "P" if n is prime and "C" if composite
        For instance, str(PrimeCrible(10)) returns 'CCPPCPCPCC'
        """
        return self._crible.tobytes().decode()

    def __bytes__(self) -> bytes:
        """
        Return a byte array representing the crible, such as bytes[n] = b'P' if n is prime and b'C' if composite.
        For instance, bytes(PrimeCrible(10)) return b'CCPPCPCPCC'
        """
        return self._crible.tobytes()

    def __bool__(self) -> bool:
        return len(self._crible) > 0

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


class PrimeCribleSlice(PrimeCribleBase):
    def __init__(self, crible: array, number_range: slice):
        self._crible = crible
        self._slice = slice(
            number_range.start if number_range.start is not None else 0,
            number_range.stop if number_range.stop is not None else len(self._crible),
            number_range.step if number_range.step is not None else 1
        ) # a completely defined slice is needed for later
        self._numbers: range = range(self._slice.start, self._slice.stop, self._slice.step)

        self._n_primes = self._crible[self._slice].count(P)
        self._n_composites = self._crible[self._slice].count(C)

    def __len__(self) -> int:
        return len(self._numbers)

    def __repr__(self):
        return f"PrimeCribleSlice[{self._slice.start}:{self._slice.stop}:{self._slice.step}]"

    def __str__(self):
        return self._crible[self._slice].tobytes().decode()

    def __bytes__(self) -> bytes:
        return self._crible[self._slice].tobytes()

    def __bool__(self):
        return len(self._crible[self._slice]) > 0

    def __iter__(self) -> Generator[tuple[int, bool], None, None]:
        for number in self._numbers:
            yield number, self._crible[number] == P

    def __getitem__(self, n: int | slice):
        if isinstance(n, int):
            index: int = self._numbers[n] # real index
            return self._crible[index] == P
        elif isinstance(n, slice):
            r: range = self._numbers[n] # using the slice on the range _numbers allows us to get the "real" slice
            s = slice(r.start, r.stop, r.step)
            return PrimeCribleSlice(self._crible, s)
        else:
            raise TypeError(f"Type {type(n).__name__} is not supported")

    @property
    def slice_(self):
        return self._slice
