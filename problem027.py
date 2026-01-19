"""
Project Euler - Problem 27: Quadratic Primes

Euler discovered the remarkable quadratic formula: n**2 + n + 41

It turns out that the formula will produce 40 primes for the consecutive integer
values 0 <= n <= 39.

The incredible formula n**2 - 79n + 1601 was discovered, which produces 80 primes
for the consecutive values 0 <= n <= 79. The product of the coefficients, -79 and
1601, is -126479.

Considering quadratics of the form: n**2 + an + b, where |a| < 1000 and |b| ≤ 1000
Find the product of the coefficients, a and b, for the quadratic expression
that produces the maximum number of primes for consecutive values of n,
starting with n = 0.
"""

from sympy import isprime

def count_consecutive_primes(a, b):
    n = 0
    while isprime(abs(n*n + a*n + b)):
        n += 1
    return n

def solution():
    max_primes = 0
    best_product = 0
    
    for a in range(-999, 1000):
        for b in range(-1000, 1001):
            count = count_consecutive_primes(a, b)
            if count > max_primes:
                max_primes = count
                best_product = a * b
    
    return best_product

if __name__ == "__main__":
    print(solution())  # Answer: -59231