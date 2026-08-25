#02/07/2026
#Easy
#Tuples
# HackerRank: Create a tuple from a sequence of n input integers and print the resulting hash value using Python's built-in hash() function.

if __name__ == '__main__':
    n = int(input())
    integer_list = map(int, input().split())
    t = tuple(integer_list)
    print(hash(t))
