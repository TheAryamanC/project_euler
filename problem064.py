"""
Project Euler - Problem 64: Odd Period Square Roots

All square roots are periodic when written as continued fractions.
sqrt(N) = a_0 + 1/(a_1 + 1/(a_2 + 1/(a_3 + ...)))
For conciseness, we use the notation sqrt(N) = [a_0; (a_1, a_2, a_3, ...)] to indicate that the block (a_1, a_2, a_3, ...) repeats indefinitely.

For example: sqrt(23) = [4; (1,3,1,8)] where (1,3,1,8) repeats indefinitely.

Exactly four continued fractions, for N <= 13, have an odd period.

How many continued fractions for N <= 10000 have an odd period?
"""

import math

def get_continued_fraction_period(n):
    sqrt_n = int(math.sqrt(n))
    if sqrt_n * sqrt_n == n:
        return 0
    
    m, d, a = 0, 1, sqrt_n
    seen = {}
    period = 0
    
    while True:
        m = d * a - m
        d = (n - m * m) // d
        a = (sqrt_n + m) // d
        
        state = (m, d)
        if state in seen:
            return period
        seen[state] = period
        period += 1

def solution():
    count = 0
    for n in range(2, 10001):
        period = get_continued_fraction_period(n)
        if period % 2 == 1:
            count += 1
    return count

if __name__ == "__main__":
    print(solution())  # Answer: 1322
