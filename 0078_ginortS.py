#02/08/2026
#Medium
#ginortS
# HackerRank: Sort a string prioritizing lowercase, then uppercase, then odd digits, then even digits.

if __name__ == '__main__':
    s = input()
    sorted_s = sorted(s, key=lambda c: (c.isdigit(), c in '02468', c.isupper(), c))
    print("".join(sorted_s))
