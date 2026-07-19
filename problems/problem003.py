"""
Project Euler - Problem 3: Largest Prime Factor

The prime factors of $13195$ are $5, 7, 13$ and $29$. What is the largest prime factor of the number $600851475143$?
"""

def solution():
    def largest_prime_factor(n):
        i = 2
        while i * i <= n:
            if n % i:
                i += 1
            else:
                n //= i
        return n

    return largest_prime_factor(600851475143)

if __name__ == "__main__":
    print(solution())  # Answer: 6857