#09/08/2026
#Easy
#Set .discard(), .remove() & .pop()
# HackerRank: Execute dynamic set removal operations and calculate the remaining sum.
n = int(input())
s = set(map(int, input().split()))
num_commands = int(input())
for _ in range(num_commands):
    cmd = input().split()
    if len(cmd) > 1:
        getattr(s, cmd[0])(int(cmd[1]))
    else:
        getattr(s, cmd[0])()
print(sum(s))