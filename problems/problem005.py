"""
Project Euler - Problem 5: Smallest Multiple

2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder. What is the smallest positive number that is evenly divisible divisible with no remainder by all of the numbers from 1 to 20?
"""

import math

def solution():
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def lcm(a, b):
        return a * b // gcd(a, b)

    result = 1
    for i in range(1, 21):
        result = lcm(result, i)

    return result

if __name__ == "__main__":
    print(solution())  # Answer: 232792560