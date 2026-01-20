"""
Project Euler - Problem 36: Double-base Palindromes

The decimal number, 585 = 1001001001 (binary), is palindromic in both bases.

Find the sum of all numbers, less than one million, which are palindromic in
base 10 and base 2.

(Please note that the palindromic number, in either base, may not include
leading zeros.)
"""

def is_palindrome(s):
    return s == s[::-1]

def solution():
    total = 0
    for n in range(1, 1000000):
        decimal_str = str(n)
        binary_str = bin(n)[2:]  # Remove '0b' prefix
        if is_palindrome(decimal_str) and is_palindrome(binary_str):
            total += n
    return total

if __name__ == "__main__":
    print(solution())  # Answer: 872187