#04/07/2026
#Easy
#Mutations
# HackerRank: Replace a character at a specific index in an immutable string using optimal slicing.

def count_substring(string, sub_string):
    return sum(1 for i in range(len(string) - len(sub_string) + 1) if string.startswith(sub_string, i))
if __name__ == '__main__':
    string = input().strip()
    sub_string = input().strip()
    count = count_substring(string, sub_string)
    print(count)
