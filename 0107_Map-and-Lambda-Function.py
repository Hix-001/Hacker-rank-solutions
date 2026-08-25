#24/08/2026
#Easy
#Map and Lambda Function
# HackerRank: Generate a sequence and transform it using functional programming tools.
 
cube = lambda x: x ** 3

def fibonacci(n):
    if n == 0:
        return []
    if n == 1:
        return [0]
    
    fib = [0, 1]
    for _ in range(2, n):
        fib.append(fib[-1] + fib[-2])
        
    return fib

if __name__ == '__main__':
    n = int(input())
    print(list(map(cube, fibonacci(n))))