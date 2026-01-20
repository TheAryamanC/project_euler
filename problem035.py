"""
Project Euler - Problem 35: Circular Primes

The number, 197, is called a circular prime because all rotations of the
digits: 197, 971, and 719, are themselves prime.

There are thirteen such primes below 100:
2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, and 97.

How many circular primes are there below one million?
"""

from sympy import isprime

def get_rotations(n):
    s = str(n)
    rotations = []
    for i in range(len(s)):
        rotations.append(int(s[i:] + s[:i]))
    return rotations

def solution():
    limit = 1000000
    
    count = 0
    for n in range(2, limit):
        if isprime(n):
            rotations = get_rotations(n)
            if all(r < limit and isprime(r) for r in rotations):
                count += 1
    
    return count

if __name__ == "__main__":
    print(solution())  # Answer: 55