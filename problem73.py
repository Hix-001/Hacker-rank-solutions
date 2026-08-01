#31/07/2026
#Easy
#Collections.namedtuple()
# HackerRank: Use namedtuple to extract student marks from columns in an unknown order and compute the average.
from collections import namedtuple
n = int(input())
Student = namedtuple('Student', input().split())
marks = [int(Student(*input().split()).MARKS) for _ in range(n)]
print(f"{sum(marks) / n:.2f}")