#18/07/2026
#30 DAYS OF CODE IN PYTHON [DAY 17]
#MORE EXCEPTIONS
# HackerRank: Throw exceptions in a Calculator class. 

class Calculator:
    def power(self, n, p):
        if n < 0 or p < 0:
            raise Exception("n and p should be non-negative")
        return n ** p
myCalculator=Calculator()
T=int(input())
for i in range(T):
    n,p = map(int, input().split())
    try:
        ans=myCalculator.power(n,p)
        print(ans)
    except Exception as e:
        print(e)   