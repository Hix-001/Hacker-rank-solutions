#20/07/2026
#30 DAYS OF CODE IN PYTHON [DAY 19]
#INTERFACES
# HackerRank: Implement an interface and calculate divisor sum.

class AdvancedArithmetic(object):
    def divisorSum(n):
        raise NotImplementedError
class Calculator(AdvancedArithmetic):
    def divisorSum(self, n):
        total_sum = 0
        for i in range(1, n + 1):
            if n % i == 0:
                total_sum += i
        return total_sum


n = int(input())
my_calculator = Calculator()
s = my_calculator.divisorSum(n)
print("I implemented: " + type(my_calculator).__bases__[0].__name__)
print(s)