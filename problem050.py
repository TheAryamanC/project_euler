"""
Project Euler - Problem 50: Consecutive Prime Sum

The prime 41, can be written as the sum of six consecutive primes:
41 = 2 + 3 + 5 + 7 + 11 + 13

This is the longest sum of consecutive primes that adds to a prime below
one-hundred.

The longest sum of consecutive primes below one-thousand that adds to a prime,
contains 21 terms, and is equal to 953.

Which prime, below one-million, can be written as the sum of the most
consecutive primes?
"""

from sympy import primerange

def solution():
    limit = 1000000
    primes = list(primerange(1, limit))
    
    cumsum = [0]
    for p in primes:
        cumsum.append(cumsum[-1] + p)
        if cumsum[-1] > limit:
            break
    
    max_length = 0
    result = 0
    
    for i in range(len(cumsum)):
        for j in range(i + max_length + 1, len(cumsum)):
            s = cumsum[j] - cumsum[i]
            if s >= limit:
                break
            if s in primes and j - i > max_length:
                max_length = j - i
                result = s
    
    return result

if __name__ == "__main__":
    print(solution())  # Answer: 997651