#05/07/2026
#Easy
#Find the Runner-Up Score!
# HackerRank: Given a list of participant scores, identify the second-highest unique value.

if __name__ == '__main__':
    n = int(input())
    arr = list(set(map(int, input().split())))
    arr.sort(reverse=True)
    print(arr[1])
    
