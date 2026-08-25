#05/07/2026
#Easy
#What's Your Name?
# HackerRank: Given a first and last name, efficiently inject them into a specific greeting string and print the result.

def print_full_name(first, last):
    print(f"Hello {first} {last}! You just delved into python.")
if __name__ == '__main__':
    first_name = input()
    last_name = input()
    print_full_name(first_name, last_name)
