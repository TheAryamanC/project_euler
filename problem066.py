"""
Project Euler Problem 66: Diophantine Equation

Consider quadratic Diophantine equations of the form:
x² - D*y² = 1

For example, when D=13, the minimal solution in x is 649² - 13*180² = 1.

It can be assumed that there are no solutions in positive integers when D is square.

By finding minimal solutions in x for D = {2, 3, 5, 6, 7}, we obtain the following:
3² - 2*2² = 1
2² - 3*1² = 1
9² - 5*4² = 1
5² - 6*2² = 1
8² - 7*3² = 1

Hence, by considering minimal solutions in x for D <= 7, the largest x is obtained when D=5.

Find the value of D <= 1000 in minimal solutions of x for which the largest value of x is obtained.
"""

import math

def solve_diophantine(D):
    sqrt_D = int(math.isqrt(D))
    if sqrt_D * sqrt_D == D:
        return None
    
    m, d, a = 0, 1, sqrt_D
    a0 = a
    
    p_prev, p_curr = 1, a0
    q_prev, q_curr = 0, 1
    
    while True:
        m = d * a - m
        d = (D - m * m) // d
        a = (a0 + m) // d
        
        p_prev, p_curr = p_curr, a * p_curr + p_prev
        q_prev, q_curr = q_curr, a * q_curr + q_prev
        
        if p_curr * p_curr - D * q_curr * q_curr == 1:
            return p_curr

def solution():
    max_x = 0
    result = 0
    
    for D in range(2, 1001):
        x = solve_diophantine(D)
        if x is not None and x > max_x:
            max_x = x
            result = D
    
    return result

if __name__ == "__main__":
    print(solution())  # Answer: 661
