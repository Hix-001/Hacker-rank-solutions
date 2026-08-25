#02/08/2026
#Medium
#Word Order
# HackerRank: Count distinct words and print their frequencies in order of appearance.

n = int(input())
word_counts = {}
for _ in range(n):
    word = input().strip()
    word_counts[word] = word_counts.get(word, 0) + 1
print(len(word_counts))
print(*word_counts.values())
