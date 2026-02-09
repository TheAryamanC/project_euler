"""
Project Euler - Problem 63: Powerful Digit Counts

The 5-digit number, 16807 = 7^5, is also a fifth power.
Similarly, the 9-digit number, 134217728 = 8^9, is a ninth power.

How many n-digit positive integers exist which are also an nth power?
"""

def solution():
    count = 0
    for base in range(1, 10):
        power = 1
        while len(str(base ** power)) == power:
            count += 1
            power += 1
    return count

if __name__ == "__main__":
    print(solution())  # Answer: 49
