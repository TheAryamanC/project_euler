"""
Project Euler - Problem 10: Summation of Primes

The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.

Find the sum of all the primes below two million.
"""

from sympy import primerange

def solution():
    return sum(list(primerange(2, 2000000)))

if __name__ == "__main__":
    print(solution())  # Answer: 142913828922