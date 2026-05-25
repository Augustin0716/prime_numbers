from src.prime_numbers import PrimeCrible,  is_prime

if __name__ == '__main__':
    c = PrimeCrible(50)
    # ---
    # correctness test for a small n, to test all the crible properties
    # ---
    primes_below_50 = list(p for p in range(50) if is_prime(p))
    assert len(primes_below_50) == c.primes
    assert c.primes + c.composites == 50
    print(f"Among the first 50 natural integers (from 0 to 49), {c.primes} are primes and {c.composites} are composites.")
    # ---
    # correctness test for PrimeCribleSlice
    # ---
    assert c[:] is c
    assert c[0:c.n:1] is c
    primes_25_50 = list(p for p in primes_below_50 if p > 25)
    cs1 = c[25:]
    assert len(primes_25_50) == cs1.primes
    assert cs1.primes + cs1.composites == 25
    print(f"Among numbers between 25 and 50, (from 25 to 49), {cs1.primes} are primes and {cs1.composites} are composites.")
    # ---
    # str() test for both PrimeCrible and PrimeCribleSlice
    # ---
    cs2 = c[1::2] # PrimeSlice from 1 to 50, with a step of 2
    print(str(c))
    print("." * 25 + str(cs1))
    print("." + ".".join(str(cs2)))

    print("Test passed successfully!")
