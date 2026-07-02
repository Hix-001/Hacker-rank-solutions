# Create a tuple from a sequence of $n$ input integers and print the resulting hash value using Python’s built-in hash() function.
if __name__ == '__main__':
    n = int(raw_input())
    integer_list = map(int, input().split())
    print(hash(tuple(integer_list)))