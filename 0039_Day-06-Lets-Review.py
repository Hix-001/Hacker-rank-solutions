#30 DAYS OF CODE IN PYTHON [DAY 06]
# HackerRank: Separate a string into even and odd indexed characters using optimal string slicing.
if __name__ == '__main__':
    T = int(input().strip())
    for _ in range(T):
        S = input().strip()
        print(f"{S[::2]} {S[1::2]}")