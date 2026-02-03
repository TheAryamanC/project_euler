"""
Project Euler - Problem 49: Prime Permutations

The arithmetic sequence, 1487, 4817, 8147, in which each of the terms increases
by 3330, is unusual in two ways: (i) each of the three terms are prime, and,
(ii) each of the 4-digit numbers are permutations of one another.

There are no arithmetic sequences made up of three 1-, 2-, or 3-digit primes,
exhibiting this property, but there is one other 4-digit increasing sequence.

What 12-digit number do you form by concatenating the three terms in this
sequence?
"""

from sympy import primerange

def solution():
    prime = set(primerange(1000,10000))
    
    for n in range(1000, 10000):
        if n not in prime:
            continue
        
        if n == 1487:
            continue
        
        for step in range(1, (10000 - n) // 2):
            n2 = n + step
            n3 = n + 2 * step
            
            if n3 >= 10000:
                break
            
            if n2 in prime and n3 in prime:
                if sorted(str(n)) == sorted(str(n2)) == sorted(str(n3)):
                    return str(n) + str(n2) + str(n3)
    
    return None

if __name__ == "__main__":
    print(solution())  # Answer: 296962999629