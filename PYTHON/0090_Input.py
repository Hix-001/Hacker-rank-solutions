#10/08/2026
#Easy
#Input()
# HackerRank: Evaluate a polynomial string mathematically using the eval() function.

if __name__ == '__main__':
    x, k = map(int, input().split())
    poly = input()
    print(eval(poly) == k)
