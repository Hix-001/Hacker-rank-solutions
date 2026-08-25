#12/08/2026
#Easy
#Set .intersection() Operation
# HackerRank: Find the number of students subscribed to both newspapers using set intersection.

_ = int(input())
english_subs = set(input().split())
_ = int(input())
french_subs = set(input().split())
both_subs = english_subs.intersection(french_subs)
print(len(both_subs))