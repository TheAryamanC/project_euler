"""
Project Euler - Problem 4: Largest Palindrome Product

A palindromic number reads the same both ways. The largest palindrome made from the product of two $2$-digit numbers is $9009 = 91 \times 99$. Find the largest palindrome made from the product of two $3$-digit numbers.
"""

def solution():
    def is_palindrome(n):
        return str(n) == str(n)[::-1]

    max_palindrome = 0
    for i in range(999, 99, -1):
        for j in range(i, 99, -1):
            product = i * j
            if product < max_palindrome:
                break
            if is_palindrome(product):
                max_palindrome = max(max_palindrome, product)
    return max_palindrome

if __name__ == "__main__":
    print(solution())  # Answer: 906609