#06/07/2026
#Easy
#Designer Door Mat
# HackerRank: Generate an aligned, symmetrical ASCII door mat using string centering and list reversals.

if __name__ == '__main__':
    n, m = map(int, input().split())
    
    pattern = [('.|.' * (2 * i + 1)).center(m, '-') for i in range(n // 2)]
    
    print('\n'.join(pattern + ['WELCOME'.center(m, '-')] + pattern[::-1]))
