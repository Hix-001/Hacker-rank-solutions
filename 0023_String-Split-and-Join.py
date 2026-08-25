#23/08/2026
#Easy
#String Split and Join
# HackerRank: Given a string of space separated words, replace all space delimiters with hyphens.

def split_and_join(line):
    return line.replace(" ", "-")
if __name__ == '__main__':
    line = input()
    result = split_and_join(line)
    print(result)
