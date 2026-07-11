#30 DAYS OF CODE IN PYTHON [DAY 07]
#DICTIONARIES AND MAPS
# HackerRank: Build a dictionary and process an unknown number of queries handling EOF safely.
import sys

if __name__ == '__main__':
    n = int(input().strip())
    phone_book = {}
    
    for _ in range(n):
        name, number = input().strip().split()
        phone_book[name] = number
        
    queries = sys.stdin.read().splitlines()
    
    for query in queries:
        number = phone_book.get(query)
        if number:
            print(f"{query}={number}")
        else:
            print("Not found")