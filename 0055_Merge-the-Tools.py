#19/07/2026
#Medium
#Merge the Tools!
# HackerRank: Merge the Tools! using basic string slicing and iteration.

def merge_the_tools(string, k):
    for i in range(0, len(string), k):
        chunk = string[i:i+k]
        result = ""
        
        for char in chunk:
            if char not in result:
                result += char
                
        print(result)
if __name__ == '__main__':
    string, k = input(), int(input())
    merge_the_tools(string, k)
