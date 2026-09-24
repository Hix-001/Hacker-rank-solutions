"""
================================================================================
PitfallsAndErrors.py - Python Competitive Programming Traps & Debugging Guide
================================================================================
A comprehensive diagnostic handbook detailing common traps, subtle runtime
pitfalls, and performance bottlenecks in Python that cause Time Limit Exceeded (TLE),
Memory Limit Exceeded (MLE), Wrong Answer (WA), and Runtime Errors (RTE) on
Codeforces, LeetCode, and HackerRank.

TABLE OF CONTENTS:
--------------------------------------------------------------------------------
1.  [PIT-01] Recursion Limit Exceeded & Stack Overflow (RTE)
2.  [PIT-02] Codeforces Anti-Hash Collision Attacks (O(N^2) TLE in Dict/Set)
3.  [PIT-03] Floating-Point Precision Loss & Float Division Gotchas (WA)
4.  [PIT-04] O(N^2) String Concatenation in Loops (TLE)
5.  [PIT-05] The O(N) list.pop(0) / list.insert(0) Queue Trap (TLE)
6.  [PIT-06] The 2D Matrix Shallow Copy Trap (`[[0]*M]*N`) (WA)
7.  [PIT-07] Bitwise Operator Precedence Traps (WA)
8.  [PIT-08] Lexicographical Number Comparison Trap (WA)
9.  [PIT-09] Modifying Collections While Iterating (RTE / Skipped Elements)
10. [PIT-10] Slicing Inside Loops Causing Hidden O(K) Copies (TLE)
11. [PIT-11] Slow Standard I/O Overhead on 10^5+ Lines (TLE)
12. [PIT-12] Python's Round-Half-To-Even "Banker's Rounding" (WA)
================================================================================
"""

import sys
import math
import random
import time
from collections import deque


# ==============================================================================
# [PIT-01] Recursion Limit Exceeded & Stack Overflow (RTE)
# ==============================================================================
"""
Trap:
    Python's default recursion limit is 1,000 stack frames.
    Any deep DFS, tree traversal, or divide-and-conquer algorithm on graphs
    with N >= 1,000 will throw `RecursionError: maximum recursion depth exceeded`.

Why It Happens:
    Python maintains detailed frame objects for stack traces, so the interpreter
    guards against C-level stack overflow with a strict artificial limit.

How To Fix It:
    1. Increase the limit at the very top of your solution:
       `sys.setrecursionlimit(300000)`
    2. On platforms like Codeforces running on Windows, if the native C stack is
       exceeded, use an iterative DFS with an explicit list stack, or run your logic
       in a separate thread with a custom stack size:
       `threading.stack_size(1024 * 1024 * 128)` (128 MB stack).
"""

def demonstrate_recursion_fix():
    # Demonstrates safe recursion limit expansion
    old_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(5000)
    
    def deep_sum(n):
        if n == 0:
            return 0
        return 1 + deep_sum(n - 1)
    
    result = deep_sum(2500)
    sys.setrecursionlimit(old_limit)  # Restore
    return result


# ==============================================================================
# [PIT-02] Codeforces Anti-Hash Collision Attacks (O(N^2) TLE in Dict/Set)
# ==============================================================================
"""
Trap:
    On Codeforces (and some competitive programming platforms), tests are generated
    specifically to exploit Python's deterministic built-in integer hash function:
        `hash(x) == x` (for small integers).
    Adversaries construct inputs where all values share identical hash buckets
    modulo the dictionary's table size, triggering continuous hash collisions.
    This degrades `dict` and `set` lookups from O(1) average to O(N) worst-case,
    causing an otherwise optimal O(N) algorithm to take O(N^2) and TLE!

Why It Happens:
    Python hashes integers directly to their integer values. The hash table capacity
    is always a power of 2, making collision generation trivial for problem setters.

How To Fix It:
    Use a randomized 64-bit salt XOR-ed with each key:
        `RANDOM_SALT = random.getrandbits(61)`
        `def safe_hash(x): return x ^ RANDOM_SALT`
    Wrap keys or use a custom dict class.
"""

RANDOM_SALT = random.getrandbits(61)

class SafeDict(dict):
    """Wrapper that prevents anti-hash collision attacks by salting keys."""
    def __setitem__(self, key, value):
        super().__setitem__(key ^ RANDOM_SALT, value)
    def __getitem__(self, key):
        return super().__getitem__(key ^ RANDOM_SALT)
    def __contains__(self, key):
        return super().__contains__(key ^ RANDOM_SALT)
    def get(self, key, default=None):
        return super().get(key ^ RANDOM_SALT, default)


# ==============================================================================
# [PIT-03] Floating-Point Precision Loss & Float Division Gotchas (WA)
# ==============================================================================
"""
Trap:
    1. Using `/` instead of `//` converts exact integers into 64-bit IEEE-754 floats.
       Floats only have 53 bits of mantissa (~15 to 17 decimal digits of precision).
       For 64-bit integers (e.g., 10^18), float division silently truncates precision:
           `int(10**18 / 3 * 3) != 10**18`
    2. Using `int(math.sqrt(x))` on large integers (e.g., 10^18) causes precision drift.

How To Fix It:
    - Always use integer floor division `//` when working with integer arithmetic.
    - Use `math.isqrt(x)` for exact integer square roots (Python 3.8+).
"""

