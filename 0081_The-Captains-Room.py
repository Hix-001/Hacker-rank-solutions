#03/08/2026
#Easy
#The Captain's Room
# HackerRank: Find the non-repeating room number in an array using sets and math.

k = int(input())
rooms = list(map(int, input().split()))
unique_rooms = set(rooms)
captain_room = ((sum(unique_rooms) * k) - sum(rooms)) // (k - 1)
print(captain_room)
