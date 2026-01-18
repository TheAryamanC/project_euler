"""
Project Euler - Problem 9: Special Pythagorean Triplet

A Pythagorean triplet is a set of three natural numbers, a < b < c, for which,
a² + b² = c²

For example, 3² + 4² = 9 + 16 = 25 = 5².

There exists exactly one Pythagorean triplet for which a + b + c = 1000.
Find the product abc.
"""

def solution():
    for a in range(1, 333):
        for b in range(a + 1, 500):
            c = 1000 - a - b
            if c > b and a * a + b * b == c * c:
                return a * b * c
    return None

if __name__ == "__main__":
    print(solution())  # Answer: 31875000