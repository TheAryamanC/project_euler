"""
Project Euler - Problem 52: Permuted Multiples

It can be seen that the number, 125874, and its double, 251748, contain exactly
the same digits, but in a different order.

Find the smallest positive integer, x, such that 2x, 3x, 4x, 5x, and 6x,
contain the same digits.
"""

def solution():
    x = 1
    while True:
        digits = sorted(str(x))
        if all(sorted(str(x * m)) == digits for m in range(2, 7)):
            return x
        x += 1

if __name__ == "__main__":
    print(solution())  # Answer: 142857
