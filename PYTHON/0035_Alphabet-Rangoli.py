#07/07/2026
#Easy
#Alphabet Rangoli
# HackerRank: Generate an alphabetical rangoli pattern using symmetrical array slicing and string centering.

def print_rangoli(size):
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    width = 4 * size - 3
    lines = []
    
    for i in range(size):
        chars = alpha[size - i - 1 : size]
        row_palindrome = chars[::-1] + chars[1:]
        row_str = '-'.join(row_palindrome)
        lines.append(row_str.center(width, '-'))
        
    print('\n'.join(lines + lines[:-1][::-1]))

if __name__ == '__main__':
    n = int(input())
    print_rangoli(n)
