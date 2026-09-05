#05/07/2026
#Easy
#Lists
# HackerRank: Implement a command-driven interface to perform dynamic list operations based on sequential input commands.

if __name__ == '__main__':
    N = int(input())
    my_list = []
    for _ in range(N):
        cmd, *args = input().split()
        args = list(map(int, args))
        if cmd == "print":
            print(my_list)
        else:
            getattr(my_list, cmd)(*args)
