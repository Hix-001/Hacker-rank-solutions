#05/07/2026
#Hard
#Maximize It!
# HackerRank: Find the maximum possible value of sum(X_i^2) % M by picking one element from K lists using Cartesian product.

import itertools
if __name__ == '__main__':
    k, m = map(int, input().split())
    lists = []
    for _ in range(k):
        raw_list = list(map(int, input().split()))
        processed_list = [(x**2) % m for x in raw_list[1:]]
        lists.append(processed_list)
    result = max(sum(combination) % m for combination in itertools.product(*lists))
    print(result)
