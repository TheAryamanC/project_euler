"""
Project Euler - Problem 3: Largest Prime Factor

The prime factors of 13195 are 5, 7, 13 and 29.

What is the largest prime factor of the number 600851475143?
"""

from sympy.ntheory import factorint

def solution():
    n = 600851475143
    factors = factorint(n)
    return max(factors.keys())

if __name__ == "__main__":
    print(solution())  # Answer: 6857