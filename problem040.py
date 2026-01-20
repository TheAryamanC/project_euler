"""
Project Euler - Problem 40: Champernowne's Constant

An irrational decimal fraction is created by concatenating the positive integers:

0.123456789101112131415161718192021...

It can be seen that the 12th digit of the fractional part is 1.

If d_n represents the nth digit of the fractional part, find the value of the
following expression:

d_1 * d_10 * d_100 * d_1000 * d_10000 * d_100000 * d_1000000
"""

def solution():
    champernowne = ""
    n = 1
    while len(champernowne) < 1000001:
        champernowne += str(n)
        n += 1
    
    result = 1
    for power in range(7):
        position = 10 ** power
        result *= int(champernowne[position - 1])
    
    return result

if __name__ == "__main__":
    print(solution())  # Answer: 210