#05/07/2026
#Easy
#Nested Lists
# HackerRank: From a list of students and their grades, output the names of those who achieved the second-lowest grade, ordered alphabetically.

if __name__ == '__main__':
    students = []
    for _ in range(int(input())):
        name = input()
        grade = float(input())
        students.append([name, grade])
    
    unique_grades = sorted(list(set(s[1] for s in students)))
    second_lowest = unique_grades[1]
    
    names = sorted([s[0] for s in students if s[1] == second_lowest])
    
    for name in names:
        print(name)
        
