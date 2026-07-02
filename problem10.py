#Print a numerical triangle of height N-1 where each row i contains the digit i repeated i times using only arithmetic.
for i in range(1, int(input())):
    print(i * (10**i - 1) // 9)
    