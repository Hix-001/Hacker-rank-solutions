#18/08/2026
#Easy
#Zipped!
# HackerRank: Compute averages by transposing matrix columns to rows using zip and unpacking.

n, x = map(int, input().split())

sheet = [list(map(float, input().split())) for _ in range(x)]

for student_scores in zip(*sheet):
    print(f"{sum(student_scores) / x:.1f}")
