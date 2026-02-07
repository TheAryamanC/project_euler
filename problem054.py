"""
Project Euler - Problem 54: Poker Hands

In the card game poker, a hand consists of five cards and are ranked, from
lowest to highest, in the following way:

• High Card: Highest value card.
• One Pair: Two cards of the same value.
• Two Pairs: Two different pairs.
• Three of a Kind: Three cards of the same value.
• Straight: All cards are consecutive values.
• Flush: All cards of the same suit.
• Full House: Three of a kind and a pair.
• Four of a Kind: Four cards of the same value.
• Straight Flush: All cards are consecutive values of same suit.
• Royal Flush: Ten, Jack, Queen, King, Ace, in same suit.

The cards are valued in the order:
2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, Ace.

If two players have the same ranked hands then the rank made up of the highest value wins; for example, a pair of eights beats a pair of fives (see example 1 below). But if two ranks tie, for example, both players have a pair of queens, then highest cards in each hand are compared (see example 4 below); if the highest cards tie then the next highest cards are compared, and so on.

Consider the following five hands dealt to two players:

Hand	 	Player 1	 	Player 2	 	Winner
1	 	5H 5C 6S 7S KD   2C 3S 8S 8D TD
                                           Player 2
        Pair of Fives    Pair of Eights
	 	
2	 	5D 8C 9S JS AC   2C 5C 7D 8S QH
                                           Player 1
       Highest card Ace Highest card Queen

3	 	2D 9C AS AH AC   3D 6D 7D TD QD
                                           Player 2
          Three Aces   Flush with Diamonds

4	 	4D 6S 9H QH QC   3D 6D 7H QD QS
        Pair of Queens   Pair of Queens    Player 1
      Highest card Nine Highest card Seven

5	 	2H 2D 4C 4D 4S   3C 3D 3S 9S 9D
          Full House       Full House      Player 1
       With Three Fours With Three Threes

The file, poker.txt, contains one-thousand random hands dealt to two players. Each line of the file contains ten cards (separated by a single space): the first five are Player 1's cards and the last five are Player 2's cards. You can assume that all hands are valid (no invalid characters or repeated cards), each player's hand is in no specific order, and in each hand there is a clear winner.

How many hands does Player 1 win?
"""

def card_value(card):
    values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
              '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    return values[card[0]]

def hand_rank(hand):
    values = sorted([card_value(c) for c in hand], reverse=True)
    suits = [c[1] for c in hand]
    
    is_flush = len(set(suits)) == 1
    is_straight = (max(values) - min(values) == 4 and len(set(values)) == 5) or values == [14, 5, 4, 3, 2]  # Ace-low straight
    
    if values == [14, 5, 4, 3, 2]:
        values = [5, 4, 3, 2, 1]
    
    value_counts = {}
    for v in values:
        value_counts[v] = value_counts.get(v, 0) + 1
    
    counts = sorted(value_counts.values(), reverse=True)
    
    if is_straight and is_flush:
        return (8, values)
    if counts == [4, 1]:
        return (7, sorted(values, key=lambda x: (value_counts[x], x), reverse=True))
    if counts == [3, 2]:
        return (6, sorted(values, key=lambda x: (value_counts[x], x), reverse=True))
    if is_flush:
        return (5, values)
    if is_straight:
        return (4, values)
    if counts == [3, 1, 1]:
        return (3, sorted(values, key=lambda x: (value_counts[x], x), reverse=True))
    if counts == [2, 2, 1]:
        return (2, sorted(values, key=lambda x: (value_counts[x], x), reverse=True))
    if counts == [2, 1, 1, 1]:
        return (1, sorted(values, key=lambda x: (value_counts[x], x), reverse=True))
    return (0, values)

def solution():
    with open('additional_files/poker.txt', 'r') as f:
        games = f.readlines()
    
    player1_wins = 0
    for game in games:
        cards = game.strip().split()
        hand1 = cards[:5]
        hand2 = cards[5:]
        if hand_rank(hand1) > hand_rank(hand2):
            player1_wins += 1
    
    return player1_wins

if __name__ == "__main__":
    print(solution())  # Answer: 376
