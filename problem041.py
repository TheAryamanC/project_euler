"""
Project Euler - Problem 41: Pandigital Prime

We shall say that an n-digit number is pandigital if it makes use of all the
digits 1 to n exactly once. For example, 2143 is a 4-digit pandigital and is
also prime.

What is the largest n-digit pandigital prime that exists?
"""

from itertools import permutations
from sympy import isprime

def solution():
    for n in range(9, 0, -1):
        digits = ''.join(str(i) for i in range(n, 0, -1))
        for perm in permutations(digits):
            num = int(''.join(perm))
            if isprime(num):
                return num
    return None

if __name__ == "__main__":
    print(solution())  # Answer: 7652413