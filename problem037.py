"""
Project Euler - Problem 37: Truncatable Primes

The number 3797 has an interesting property. Being prime itself, it is
possible to continuously remove digits from left to right, and remain prime
at each stage: 3797, 797, 97, and 7.
Similarly we can work from right to left: 3797, 379, 37, and 3.

Find the sum of the only eleven primes that are both truncatable from left
to right and right to left.

NOTE: 2, 3, 5, and 7 are not considered to be truncatable primes.
"""

from sympy import isprime

def is_truncatable_prime(n):
    s = str(n)
    for i in range(len(s)):
        if not isprime(int(s[i:])):
            return False
    for i in range(1, len(s) + 1):
        if not isprime(int(s[:i])):
            return False
    return True

def solution():
    truncatable_primes = []
    n = 11
    
    while len(truncatable_primes) < 11:
        if is_truncatable_prime(n):
            truncatable_primes.append(n)
        n += 2
    
    return sum(truncatable_primes)

if __name__ == "__main__":
    print(solution())  # Answer: 748317