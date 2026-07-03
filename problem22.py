#Given a string, return a new string where all lowercase letters are converted to uppercase letters and vice versa.
def swap_case(s):
    return s.swapcase()
if __name__ == '__main__':
    s = input()
    result = swap_case(s)
    print(result)