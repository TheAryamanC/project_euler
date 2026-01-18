"""
Project Euler - Problem 15: Lattice Paths

Starting in the top left corner of a 2*2 grid, and only being able to move to
the right and down, there are exactly 6 routes to the bottom right corner.

How many such routes are there through a 20*20 grid?
"""

from math import comb

def solution():
    grid_size = 20
    return comb(2 * grid_size, grid_size)

if __name__ == "__main__":
    print(solution())  # Answer: 137846528820