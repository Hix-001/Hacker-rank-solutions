#05/07/2026
#Easy
#Power - Mod Power
# HackerRank: Read three integers and print a^b and a^b mod m.

if __name__ == '__main__':
    a = int(input())
    b = int(input())
    m = int(input())
    print(pow(a, b))
    print(pow(a, b, m))
    
