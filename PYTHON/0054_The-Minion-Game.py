#19/07/2026
#Medium
#Minion Game
# HackerRank: Solve the Minion Game using O(N) mathematical index calculation.

def minion_game(string):
    vowels = "AEIOU"
    kevin_score = 0
    stuart_score = 0
    length = len(string)
    
    for i in range(length):
        if string[i] in vowels:
            kevin_score += length - i
        else:
            stuart_score += length - i
            
    if kevin_score > stuart_score:
        print("Kevin " + str(kevin_score))
    elif stuart_score > kevin_score:
        print("Stuart " + str(stuart_score))
    else:
        print("Draw")
if __name__ == '__main__':
    s = input()
    minion_game(s)
