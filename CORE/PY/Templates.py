"""
================================================================================
Templates.py - Competitive Programming Production Templates
================================================================================
A library of modular, battle-tested, copy-pasteable data structures, algorithms,
and boilerplate templates for Codeforces, LeetCode, and HackerRank contests.

TABLE OF CONTENTS:
--------------------------------------------------------------------------------
1.  [TMP-01] Contest Fast I/O & Main Skeleton
2.  [TMP-02] Modular Arithmetic Class (ModInt)
3.  [TMP-03] Disjoint Set Union (DSU / Union-Find)
4.  [TMP-04] Fenwick Tree / Binary Indexed Tree (1D BIT)
5.  [TMP-05] Segment Tree (Range Minimum Query & Point Update)
6.  [TMP-06] Sieve of Eratosthenes & Smallest Prime Factor (SPF) Factorizer
7.  [TMP-07] Combinatorics / Factorials & Inverse Factorials mod P (nCr in O(1))
8.  [TMP-08] Extended Euclidean Algorithm & Diophantine Solver
9.  [TMP-09] Sliding Window Extremum Monotonic Deque
10. [TMP-10] Binary Search Standard Boundary Templates (Leftmost & Rightmost)
11. [TMP-11] Safe Hash Set & Dictionary (Codeforces Anti-Hash Shield)
================================================================================
"""

import sys
import math
import random
from collections import deque


# ==============================================================================
# [TMP-01] Contest Fast I/O & Main Skeleton
# ==============================================================================
"""
Usage:
    Copy-paste at the top of competitive programming scripts to maximize I/O throughput.
    Reads all tokens in a single system call and provides an iterator.
"""

def solve_io():
    """Template demonstrating fast bulk token ingestion."""
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    iterator = iter(input_data)
    
    # Read tokens via next(iterator)
    # Example: t = int(next(iterator))
    out = []
    # Accumulate results in out, then flush once:
    # sys.stdout.write("\n".join(out) + "\n")


# ==============================================================================
# [TMP-02] Modular Arithmetic Class (ModInt)
# ==============================================================================
"""
Usage:
    Provides automatic modular arithmetic with operators +, -, *, /, pow, and ==.
    Eliminates tedious repetitive `% MOD` statements.
"""

MOD = 1_000_000_007

class ModInt:
    __slots__ = ('val',)
    
    def __init__(self, val=0):
        self.val = val % MOD

    def __add__(self, other):
        o = other.val if isinstance(other, ModInt) else other
        return ModInt(self.val + o)

    def __sub__(self, other):
        o = other.val if isinstance(other, ModInt) else other
        return ModInt(self.val - o)

    def __mul__(self, other):
        o = other.val if isinstance(other, ModInt) else other
        return ModInt(self.val * o)

    def __truediv__(self, other):
        o = other.val if isinstance(other, ModInt) else other
        # Fermat's Little Theorem: inverse of o is o^(MOD - 2)
        inv = pow(o, MOD - 2, MOD)
        return ModInt(self.val * inv)

    def __pow__(self, p):
        return ModInt(pow(self.val, p, MOD))

    def __neg__(self):
        return ModInt(-self.val)

    def __eq__(self, other):
        o = other.val if isinstance(other, ModInt) else other
        return self.val == (o % MOD)

    def __int__(self):
        return self.val

    def __repr__(self):
        return str(self.val)


# ==============================================================================
# [TMP-03] Disjoint Set Union (DSU / Union-Find)
# ==============================================================================
"""
Usage:
    Maintains dynamic connectivity, connected component counts, and component sizes
    in near-O(1) amortized time via path compression and union by size.
"""

class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n
        self.num_sets = n

    def find(self, i: int) -> int:
        root = i
        while root != self.parent[root]:
            root = self.parent[root]
        # Path compression
        curr = i
        while curr != root:
            nxt = self.parent[curr]
            self.parent[curr] = root
            curr = nxt
        return root

    def union(self, i: int, j: int) -> bool:
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i == root_j:
            return False
        if self.size[root_i] < self.size[root_j]:
            root_i, root_j = root_j, root_i
        self.parent[root_j] = root_i
        self.size[root_i] += self.size[root_j]
        self.num_sets -= 1
        return True

    def get_size(self, i: int) -> int:
        return self.size[self.find(i)]

    def is_connected(self, i: int, j: int) -> bool:
        return self.find(i) == self.find(j)


# ==============================================================================
# [TMP-04] Fenwick Tree / Binary Indexed Tree (1D BIT)
# ==============================================================================
"""
Usage:
    Point update in O(log N) and prefix sum query in O(log N).
    1-indexed internally for clean bitwise lowbit logic: `i & (-i)`.
"""

class FenwickTree:
    def __init__(self, n: int):
        self.n = n
        self.tree = [0] * (n + 1)

    def add(self, i: int, delta: int):
        """Adds delta to 1-based index i in O(log N)."""
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)

    def query(self, i: int) -> int:
        """Returns prefix sum A[1..i] in O(log N)."""
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s

    def range_query(self, l: int, r: int) -> int:
        """Returns sum of elements in range [l, r] in O(log N)."""
        return self.query(r) - self.query(l - 1)


