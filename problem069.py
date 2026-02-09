"""
Project Euler Problem 69: Totient Maximum

Euler's totient function, φ(n) [sometimes called the phi function], is defined 
as the number of positive integers not exceeding n which are relatively prime to n. 
For example, as 1, 2, 4, 5, 7, and 8, are all less than or equal to nine and 
relatively prime to nine, φ(9) = 6.

n    Relatively Prime    φ(n)    n/φ(n)
2    1                   1       2
3    1,2                 2       1.5
4    1,3                 2       2
5    1,2,3,4             4       1.25
6    1,5                 2       3
7    1,2,3,4,5,6         6       1.1666...
8    1,3,5,7             4       2
9    1,2,4,5,7,8         6       1.5
10   1,3,7,9             4       2.5

It can be seen that n=6 produces a maximum n/φ(n) for n ≤ 10.

Find the value of n <= 1,000,000 for which n/φ(n) is a maximum.
"""

from sympy import primerange

def solution():
    limit = 1000000
    prod = 1
    primes = list(primerange(2, limit))
    p = 2
    # generate primes incrementally and multiply until product would exceed limit
    while True:
        isprime = True
        for q in primes:
            if q * q > p:
                break
            if p % q == 0:
                isprime = False
                break
        if isprime:
            if prod * p > limit:
                break
            prod *= p
            primes.append(p)
        p += 1
    return prod

if __name__ == "__main__":
    print(solution())  # Answer: 510510
