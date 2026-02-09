"""
Project Euler - Problem 62: Cubic Permutations

The cube, 41063625 (345³), can be permuted to produce two other cubes:
56623104 (384³) and 66430125 (405³). In fact, 41063625 is the smallest cube
which has exactly three permutations of its digits which are also cube.

Find the smallest cube for which exactly five permutations of its digits are cube.
"""

def solution():
    cubes = {}
    n = 1
    
    while True:
        cube = n ** 3
        key = ''.join(sorted(str(cube)))
        
        if key not in cubes:
            cubes[key] = []
        cubes[key].append(cube)
        
        if len(cubes[key]) == 5:
            return min(cubes[key])
        
        n += 1

if __name__ == "__main__":
    print(solution())  # Answer: 127035954683
