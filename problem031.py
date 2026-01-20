"""
Project Euler - Problem 31: Coin Sums

In the United Kingdom the currency is made up of pound (£) and pence (p).
There are eight coins in general circulation:
1p, 2p, 5p, 10p, 20p, 50p, £1 (100p), and £2 (200p).

It is possible to make £2 in the following way:
1*£1 + 1*50p + 2*20p + 1*5p + 1*2p + 3*1p

How many different DP can £2 be made using any number of coins?
"""

def solution():
    coins = [1, 2, 5, 10, 20, 50, 100, 200]
    target = 200
    
    DP = [0] * (target + 1)
    DP[0] = 1
    
    for coin in coins:
        for i in range(coin, target + 1):
            DP[i] += DP[i - coin]
    
    return DP[target]

if __name__ == "__main__":
    print(solution())  # Answer: 73682