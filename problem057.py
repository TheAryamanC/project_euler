"""
Project Euler - Problem 57: Square Root Convergents

It is possible to show that the square root of two can be expressed as an
infinite continued fraction: sqrt(2) = 1 + 1/(2 + 1/(2 + 1/(2 + ...)))

By expanding this for the first four iterations, we get:
1 + 1/2 = 3/2 = 1.5
1 + 1/(2 + 1/2) = 7/5 = 1.4
1 + 1/(2 + 1/(2 + 1/2)) = 17/12 = 1.41666...
1 + 1/(2 + 1/(2 + 1/(2 + 1/2))) = 41/29 = 1.41379...

The eighth expansion, 1393/985, is the first example where the number of digits
in the numerator exceeds the number of digits in the denominator.

In the first one-thousand expansions, how many fractions contain a numerator
with more digits than the denominator?
"""

def solution():
    count = 0
    numerator = 3
    denominator = 2
    
    for _ in range(1000):
        if len(str(numerator)) > len(str(denominator)):
            count += 1
        numerator, denominator = numerator + 2 * denominator, numerator + denominator
    
    return count

if __name__ == "__main__":
    print(solution())  # Answer: 153
