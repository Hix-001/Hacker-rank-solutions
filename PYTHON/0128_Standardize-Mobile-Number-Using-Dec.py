#08/09/2026
#Medium
#Standardize Mobile Number Using Decorators
# HackerRank: Use a decorator closure to sanitize string formats before processing.

def wrapper(f):
    def fun(l):
        f(["+91 " + n[-10:-5] + " " + n[-5:] for n in l])
    return fun

@wrapper
def sort_phone(l):
    print(*sorted(l), sep='\n')

if __name__ == '__main__':
    l = [input() for _ in range(int(input()))]
    sort_phone(l) 


