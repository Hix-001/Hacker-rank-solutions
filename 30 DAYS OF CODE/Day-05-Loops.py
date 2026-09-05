#08/07/2026
#Easy
#Q38
#Loops
# HackerRank: Print the first 10 multiples of an integer using an iterative loop and f-string formatting.

if __name__ == '__main__':
    n = int(input().strip())
    
    for i in range(1, 11):
        print(f"{n} x {i} = {n * i}")
