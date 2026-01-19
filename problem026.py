"""
Project Euler - Problem 26: Reciprocal Cycles

A unit fraction contains 1 in the numerator. The decimal representation of the
unit fractions with denominators 2 to 10 are given:

1/2 = 0.5
1/3 = 0.(3)
1/4 = 0.25
1/5 = 0.2
1/6 = 0.1(6)
1/7 = 0.(142857)
1/8 = 0.125
1/9 = 0.(1)
1/10 = 0.1

Where 0.1(6) means 0.166666..., and has a 1-digit recurring cycle.
It can be seen that 1/7 has a 6-digit recurring cycle.

Find the value of d < 1000 for which 1/d contains the longest recurring cycle
in its decimal fraction part.
"""

def get_cycle_length(d):
    remainders = {}
    remainder = 1
    position = 0
    
    while remainder != 0:
        if remainder in remainders:
            return position - remainders[remainder]
        remainders[remainder] = position
        remainder = (remainder * 10) % d
        position += 1
    
    return 0

def solution():
    max_length = 0
    max_d = 0
    
    for d in range(2, 1000):
        cycle_length = get_cycle_length(d)
        if cycle_length > max_length:
            max_length = cycle_length
            max_d = d
    
    return max_d

if __name__ == "__main__":
    print(solution())  # Answer: 983