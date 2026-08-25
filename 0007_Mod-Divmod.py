# HackerRank: Read two integers and print integer division, modulo, and divmod result.
if __name__ == '__main__':
    a = int(input())
    b = int(input())
    print(a // b)
    print(a % b)
    print(divmod(a, b))