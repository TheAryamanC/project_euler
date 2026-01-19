"""
Project Euler - Problem 17: Number Letter Counts

If the numbers 1 to 5 are written out in words: one, two, three, four, five,
then there are 3 + 3 + 5 + 4 + 4 = 19 letters used in total.

If all the numbers from 1 to 1000 (one thousand) inclusive were written out
in words, how many letters would be used?

NOTE: Do not count spaces or hyphens. For example, 342 (three hundred and forty-two)
contains 23 letters and 115 (one hundred and fifteen) contains 20 letters.
The use of "and" when writing out numbers is in compliance with British usage.
"""

def solution():
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
            "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
            "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    
    def number_to_words(n):
        if n == 1000:
            return "onethousand"
        if n >= 100:
            result = ones[n // 100] + "hundred"
            if n % 100 != 0:
                result += "and" + number_to_words(n % 100)
            return result
        if n >= 20:
            return tens[n // 10] + ones[n % 10]
        return ones[n]
    
    total = sum(len(number_to_words(i)) for i in range(1, 1001))
    return total

if __name__ == "__main__":
    print(solution())  # Answer: 21124