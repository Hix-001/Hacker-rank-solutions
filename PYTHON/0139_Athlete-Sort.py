#09/09/2026
#Medium
#Athlete Sort
# HackerRank: Sort a 2D array based on a specific column index using a lambda key.

if __name__ == '__main__':
    nm = input().split()
    n = int(nm[0])
    m = int(nm[1])

    arr = []
    for _ in range(n):
        arr.append(list(map(int, input().rstrip().split())))

    k = int(input())

    arr.sort(key=lambda x: x[k])
    
    for row in arr:
        print(*row)