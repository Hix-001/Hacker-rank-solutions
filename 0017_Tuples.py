# Create a tuple from a sequence of $n$ input integers and print the resulting hash value using Python’s built-in hash() function.
# ==============================================================================
# Problem: Tuples (HackerRank)
# Description: Read a sequence of space-separated integers, convert them into an 
#              immutable tuple, and calculate its hash value using built-ins.
#
# PLATFORM NOTE: This is the correct, modern Python 3 implementation. However, 
# HackerRank's legacy test cases for this specific problem require deterministic 
# hashing. To pass on the platform, you must switch the compiler to PyPy 2 
# and use Python 2 syntax: `print hash(tuple(integer_list))`
# ==============================================================================

if __name__ == '__main__':
    n = int(input())
    integer_list = map(int, input().split())
    t = tuple(integer_list)
    print(hash(t))