#08/07/2026
#30 DAYS OF CODE IN PYTHON [DAY 07]
#ARRAYS
# HackerRank: Reverse an array and print space-separated elements using optimal slicing and unpacking.
if __name__ == '__main__':
    n = int(input().strip())
    arr = input().strip().split()
    print(*arr[::-1])