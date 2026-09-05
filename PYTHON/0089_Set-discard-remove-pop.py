#09/08/2026
#Easy
#Set .discard(), .remove() & .pop()
# HackerRank: Execute dynamic set removal operations and calculate the remaining sum.

import sys
tokens = sys.stdin.read().split()
if not tokens:
    exit()
n = int(tokens[0])
s = set(int(x) for x in tokens[1:n+1])
command_iterator = iter(tokens[n+2:])
for cmd in command_iterator:
    if cmd == 'pop':
        if s:
            s.pop()
    elif cmd in ('remove', 'discard'):
        try:
            val = int(next(command_iterator))
            s.discard(val)
        except StopIteration:
            break
print(sum(s))