# ==============================================================================
# [TMP-05] Segment Tree (Range Minimum Query & Point Update)
# ==============================================================================
"""
Usage:
    Maintains arbitrary associative operations (min, max, sum, gcd) over ranges.
    Point update in O(log N), Range query in O(log N).
"""

class SegmentTreeRMQ:
    def __init__(self, arr: list):
        self.n = len(arr)
        self.tree = [float('inf')] * (4 * self.n)
        if self.n > 0:
            self._build(arr, 1, 0, self.n - 1)

    def _build(self, arr: list, node: int, start: int, end: int):
        if start == end:
            self.tree[node] = arr[start]
            return
        mid = (start + end) // 2
        self._build(arr, 2 * node, start, mid)
        self._build(arr, 2 * node + 1, mid + 1, end)
        self.tree[node] = min(self.tree[2 * node], self.tree[2 * node + 1])

    def update(self, idx: int, val: int, node: int = 1, start: int = 0, end: int = None):
        """Updates element at 0-based index idx to val in O(log N)."""
        if end is None:
            end = self.n - 1
        if start == end:
            self.tree[node] = val
            return
        mid = (start + end) // 2
        if start <= idx <= mid:
            self.update(idx, val, 2 * node, start, mid)
        else:
            self.update(idx, val, 2 * node + 1, mid + 1, end)
        self.tree[node] = min(self.tree[2 * node], self.tree[2 * node + 1])

    def query(self, l: int, r: int, node: int = 1, start: int = 0, end: int = None) -> int:
        """Returns minimum in range [l, r] inclusive in O(log N)."""
        if end is None:
            end = self.n - 1
        if r < start or end < l:
            return float('inf')
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        p1 = self.query(l, r, 2 * node, start, mid)
        p2 = self.query(l, r, 2 * node + 1, mid + 1, end)
        return min(p1, p2)


# ==============================================================================
# [TMP-06] Sieve of Eratosthenes & Smallest Prime Factor (SPF) Factorizer
# ==============================================================================
"""
Usage:
    Precomputes Smallest Prime Factor (SPF) up to N in O(N log log N).
    Enables O(log X) prime factorization for any query X <= N.
"""

