#26/07/2026
#Medium
#Running Time and Complexity
# HackerRank: Determine if a given number is prime using an optimized O(sqrt(n)) algorithm.

import math
def is_prime(n):
    if n <= 1:
        return "Not prime"
    if n == 2:
        return "Prime"
    if n % 2 == 0:
        return "Not prime"
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return "Not prime" 
    return "Prime"
if __name__ == '__main__':
    T = int(input().strip())
    for _ in range(T):
        n = int(input().strip())
        print(is_prime(n))
