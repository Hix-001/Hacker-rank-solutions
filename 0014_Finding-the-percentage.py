# HackerRank: Calculate the average of a specific student's grades from a dictionary of student records, and format the output to exactly two decimal places.
if __name__ == '__main__':
    n = int(input())
    student_marks = {}
    for _ in range(n):
        name, *line = input().split()
        scores = list(map(float, line))
        student_marks[name] = scores
    query_name = input()
    
    avg = sum(student_marks[query_name]) / len(student_marks[query_name])
    print(f"{avg:.2f}")
    