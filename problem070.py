"""
Project Euler Problem 70: Totient Permutation

Euler's totient function, φ(n) [sometimes called the phi function], is used to 
determine the number of positive numbers less than or equal to n which are 
relatively prime to n. For example, as 1, 2, 4, 5, 7, and 8, are all less than 
nine and relatively prime to nine, φ(9) = 6.

The number 1 is considered to be relatively prime to every positive number, 
so φ(1) = 1.

Interestingly, φ(87109) = 79180, and it can be seen that 87109 is a permutation 
of 79180.

Find the value of n, 1 < n < 10^7, for which φ(n) is a permutation of n and 
the ratio n/φ(n) produces a minimum.
"""

from sympy import primerange

# Modified permutation for speed
def is_permutation(a, b):
    sa = str(a)
    sb = str(b)
    if len(sa) != len(sb):
        return False
    counts = [0] * 10
    for ch in sa:
        counts[ord(ch) - 48] += 1
    for ch in sb:
        counts[ord(ch) - 48] -= 1
    for c in counts:
        if c:
            return False
    return True

def solution():
    limit = 10**7
    primes = list(primerange(2, limit))
    sqrt_limit = int(limit**0.5) + 1
    
    min_ratio = float('inf')
    result = 0
    
    for i, p in enumerate(primes):
        if p > sqrt_limit:
            break
        for q in primes[i:]:
            n = p * q
            if n >= limit:
                break
            
            phi = (p - 1) * (q - 1)
            
            if is_permutation(n, phi):
                ratio = n / phi
                if ratio < min_ratio:
                    min_ratio = ratio
                    result = n
    
    return result

if __name__ == "__main__":
    print(solution())  # Answer: 8319823
