#11/07/2026
#Easy
#Q44
#Binary Numbers
# HackerRank: Find the maximum consecutive 1s in a binary string using optimal string splitting.

if __name__ == '__main__':
    n = int(input().strip())
    print(max(map(len, bin(n)[2:].split('0'))))
