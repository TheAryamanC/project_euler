"""
Project Euler - Problem 32: Pandigital Products

We shall say that an n-digit number is pandigital if it makes use of all the
digits 1 to n exactly once; for example, the 5-digit number, 15234, is 1
through 5 pandigital.

The product 7254 is unusual, as the identity, 39 × 186 = 7254, containing
multiplicand, multiplier, and product is 1 through 9 pandigital.

Find the sum of all products whose multiplicand/multiplier/product identity
can be written as a 1 through 9 pandigital.

HINT: Some products can be obtained in more than one way so be sure to only
include it once in your sum.
"""

def is_pandigital(a, b, c):
    s = str(a) + str(b) + str(c)
    return len(s) == 9 and set(s) == set('123456789')

def solution():
    products = set()
    
    # a is 1-digit, b is 4-digit
    for a in range(1, 10):
        for b in range(1000, 10000):
            c = a * b
            if is_pandigital(a, b, c):
                products.add(c)
    
    # a is 2-digit, b is 3-digit
    for a in range(10, 100):
        for b in range(100, 1000):
            c = a * b
            if is_pandigital(a, b, c):
                products.add(c)
    
    return sum(products)

if __name__ == "__main__":
    print(solution())  # Answer: 45228