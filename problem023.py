"""
Project Euler - Problem 23: Non-Abundant Sums

A perfect number is a number for which the sum of its proper divisors is exactly
equal to the number. For example, the sum of the proper divisors of 28 would be
1 + 2 + 4 + 7 + 14 = 28, which means that 28 is a perfect number.

A number n is called deficient if the sum of its proper divisors is less than n
and it is called abundant if this sum exceeds n.

As 12 is the smallest abundant number, 1 + 2 + 3 + 4 + 6 = 16, the smallest
number that can be written as the sum of two abundant numbers is 24.

By mathematical analysis, it can be shown that all integers greater than 28123
can be written as the sum of two abundant numbers.

Find the sum of all the positive integers which cannot be written as the sum of
two abundant numbers.
"""

from sympy import divisors

def solution():
    limit = 28123
    
    abundant = [i for i in range(12, limit + 1) if sum(divisors(i)) > 2 * i]
    
    can_be_sum = set()
    for a in abundant:
        for b in abundant:
            if a + b > limit:
                break
            can_be_sum.add(a + b)
    
    return sum(i for i in range(1, limit + 1) if i not in can_be_sum)

if __name__ == "__main__":
    print(solution())  # Answer: 4179871