#05/07/2026
#Easy
#Print Function
# HackerRank: Print the sequence of numbers from 1 to n concatenated without spaces.

if __name__ == '__main__':
    n = int(input())
    for i in range(1, n + 1):
        print(i, end='')
