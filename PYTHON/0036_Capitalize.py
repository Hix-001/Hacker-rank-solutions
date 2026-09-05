#08/07/2026
#Easy
#Capitalize!
# HackerRank: Capitalize the first letter of each word in a string while preserving exact whitespace.

import os

def solve(s):
    return ' '.join(word.capitalize() for word in s.split(' '))

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    s = input()
    result = solve(s)
    fptr.write(result + '\n')
    fptr.close()
    
