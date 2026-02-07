"""
Project Euler - Problem 60: Prime Pair Sets

The primes 3, 7, 109, and 673, are quite remarkable. By taking any two primes
and concatenating them in any order the result will always be prime. For
example, taking 7 and 109, both 7109 and 1097 are prime. The sum of these four
primes, 792, represents the lowest sum for a set of four primes with this
property.

Find the lowest sum for a set of five primes for which any two primes
concatenate to produce another prime.
"""

from sympy import isprime, primerange

def concat_prime(a, b):
    return isprime(int(str(a) + str(b))) and isprime(int(str(b) + str(a)))

def solution():
    limit = 10000
    primes = list(primerange(2, limit))
    
    compatible = {}
    for i, p in enumerate(primes):
        compatible[p] = []
        for q in primes[i+1:]:
            if concat_prime(p, q):
                compatible[p].append(q)
    
    for i, a in enumerate(primes):
        for b in compatible[a]:
            if b not in compatible:
                continue
            for c in compatible[b]:
                if c <= b or c not in compatible[a]:
                    continue
                for d in compatible[c]:
                    if d <= c or d not in compatible[a] or d not in compatible[b]:
                        continue
                    for e in compatible[d]:
                        if e <= d or e not in compatible[a] or e not in compatible[b] or e not in compatible[c]:
                            continue
                        return a + b + c + d + e
    return None

if __name__ == "__main__":
    print(solution())  # Answer: 26033
