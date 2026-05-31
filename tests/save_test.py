from src.prime_numbers import prime_generator, __primes, __unordered_primes # don't do that kids

print(__primes)
print(__unordered_primes)
g = prime_generator()
for p in g:
    if p > 500:
        break

print("Final List :", __primes)
print("Final set :", __unordered_primes)
