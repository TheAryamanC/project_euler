"""
Project Euler - Problem 34: Digit Factorials

145 is a curious number, as 1! + 4! + 5! = 1 + 24 + 120 = 145.

Find the sum of all numbers which are equal to the sum of the factorial of
their digits.

Note: As 1! = 1 and 2! = 2 are not sums they are not included.
"""

from math import factorial

def solution():
    factorials = [factorial(d) for d in range(10)]
    
    total = 0
    for n in range(10, 7 * factorials[9] + 1):
        digit_factorial_sum = sum(factorials[int(d)] for d in str(n))
        if digit_factorial_sum == n:
            total += n
    
    return total

if __name__ == "__main__":
    print(solution())  # Answer: 40730