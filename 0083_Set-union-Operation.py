#05/08/2026
#Easy
#Set .union() Operation
# HackerRank: Find the total number of unique subscribers using Python set union.

_ = int(input())
english_subs = set(input().split())
_ = int(input())
french_subs = set(input().split())
total_students = len(english_subs.union(french_subs))
print(total_students)
