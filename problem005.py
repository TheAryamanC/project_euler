"""
Project Euler - Problem 5: Smallest Multiple

2520 is the smallest number that can be divided by each of the numbers from 1 to 10
without any remainder.

What is the smallest positive number that is evenly divisible by all of the numbers
from 1 to 20?
"""

from math import lcm

def solution():
    return lcm(*range(1, 21))

if __name__ == "__main__":
    print(solution())  # Answer: 232792560