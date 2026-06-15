from src.prime_numbers import prime_generator, __primes, __unordered_primes # don't do that kids

print(__primes)
print(__unordered_primes)
g = prime_generator(100)
for p in g:
    pass

print("Final List :", __primes, f"\n{len(__primes)} elements")
print("Final set :", __unordered_primes)
