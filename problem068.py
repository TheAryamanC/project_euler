"""
Project Euler Problem 68: Magic 5-gon Ring

Consider the following "magic" 3-gon ring, filled with the numbers 1 to 6, 
and each line adding to nine.

Working clockwise, and starting from the group of three with the numerically 
lowest external node (4,3,2 in this example), each solution can be described 
uniquely. For example, the above solution can be described by the set: 
4,3,2; 6,2,1; 5,1,3.

It is possible to complete the ring with four different totals: 9, 10, 11, and 12. 
There are eight solutions in total.

By concatenating each group it is possible to form 9-digit strings; the maximum
string for a 3-gon ring is 432621513.

Using the numbers 1 to 10, and depending on arrangements, it is possible to form
16- and 17-digit strings. What is the maximum 16-digit string for a "magic" 5-gon ring?
"""

from itertools import permutations

def solution():
    max_string = ""
    
    numbers = list(range(1, 11))
    
    for inner in permutations(range(1, 10), 5):
        remaining = [x for x in numbers if x not in inner]
        
        for outer in permutations(remaining):
            lines = []
            total = outer[0] + inner[0] + inner[1]
            valid = True
            
            for i in range(5):
                line_sum = outer[i] + inner[i] + inner[(i + 1) % 5]
                if line_sum != total:
                    valid = False
                    break
                lines.append((outer[i], inner[i], inner[(i + 1) % 5]))
            
            if valid:
                min_outer = min(outer)
                start_idx = outer.index(min_outer)
                
                result = ""
                for i in range(5):
                    idx = (start_idx + i) % 5
                    for num in lines[idx]:
                        result += str(num)
                
                if len(result) == 16 and result > max_string:
                    max_string = result
    
    return max_string

if __name__ == "__main__":
    print(solution())  # Answer: 6531031914842725
