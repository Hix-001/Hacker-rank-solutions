#13/08/2026
#Easy
#Set .symmetric_difference() Operation
# HackerRank: Count students subscribed to exactly one newspaper using symmetric difference.

_ = int(input())
english_subs = set(input().split())
_ = int(input())
french_subs = set(input().split())
sym_diff = english_subs.symmetric_difference(french_subs)
print(len(sym_diff))