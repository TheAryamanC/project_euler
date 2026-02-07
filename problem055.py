"""
Project Euler - Problem 55: Lychrel Numbers

If we take 47, reverse and add, 47 + 74 = 121, which is palindromic.

Not all numbers produce palindromes so quickly. For example,
349 + 943 = 1292
1292 + 2921 = 4213
4213 + 3124 = 7337

That is, 349 took three iterations to arrive at a palindrome.

A number that never forms a palindrome through the reverse and add process is
called a Lychrel number. For the purpose of this problem, we shall assume that
a number is Lychrel until proven otherwise.

How many Lychrel numbers are there below ten-thousand?

NOTE: It will either become a palindrome in less than fifty iterations, or no
one has managed so far to map it to a palindrome.
"""

def is_palindrome(n):
    s = str(n)
    return s == s[::-1]

def is_lychrel(n, max_iterations=50):
    for _ in range(max_iterations):
        n = n + int(str(n)[::-1])
        if is_palindrome(n):
            return False
    return True

def solution():
    return sum(1 for n in range(1, 10000) if is_lychrel(n))

if __name__ == "__main__":
    print(solution())  # Answer: 249
