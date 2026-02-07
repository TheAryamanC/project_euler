"""
Project Euler - Problem 51: Prime Digit Replacements

By replacing the 1st digit of the 2-digit number *3, it turns out that six of
the nine possible values: 13, 23, 43, 53, 73, and 83, are all prime.

By replacing the 3rd and 4th digits of 56**3 with the same digit, this 5-digit
number is the first example having seven primes among the ten generated numbers,
yielding the family: 56003, 56113, 56333, 56443, 56663, 56773, and 56993.

Find the smallest prime which, by replacing part of the number (not necessarily
adjacent digits) with the same digit, is part of an eight prime value family.
"""

from itertools import combinations
from sympy import primerange

def solution():
    limit = 1000000
    is_prime = set(primerange(0, limit))
    
    for n in sorted(is_prime):
        s = str(n)
        length = len(s)
        
        for r in range(1, length):
            for indices in combinations(range(length), r):
                family = []
                
                for digit in '0123456789':
                    candidate = list(s)
                    for index in indices:
                        candidate[index] = digit
                    candidate_num = int(''.join(candidate))
                    
                    if candidate_num >= 10**(length-1) and candidate_num in is_prime:
                        family.append(candidate_num)
                
                if len(family) == 8:
                    return min(family)

if __name__ == "__main__":
    print(solution())  # Answer: 121313