def compute_spf(max_n: int) -> list:
    """Precomputes smallest prime factor for all numbers up to max_n."""
    spf = list(range(max_n + 1))
    for i in range(2, int(math.isqrt(max_n)) + 1):
        if spf[i] == i:  # i is prime
            for j in range(i * i, max_n + 1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf

def factorize_fast(x: int, spf: list) -> list:
    """Factorizes integer x into prime factors in O(log x) time using precomputed SPF."""
    factors = []
    while x > 1:
        factors.append(spf[x])
        x //= spf[x]
    return factors


# ==============================================================================
# [TMP-07] Combinatorics / Factorials & Inverse Factorials mod P (nCr in O(1))
# ==============================================================================
"""
Usage:
    Precomputes factorials and inverse factorials up to N in O(N).
    Enables O(1) query of nCr % MOD.
"""

class CombinatoricsMod:
    def __init__(self, max_n: int, mod: int = MOD):
        self.mod = mod
        self.fact = [1] * (max_n + 1)
        self.inv_fact = [1] * (max_n + 1)
        
        for i in range(1, max_n + 1):
            self.fact[i] = (self.fact[i - 1] * i) % mod
            
        # Fermat's Little Theorem for inverse of fact[max_n]
        self.inv_fact[max_n] = pow(self.fact[max_n], mod - 2, mod)
        for i in range(max_n - 1, 0, -1):
            self.inv_fact[i] = (self.inv_fact[i + 1] * (i + 1)) % mod

    def nCr(self, n: int, r: int) -> int:
        if r < 0 or r > n:
            return 0
        num = self.fact[n]
        den = (self.inv_fact[r] * self.inv_fact[n - r]) % self.mod
        return (num * den) % self.mod


# ==============================================================================
# [TMP-08] Extended Euclidean Algorithm & Diophantine Solver
# ==============================================================================
"""
Usage:
    Finds integer solutions (x, y) to Bezout's identity: a*x + b*y = gcd(a, b).
    Computes modular inverse when mod is not prime.
"""

def ext_gcd(a: int, b: int) -> tuple:
    """Returns (gcd, x, y) such that a*x + b*y = gcd(a, b)."""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = ext_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y

def mod_inverse(a: int, m: int) -> int:
    """Computes modular inverse of a modulo m using Extended Euclidean Algorithm."""
    g, x, _ = ext_gcd(a, m)
    if g != 1:
        raise ValueError(f"Inverse does not exist: {a} and {m} are not coprime")
    return (x % m + m) % m


# ==============================================================================
# [TMP-09] Sliding Window Extremum Monotonic Deque
# ==============================================================================
"""
Usage:
    Finds sliding window minimum or maximum over dynamic or fixed streams in O(N).
"""

class MonotonicQueue:
    def __init__(self, mode='min'):
        self.dq = deque()  # stores (value, index)
        self.is_min = (mode == 'min')

    def push(self, val: int, idx: int):
        if self.is_min:
            while self.dq and self.dq[-1][0] >= val:
                self.dq.pop()
        else:
            while self.dq and self.dq[-1][0] <= val:
                self.dq.pop()
        self.dq.append((val, idx))

    def pop(self, min_valid_idx: int):
        while self.dq and self.dq[0][1] < min_valid_idx:
            self.dq.popleft()

    def get_extremum(self) -> int:
        return self.dq[0][0]


# ==============================================================================
# [TMP-10] Binary Search Standard Boundary Templates (Leftmost & Rightmost)
# ==============================================================================
"""
Usage:
    - `bsearch_left`: Finds smallest index i in [low, high] satisfying condition(i) == True.
    - `bsearch_right`: Finds largest index i in [low, high] satisfying condition(i) == True.
"""

def bsearch_leftmost(low: int, high: int, condition_fn) -> int:
    """Returns first index where condition_fn(i) is True (TTTTT... regime)."""
    ans = -1
    while low <= high:
        mid = (low + high) // 2
        if condition_fn(mid):
            ans = mid
            high = mid - 1
        else:
            low = mid + 1
    return ans

def bsearch_rightmost(low: int, high: int, condition_fn) -> int:
    """Returns last index where condition_fn(i) is True (TTTTT... regime)."""
    ans = -1
    while low <= high:
        mid = (low + high) // 2
        if condition_fn(mid):
            ans = mid
            low = mid + 1
        else:
            high = mid - 1
    return ans


# ==============================================================================
# [TMP-11] Safe Hash Set & Dictionary (Codeforces Anti-Hash Shield)
# ==============================================================================
"""
Usage:
    Drop-in replacement for set/dict that eliminates O(N^2) anti-hash test hacks.
"""

CF_SALT = random.getrandbits(61)

class SafeSet:
    def __init__(self, iterable=None):
        self._inner = set()
        if iterable:
            for x in iterable:
                self.add(x)

    def add(self, x: int):
        self._inner.add(x ^ CF_SALT)

    def discard(self, x: int):
        self._inner.discard(x ^ CF_SALT)

    def __contains__(self, x: int):
        return (x ^ CF_SALT) in self._inner

    def __len__(self):
        return len(self._inner)


# ==============================================================================
# SELF-TEST SUITE
# ==============================================================================
if __name__ == '__main__':
    # Test TMP-02: ModInt
    a = ModInt(MOD - 2)
    b = ModInt(5)
    assert int(a + b) == 3
    assert int(b / b) == 1
    assert int(ModInt(2) ** 10) == 1024
    
    # Test TMP-03: DSU
    dsu = DSU(5)
    dsu.union(0, 1)
    dsu.union(1, 2)
    assert dsu.is_connected(0, 2) is True
    assert dsu.is_connected(0, 3) is False
    assert dsu.get_size(0) == 3
    
    # Test TMP-04: FenwickTree
    ft = FenwickTree(5)
    ft.add(1, 10)
    ft.add(2, 20)
    ft.add(3, 30)
    assert ft.query(3) == 60
    assert ft.range_query(2, 3) == 50
    
    # Test TMP-05: SegmentTreeRMQ
    st = SegmentTreeRMQ([18, 17, 13, 19, 15, 11, 20])
    assert st.query(1, 4) == 13  # min of [17, 13, 19, 15]
    st.update(2, 25)
    assert st.query(1, 4) == 15  # min of [17, 25, 19, 15]
    
    # Test TMP-06: SPF Factorizer
    spf = compute_spf(100)
    assert factorize_fast(60, spf) == [2, 2, 3, 5]
    
    # Test TMP-07: CombinatoricsMod
    comb = CombinatoricsMod(10, MOD)
    assert comb.nCr(5, 2) == 10
    assert comb.nCr(5, 0) == 1
    assert comb.nCr(5, 5) == 1
    
    # Test TMP-08: Extended Euclidean & Mod Inverse
    g, x, y = ext_gcd(30, 20)
    assert g == 10 and 30 * x + 20 * y == 10
    assert mod_inverse(3, 7) == 5  # 3 * 5 = 15 = 1 mod 7
    
    # Test TMP-09: MonotonicQueue
    mq = MonotonicQueue(mode='min')
    mq.push(10, 0)
    mq.push(5, 1)
    mq.push(8, 2)
    assert mq.get_extremum() == 5
    mq.pop(min_valid_idx=2)
    assert mq.get_extremum() == 8
    
    # Test TMP-10: Binary Search
    # Leftmost x where x^2 >= 20
    assert bsearch_leftmost(1, 10, lambda x: x * x >= 20) == 5
    # Rightmost x where x^2 <= 50
    assert bsearch_rightmost(1, 10, lambda x: x * x <= 50) == 7
    
    # Test TMP-11: SafeSet
    ss = SafeSet([10, 20, 30])
    assert 20 in ss
    assert 40 not in ss
    assert len(ss) == 3

    print("ALL Templates.py tests passed successfully!")
