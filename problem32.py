# HackerRank: Calculate earnings based on inventory availability using an optimal Hash Map (Counter).
from collections import Counter

if __name__ == '__main__':
    _ = input()
    inventory = Counter(map(int, input().split()))
    num_customers = int(input())
    
    earnings = 0
    
    for _ in range(num_customers):
        size, price = map(int, input().split())
        
        if inventory[size] > 0:
            earnings += price
            inventory[size] -= 1
            
    print(earnings)
