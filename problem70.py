#28/07/2026
#Easy
#Exceptions
# HackerRank: Handle ZeroDivisionError and ValueError using try-except blocks.

T = int(input())
for _ in range(T):
    a, b = input().split()
    try:
        print(int(a) // int(b))
    except ZeroDivisionError as e:
        print(f"Error Code: integer division or modulo by zero")
    except ValueError as e:
        print(f"Error Code: {e}")