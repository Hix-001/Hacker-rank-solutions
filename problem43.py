#10/07/2026
#30 DAYS OF CODE IN PYTHON [DAY 09]
# RECURSION 3
# HackerRank: Calculate the factorial of a number using a strictly recursive algorithm.
import os

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    n = int(input().strip())
    result = factorial(n)
    fptr.write(str(result) + '\n')
    fptr.close()