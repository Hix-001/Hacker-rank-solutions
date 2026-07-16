#15/07/2026
#30 DAYS OF CODE IN PYTHON [DAY 14]
#SCOPE
# HackerRank: Calculate the maximum absolute difference using class scope.
class Difference:
    def __init__(self, a):
        self.__elements = a
        self.maximumDifference = 0

    def computeDifference(self):
        min_element = min(self.__elements)
        max_element = max(self.__elements)
        self.maximumDifference = max_element - min_element

_ = input()
a = [int(e) for e in input().split(' ')]

d = Difference(a)
d.computeDifference()

print(d.maximumDifference)  