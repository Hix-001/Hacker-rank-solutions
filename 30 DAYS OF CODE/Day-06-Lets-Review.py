#07/07/2026
#Easy
#Q39
#Let's Review
# HackerRank: Separate a string into even and odd indexed characters using optimal string slicing.

if __name__ == '__main__':
    T = int(input().strip())
    for _ in range(T):
        S = input().strip()
        print(f"{S[::2]} {S[1::2]}")