def demonstrate_precision_pitfall():
    large_int = 10**18 + 7
    float_res = int((large_int // 10) * 10)  # Exact integer math
    return float_res


# ==============================================================================
# [PIT-04] O(N^2) String Concatenation in Loops (TLE)
# ==============================================================================
"""
Trap:
    Writing `s += char` inside a loop of size N.
    Strings in Python are immutable. Each `+=` allocates a new string in memory
    and copies all previous i characters, resulting in:
        1 + 2 + 3 + ... + N = O(N^2) operations.
    For N = 10^5, this takes ~15 seconds and causes instant TLE.

How To Fix It:
    Append characters or chunks to a list, then join them once at the end:
        `parts = []`
        `for char in stream: parts.append(char)`
        `result = "".join(parts)`  # Strictly O(N)
"""

def fast_string_build(n: int) -> str:
    """Builds a string of length N in O(N) time instead of O(N^2)."""
    parts = []
    for i in range(n):
        parts.append('a')
    return "".join(parts)


# ==============================================================================
# [PIT-05] The O(N) list.pop(0) / list.insert(0) Queue Trap (TLE)
# ==============================================================================
"""
Trap:
    Using a standard Python `list` as a queue via `q.pop(0)` or `q.insert(0, val)`.
    `list.pop(0)` removes the first element and shifts all remaining N - 1 elements
    one position to the left in memory, costing O(N) time per operation.
    In a BFS on 10^5 nodes, this results in O(N^2) = 10^10 operations (TLE).

How To Fix It:
    Always use `from collections import deque`.
    `dq.popleft()` and `dq.appendleft()` are strictly O(1).
"""

def demonstrate_queue_performance():
    dq = deque()
    for i in range(1000):
        dq.append(i)
    # Fast O(1) popleft
    return dq.popleft()


# ==============================================================================
# [PIT-06] The 2D Matrix Shallow Copy Trap (`[[0]*M]*N`) (WA)
# ==============================================================================
"""
Trap:
    Creating a 2D matrix using:
        `grid = [[0] * M] * N`
    This creates ONE single list `[0] * M` and duplicates its REFERENCE N times!
    Modifying `grid[0][0] = 5` will simultaneously set `grid[1][0] = 5`,
    `grid[2][0] = 5`, etc., corrupting the entire grid!

How To Fix It:
    Use a list comprehension to instantiate a distinct row list on every iteration:
        `grid = [[0] * M for _ in range(N)]`
"""

def create_safe_matrix(rows: int, cols: int, fill=0) -> list:
    """Instantiates a 2D grid where every row is an independent list in memory."""
    return [[fill] * cols for _ in range(rows)]


# ==============================================================================
# [PIT-07] Bitwise Operator Precedence Traps (WA)
# ==============================================================================
"""
Trap:
    Arithmetic operators (+, -) have HIGHER precedence than bitwise shifts (<<, >>).
    Comparison operators (==, !=, <) have HIGHER precedence than bitwise AND/OR (&, |).
    Examples:
        `1 << n - 1`   evaluates as `1 << (n - 1)`, NOT `(1 << n) - 1`!
        `x & 1 == 0`   evaluates as `x & (1 == 0)` which is `x & False` -> 0!
        `x & y == target` evaluates as `x & (y == target)`!

How To Fix It:
    ALWAYS enclose bitwise operations in explicit parentheses:
        `((1 << n) - 1)`
        `(x & 1) == 0`
        `(x & y) == target`
"""

def is_even_bitwise(x: int) -> bool:
    # Explicit parentheses are mandatory!
    return (x & 1) == 0

def mask_all_ones(n: int) -> int:
    # Generates (2^n - 1)
    return (1 << n) - 1


# ==============================================================================
# [PIT-08] Lexicographical Number Comparison Trap (WA)
# ==============================================================================
"""
Trap:
    Comparing numerical inputs while they are still stored as strings:
        `"100" < "20"` evaluates to `True`!
    Because Python compares strings character-by-character from left to right,
    and `'1' < '2'`.

How To Fix It:
    Always cast string inputs to integers before comparisons:
        `int("100") < int("20")` -> `False`
    If sorting strings by numeric value without casting the whole string:
        `arr.sort(key=int)`
"""

def sort_numeric_strings(arr: list) -> list:
    """Sorts string representations of numbers by their numeric value."""
    return sorted(arr, key=int)


# ==============================================================================
# [PIT-09] Modifying Collections While Iterating (RTE / Skipped Elements)
# ==============================================================================
"""
Trap:
    1. In sets / dicts: Mutating size during iteration raises:
       `RuntimeError: Set changed size during iteration`
    2. In lists: Removing an element while iterating shifts subsequent elements,
       causing the loop index to advance past the neighbor without inspecting it!

How To Fix It:
    - Iterate over a shallow copy of the collection:
      `for item in list(my_set):`
      `for key in list(my_dict.keys()):`
    - Or build a filtered container using a list comprehension:
      `arr = [x for x in arr if condition(x)]`
"""

def remove_negatives_safely(arr: list) -> list:
    """Safely filters items without mutation-skipping bugs."""
    return [x for x in arr if x >= 0]


# ==============================================================================
# [PIT-10] Slicing Inside Loops Causing Hidden O(K) Copies (TLE)
# ==============================================================================
"""
Trap:
    Inside a loop over length N, writing `window = arr[i:i+k]`.
    Python list slicing makes a SHALLOW COPY of the elements.
    If K is large (e.g., K = 50,000) and N = 100,000:
    The loop performs 100,000 copies of size 50,000 = 5 * 10^9 operations (TLE)!

How To Fix It:
    - Use index pointers instead of copying sublists.
    - Update running metrics (sum, Counter, hash) incrementally when entering
      and leaving the window in O(1) instead of re-slicing and re-aggregating.
"""

def running_window_sum(arr: list, k: int) -> list:
    """Maintains sliding window sum incrementally in O(1) per step with zero slicing."""
    curr = sum(arr[:k])
    res = [curr]
    for i in range(k, len(arr)):
        curr += arr[i] - arr[i - k]  # O(1) update
        res.append(curr)
    return res


# ==============================================================================
# [PIT-11] Slow Standard I/O Overhead on 10^5+ Lines (TLE)
# ==============================================================================
"""
Trap:
    Calling `input()` and `print()` 100,000+ times.
    `input()` performs single-character reads and strips newlines, while `print()`
    flushes and formats strings repeatedly, creating massive runtime overhead.

How To Fix It:
    Use fast I/O:
    ```python
    import sys
    # Read entire input at once:
    input_data = sys.stdin.read().split()
    
    # Fast output:
    sys.stdout.write("\\n".join(output_lines) + "\\n")
    ```
"""

def parse_all_integers(stream: str) -> list:
    """Simulates ultra-fast bulk integer parsing from stdin."""
    return list(map(int, stream.split()))


# ==============================================================================
# [PIT-12] Python's Round-Half-To-Even "Banker's Rounding" (WA)
# ==============================================================================
"""
Trap:
    In Python 3, `round(x)` implements Banker's Rounding (rounds half-integers
    to the nearest EVEN integer):
        `round(2.5) == 2`  (rounds DOWN to nearest even!)
        `round(3.5) == 4`  (rounds UP to nearest even!)
    Competitive programming problems often specify standard arithmetic rounding
    (round half UP away from zero, so 2.5 should become 3).

How To Fix It:
    For positive numbers: `int(x + 0.5)`
    Or using `decimal`:
    ```python
    from decimal import Decimal, ROUND_HALF_UP
    val = int(Decimal(str(x)).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
    ```
"""

def standard_round_half_up(x: float) -> int:
    """Standard competitive programming half-up rounding (2.5 -> 3, 3.5 -> 4)."""
    if x >= 0:
        return int(x + 0.5)
    else:
        return int(x - 0.5)


# ==============================================================================
# SELF-TEST SUITE
# ==============================================================================
if __name__ == '__main__':
    # Test PIT-01
    assert demonstrate_recursion_fix() == 2500
    
    # Test PIT-02
    sd = SafeDict()
    sd[42] = "answer"
    assert sd[42] == "answer"
    assert 42 in sd
    assert sd.get(100, -1) == -1
    
    # Test PIT-03
    assert demonstrate_precision_pitfall() == 10**18
    assert math.isqrt(10**18) == 10**9
    
    # Test PIT-04
    assert len(fast_string_build(100)) == 100
    
    # Test PIT-05
    assert demonstrate_queue_performance() == 0
    
    # Test PIT-06
    mat = create_safe_matrix(3, 3, 0)
    mat[0][0] = 99
    assert mat[1][0] == 0, "Matrix rows must be independent!"
    
    # Test PIT-07
    assert is_even_bitwise(4) is True
    assert is_even_bitwise(5) is False
    assert mask_all_ones(3) == 7
    
    # Test PIT-08
    assert sort_numeric_strings(["100", "20", "5"]) == ["5", "20", "100"]
    
    # Test PIT-09
    assert remove_negatives_safely([-2, 5, -1, 3]) == [5, 3]
    
    # Test PIT-10
    assert running_window_sum([1, 2, 3, 4], 2) == [3, 5, 7]
    
    # Test PIT-11
    assert parse_all_integers("10 20  30\n40") == [10, 20, 30, 40]
    
    # Test PIT-12
    # Demonstrates distinction: round(2.5) == 2, but standard_round_half_up(2.5) == 3
    assert round(2.5) == 2
    assert standard_round_half_up(2.5) == 3
    assert standard_round_half_up(3.5) == 4

    print("ALL PitfallsAndErrors.py tests passed successfully!")
