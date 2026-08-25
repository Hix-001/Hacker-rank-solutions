#02/08/2026
#Easy
#Collections.OrderedDict
# HackerRank: Calculate item totals and print them in order of their first appearance using OrderedDict.

from collections import OrderedDict
n = int(input())
ordered_dict = OrderedDict()
for _ in range(n):
    *name_parts, price = input().split()
    item_name = " ".join(name_parts)
    price = int(price)
    ordered_dict[item_name] = ordered_dict.get(item_name, 0) + price
for item, net_price in ordered_dict.items():
    print(f"{item} {net_price}")
