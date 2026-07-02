#Given an integer n, perform conditional actions: if odd print "Weird", if even in range 2-5 print "Not Weird", 6-20 print "Weird", >20 print "Not Weird".
if __name__ == '__main__':
    n = int(input().strip())
    
    if n % 2 != 0 or (6 <= n <= 20):
        print("Weird")
    else:
        print("Not Weird")

