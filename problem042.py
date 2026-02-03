"""
Project Euler - Problem 42: Coded Triangle Numbers

The nth term of the sequence of triangle numbers is given by, t_n = n(n+1)/2;
so the first ten triangle numbers are: 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...

By converting each letter in a word to a number corresponding to its
alphabetical position and adding these values we form a word value. For
example, the word value for SKY is 19 + 11 + 25 = 55 = t_10. If the word value
is a triangle number then we shall call the word a triangle word.

Using words.txt, a 16K text file containing nearly two-thousand common English
words, how many are triangle words?
"""

def word_value(word):
    return sum(ord(c) - ord('A') + 1 for c in word)

def solution():
    with open('additional_files/words.txt', 'r') as f:
        words = f.read().replace('"', '').split(',')
    triangle_numbers = set(n * (n + 1) // 2 for n in range(1, 100))

    count = 0
    for word in words:
        if word_value(word) in triangle_numbers:
            count += 1
    
    return count

if __name__ == "__main__":
    print(solution())  # Answer: 162