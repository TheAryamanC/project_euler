"""
Project Euler - Problem 46: Goldbach's Other Conjecture

It was proposed by Christian Goldbach that every odd composite number can be
written as the sum of a prime and twice a square.

9 = 7 + 2*1²
15 = 7 + 2*2²
21 = 3 + 2*3²
25 = 7 + 2*3²
27 = 19 + 2*2²
33 = 31 + 2*1²
It turns out that the conjecture was false.

What is the smallest odd composite that cannot be written as the sum of a prime
and twice a square?
"""

from sympy import isprime

def can_be_written_as_sum(n):
    i = 1
    while 2 * i * i < n:
        remainder = n - 2 * i * i
        if isprime(remainder):
            return True
        i += 1
    return False

def solution():
    n = 9  # Start with first odd composite
    
    while True:
        if not isprime(n) and not can_be_written_as_sum(n):
            return n
        n += 2

if __name__ == "__main__":
    print(solution())  # Answer: 5777