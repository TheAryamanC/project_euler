"""
Project Euler - Problem 33: Digit Cancelling Fractions

The fraction 49/98 is a curious fraction, as an inexperienced mathematician
in attempting to simplify it may incorrectly believe that 49/98 = 4/8,
which is correct, is obtained by cancelling the 9s.

We shall consider fractions like, 30/50 = 3/5, to be trivial examples.

There are exactly four non-trivial examples of this type of fraction, less
than one in value, and containing two digits in the numerator and denominator.

If the product of these four fractions is given in its lowest common terms,
find the value of the denominator.
"""

from math import gcd

def solution():
    num_product = 1
    den_product = 1
    
    for numerator in range(10, 100):
        for denominator in range(numerator + 1, 100):
            n1, n2 = numerator // 10, numerator % 10
            d1, d2 = denominator // 10, denominator % 10
            
            if n2 == 0 and d2 == 0:
                continue
            
            if n2 == d1 and d2 != 0:
                if numerator * d2 == denominator * n1:
                    num_product *= numerator
                    den_product *= denominator
            
            if n2 == d2 and d1 != 0:
                if numerator * d1 == denominator * n1:
                    num_product *= numerator
                    den_product *= denominator
            
            if n1 == d1 and d2 != 0:
                if numerator * d2 == denominator * n2:
                    num_product *= numerator
                    den_product *= denominator
            
            if n1 == d2 and d1 != 0:
                if numerator * d1 == denominator * n2:
                    num_product *= numerator
                    den_product *= denominator
    
    return den_product // gcd(num_product, den_product)

if __name__ == "__main__":
    print(solution())  # Answer: 100