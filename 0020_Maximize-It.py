#hard question 
# HackerRank: Find the maximum possible value of $(X_1^2 + X_2^2 + \dots + X_K^2) \pmod{M}$ by picking exactly one element from $K$ given lists, utilizing the Cartesian product.
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