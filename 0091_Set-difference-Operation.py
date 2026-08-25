#11/08/2026
#Easy
#Set .difference() Operation
# HackerRank: Find the number of students subscribed only to one newspaper using set difference.

_ = int(input())
english_subs = set(input().split())
_ = int(input())
french_subs = set(input().split())
only_english = english_subs.difference(french_subs)
print(len(only_english))
