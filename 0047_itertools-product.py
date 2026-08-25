#13/07/2026
# HackerRank: Compute the Cartesian product of two lists using basic nested loops.

string_line_A = input().split()
list_A = []
for string_number in string_line_A:
    list_A.append(int(string_number))
    
string_line_B = input().split()
list_B = []
for string_number in string_line_B:
    list_B.append(int(string_number))

for a in list_A:
    for b in list_B:
        pair = (a, b)
        print(pair, end=" ")