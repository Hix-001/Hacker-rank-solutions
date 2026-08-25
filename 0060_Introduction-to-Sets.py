#22/07/2026
#Easy
#Introduction To Sets
# HackerRank: Calculate the average of distinct items using Sets.

def average(array):
    distinct_heights = set(array)
    return sum(distinct_heights) / len(distinct_heights)
if __name__ == '__main__':
    n = int(input())
    arr = list(map(int, input().split()))
    result = average(arr)
    print(result)