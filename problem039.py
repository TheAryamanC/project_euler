"""
Project Euler - Problem 39: Integer Right Triangles

If p is the perimeter of a right angle triangle with integral length sides,
{a, b, c}, there are exactly three solutions for p = 120.

{20, 48, 52}, {24, 45, 51}, {30, 40, 50}

For which value of p <= 1000, is the number of solutions maximised?
"""

def solution():
    max_solutions = 0
    best_p = 0
    
    for p in range(12, 1001):
        solutions = 0
        for a in range(1, p // 3):
            for b in range(a, (p - a) // 2):
                c = p - a - b
                if a * a + b * b == c * c:
                    solutions += 1
        
        if solutions > max_solutions:
            max_solutions = solutions
            best_p = p
    
    return best_p

if __name__ == "__main__":
    print(solution())  # Answer: 840