from src.prime_numbers import PrimeSieve, is_prime

"""
File made to test all properties of PrimeSieve and PrimeSieveSlice.
# Properties of PrimeSieve(n) (noted pc):
    * pc.primes returns the number of primes from 0 to n-1 included (the first n integers).
    * pc.composites returns the number of composites from 0 to n-1 included.
    * pc.primes + pc.composites = n = len(pc).
    * pc[index] return the primality of index if index is a number, as a boolean: True if prime, False if composite.
    That is, pc[0] is False, pc[1] is False, pc[2] is True, pc[3] is True and pc[n + 1] raises IndexError
    * pc[index] will return a PrimeSieveSlice if index is a slice, unless slice can be regarded as slice(0, n, 1)
    (for instance, pc[:], pc[0:], pc[:n], pc[::1], etc) then pc will return itself, in such a way that `pc[:] is pc`
    * pc.__iter__ returns a number and its primality in a tuple for each number from 0 to n-1
    * str(pc) returns a string where every number is represented by either 'C' if composite or 'P' if prime.
    * bytes(pc) returns a bytes where every number if represented by either b'C' if composite or b'P' if prime.
    * bool(pc) returns True if the Sieve contains at least one number
    * repr(pc) returns "PrimeSieve(n={n})
    * pc == o will return either pc and o have the same sequence if o is a PrimeSieve or PrimeSieveSlice object or
    NotImplemented if o is of a different type
    * pc < o will compare its propriety `primes` with o, if o has one, and will return NotImplemented o has no attribute
    `primes`.
# Properties of PrimeSieveSlice (noted pcs = pc[s]):
    * pcs does not generate another array nor get a slice of one (the object "looks" at the sieve using s as a "lens").
    * pcs generates a range (noted r) using the slice, which contains every number "selected" by the slice s. It is
    assigned as such: r = range(s.start, s.stop, s.step).
    * pcs.slice_ returns a slice s1 with no None attributes, so technically s1 == s is False, but pc[s1] == pcs.
    * pcs.primes returns the number of primes from 0 to n-1 included, filtered using s.
    * pcs.composites returns the number of composites from 0 to n-1 included, filtered using s.
    * pcs.primes + pcs.composites = len(r) = len(pcs).
    * pcs[index] will return the primality of r[index] if index is an integer as a boolean,
    True meaning index is prime, False meaning index is composite.
    * pcs[index] will return a PrimeSieveSlice if index is a slice, which is a slice of the current slice. If the slice
    doesn't change the current slice, for instance pcs[:], pcs[index] will return itself: pcs[:] is pcs.
    * pcs.__iter__ will iterate in the same way as in PrimeSieve, but for numbers in r.
    * str(pcs) will act the same way as PrimeSieve, but on r, which means str(pc)[s] is str(pcs).
    * bytes(pcs) will act the same way as PrimeSieve, but on r, which means bytes(pc)[s] is bytes(pcs).
    * bool(pcs) will return True if the Sieve contains at least one number.
    * pcs == o will work the same way as PrimeSieve.
    * pcs < o will work the same way as PrimeSieve.
"""
if __name__ == '__main__':
    c = PrimeSieve(50)
    # ---
    # correctness test for a small n, to test all the sieve properties
    # ---
    primes_below_50 = list(p for p in range(50) if is_prime(p))
    assert len(primes_below_50) == c.primes
    assert c.primes + c.composites == 50
    assert len(c) == 50
    for n, p in c:
        print(f"{n}: {"prime" if p else "composite"}")
    print(f"Among the first 50 natural integers (from 0 to 49), {c.primes} are primes and {c.composites} are composites.")
    # ---
    # correctness test for PrimeSieveSlice
    # ---
    assert c[:] is c
    assert c[0:c.n:1] is c # same as line 15, just another way to put it
    # if the slice is 0 to n for PrimeSieve(n), then it should return itself
    primes_25_50 = list(p for p in primes_below_50 if p > 25)
    cs1 = c[25:] # PrimeSieveSlice from 25 included to 49
    assert cs1.slice_ == slice(25, 50, 1)
    assert len(primes_25_50) == cs1.primes
    assert cs1.primes + cs1.composites == 25
    print(f"Among numbers between 25 and 50, (from 25 to 49), {cs1.primes} are primes and {cs1.composites} are composites.")
    # ---
    # str() test for both PrimeSieve and PrimeSieveSlice, no test for bytes() because it works the same way as str()
    # ---
    cs2 = c[1::2] # PrimeSlice from 1 to 50, with a step of 2 (only odd numbers)
    cs3 = c[3::10] # PrimeSlice from 3 to 50 with a step of 10: 3, 13, 23, 33, 43
    print(cs1 < cs2)
    print(str(c))
    # dots where the number isn't in the PrimeSieveSlice
    print("." * 25 + str(cs1))
    print("." + ".".join(str(cs2)))
    print("." * 3 + ("." * 9).join(str(cs3)) + "." * 6)

    print("Test passed successfully!")
