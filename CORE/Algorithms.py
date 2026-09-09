"""
================================================================================
000_Algorithms.py - Competitive Programming Algorithm Notebook
================================================================================
A curated, reusable reference of algorithmic techniques, mathematical shortcuts,
and problem-solving patterns extracted from 139 HackerRank solutions.

Organized for quick retrieval during Codeforces, LeetCode, and HackerRank contests.
Every algorithm is directly grounded in problems from this repository.

TABLE OF CONTENTS:
--------------------------------------------------------------------------------
1.  [ALG-01] Substring Counting Without Generation (The Minion Game Pattern)
2.  [ALG-02] Greedy Boundary Deque Simulation (Piling Up! Pattern)
3.  [ALG-03] Cartesian Product Optimization & Search Space Bounding
4.  [ALG-04] Frequency Disparity Isolation via Sum-Set Math (Captain's Room)
5.  [ALG-05] Fast Prime Verification via O(sqrt(N)) 6k +/- 1 Trial Division
6.  [ALG-06] Overlapping Regex Pattern Search via Zero-Width Positive Lookahead
7.  [ALG-07] Combinatorial Probability via Complementary Counting
8.  [ALG-08] Alternating & Consecutive Repetition Detection (Lookahead Chains)
9.  [ALG-09] Run-Length Encoding via itertools.groupby
10. [ALG-10] Breadth-First Search (BFS) Tree Level-Order Traversal
11. [ALG-11] Tree Height & Depth via Recursive Divide-and-Conquer (DFS)
12. [ALG-12] 3D Vector Geometry: Dihedral (Torsional) Angle Between Planes
13. [ALG-13] Right-Triangle Median Invariance Theorem (Thales' Circumcenter)
14. [ALG-14] Demlo Numbers & Repunit Arithmetic for Constant-Memory Sequences
15. [ALG-15] Matrix Serialization & Boundary-Preserving Regex Decoding
16. [ALG-16] 2D Stencil / Sliding-Window Convolution (Hourglass Scan)
17. [ALG-17] Modular Exponentiation & Coprime Calculations
18. [ALG-18] In-Place Sorted Linked-List Deduplication
================================================================================
"""

import math
import cmath
import re
import itertools
from collections import deque, Counter, defaultdict
from functools import reduce


# ==============================================================================
# [ALG-01] Substring Counting Without Generation (The Minion Game Pattern)
# ==============================================================================
"""
Algorithm Name:
    O(N) Suffix-Contribution Substring Counting

What It Does:
    Calculates the total count of valid substrings starting with specific
    character types (e.g., vowels vs. consonants) in O(N) time and O(1) space,
    completely bypassing the O(N^2) or O(N^3) cost of explicit substring generation.

When To Recognize / Use:
    - Problem asks to count or score all substrings starting/ending with a character.
    - String length N >= 10^5 (where N^2 generates 10^10 substrings and causes TLE/MLE).
    - Scoring games based on substring start positions.

Core Idea:
    In any string S of length L, a character at index i is the starting character
    of exactly (L - i) distinct substrings:
    S[i:i+1], S[i:i+2], ..., S[i:L].
    Instead of generating strings, accumulate the scalar contribution (L - i).

Edge Cases & Limitations:
    - Requires case-normalization if the input contains mixed-case characters.
    - If duplicates are not counted independently, suffix contribution alone does
      not suffice (requires Suffix Automaton or Trie).

Repository References:
    - PYTHON/0054_The-Minion-Game.py (Q54)
"""

def count_substrings_by_start(s: str, target_charset: set) -> int:
    """Computes total count of substrings starting with any character in target_charset."""
    total_len = len(s)
    return sum(total_len - i for i, char in enumerate(s) if char in target_charset)


# ==============================================================================
# [ALG-02] Greedy Boundary Deque Simulation (Piling Up! Pattern)
# ==============================================================================
"""
Algorithm Name:
    Two-Pointer / Deque Outer-Boundary Greedy Reduction

What It Does:
    Determines whether an array can be completely emptied by repeatedly picking
    elements from either the left or right boundary such that the sequence of
    chosen elements is non-increasing.

When To Recognize / Use:
    - Elements can only be selected from the current left or right ends of a sequence.
    - Must stack, reduce, or sort elements subject to monotonic constraints.
    - Can be modeled as a two-pointer scan meeting in the center.

Core Idea:
    At each step, examine both ends: left and right.
    Always pick the LARGER valid element among (left, right) that is <= current_top.
    Greedily consuming the larger available element preserves maximum leeway for
    subsequent steps. If neither end is <= current_top, stacking is impossible.

Edge Cases & Limitations:
    - All elements identical (trivially True).
    - strictly increasing or strictly decreasing arrays (always True).
    - V-shaped arrays (decreasing then increasing) are solvable; inverted V-shaped
      (increasing then decreasing) always fail.

Repository References:
    - PYTHON/0076_Piling-Up.py (Q76)
"""

def can_stack_from_ends(arr: list) -> bool:
    """Verifies if an array can be reduced from ends to form a non-increasing stack."""
    dq = deque(arr)
    current_top = float('inf')
    
    while dq:
        # Pick the larger candidate that is <= current_top
        left, right = dq[0], dq[-1]
        if left >= right:
            candidate = left
            from_left = True
        else:
            candidate = right
            from_left = False
            
        if candidate <= current_top:
            current_top = candidate
            dq.popleft() if from_left else dq.pop()
        else:
            # The larger end failed; try the smaller end
            smaller = right if from_left else left
            if smaller <= current_top:
                current_top = smaller
                dq.pop() if from_left else dq.popleft()
            else:
                return False
    return True


# ==============================================================================
# [ALG-03] Cartesian Product Optimization & Search Space Bounding
# ==============================================================================
"""
Algorithm Name:
    Modular State Compression Cartesian Search

What It Does:
    Finds the maximum value of sum(X_i^2) % M where exactly one element X_i
    is chosen from each of K lists.

When To Recognize / Use:
    - Selecting one element per list across K independent candidate lists.
    - Target metric involves modular arithmetic: f(x1, x2, ..., xk) % M.
    - Number of lists K is small (e.g., K <= 7) while list sizes N_i <= 7.

Core Idea:
    Pre-process each element by computing (x^2) % M and deduplicating values within
    each list using a set. This shrinks the search space dramatically before feeding
    into itertools.product(*processed_lists).

Edge Cases & Limitations:
    - Note that (sum % M) is NOT distributive over max, meaning greedy picking
      per list is incorrect: max(a % M) + max(b % M) != max((a + b) % M).
      Full combinatorial search or DP is mandatory.

Repository References:
    - PYTHON/0020_Maximize-It.py (Q20)
"""

def maximize_modular_sum(lists: list, m: int) -> int:
    """Finds max(sum(x^2 for x in choice) % m) by picking one x per list."""
    # Pre-reduce states: only unique squares mod m matter per list
    reduced_lists = [set((x ** 2) % m for x in sublist) for sublist in lists]
    return max(sum(comb) % m for comb in itertools.product(*reduced_lists))


# ==============================================================================
# [ALG-04] Frequency Disparity Isolation via Sum-Set Math (Captain's Room)
# ==============================================================================
"""
Algorithm Name:
    Algebraic Frequency Isolation (The Set-Sum Outlier Formula)

What It Does:
    Identifies the unique single element that appears exactly once in an array
    where every other distinct element appears exactly K times.
    Time Complexity: O(N), Space Complexity: O(U) where U is unique elements.

When To Recognize / Use:
    - Every group has known uniform size K, except for one group of size 1.
    - Standard XOR reduction fails because K can be odd (e.g., K = 5).
    - Counter hash map requires O(U) space and higher constant factor overhead.

Core Idea:
    Let S be the sum of all elements in the input list.
    Let U be the sum of the unique elements (i.e., sum(set(list))).
    Each non-target element is multiplied by K in S, but only once in U.
    Therefore:
        K * U - S = (K - 1) * target
        target = (K * U - S) // (K - 1)

Edge Cases & Limitations:
    - K must be strictly greater than 1.
    - Memory for set(array) must fit in memory; for streaming input with O(1) space,
      bit-frequency array mod K must be used instead.

Repository References:
    - PYTHON/0081_The-Captains-Room.py (Q81)
"""

def find_single_outlier(arr: list, k: int) -> int:
    """Finds the element appearing once when all others appear k times."""
    unique_sum = sum(set(arr))
    total_sum = sum(arr)
    return (k * unique_sum - total_sum) // (k - 1)


# ==============================================================================
# [ALG-05] Fast Prime Verification via O(sqrt(N)) 6k +/- 1 Trial Division
# ==============================================================================
"""
Algorithm Name:
    Wheel-Factorized (6k +/- 1) Trial Division Primality Test

What It Does:
    Determines if an integer N is prime in O(sqrt(N)) operations with 3x speedup
    over naive trial division by skipping all multiples of 2 and 3.

When To Recognize / Use:
    - Fast single-number primality checking up to N <= 10^14.
    - When Sieve of Eratosthenes memory O(N) is prohibited because N is large.

Core Idea:
    All primes greater than 3 can be expressed in the form 6k - 1 or 6k + 1.
    After verifying that N is not divisible by 2 or 3, we test divisors i and i + 2
    while incrementing i by 6 up to sqrt(N).

Edge Cases & Limitations:
    - N <= 1 is not prime.
    - N = 2, 3 are prime.
    - Loop condition must check i * i <= N.

Repository References:
    - 30 DAYS OF CODE/Day-25-Running-Time-and-Complexity.py (Q65)
"""

def is_prime(n: int) -> bool:
    """Returns True if n is prime, False otherwise."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


# ==============================================================================
# [ALG-06] Overlapping Regex Pattern Search via Zero-Width Positive Lookahead
# ==============================================================================
"""
Algorithm Name:
    Zero-Width Lookahead Non-Consuming Regex Matcher

What It Does:
    Extracts all occurrences (including overlapping matches) and their exact
    start/end indices across a string.

When To Recognize / Use:
    - Standard regex `re.findall` or `re.finditer` fails because it consumes
      matched characters, skipping overlapping substrings (e.g. searching 'aa' in 'aaa').
    - Finding all starting indices of substring matches.

Core Idea:
    A positive lookahead assertion `(?=pattern)` tests if the pattern matches
    immediately ahead without advancing the regex match pointer.
    By wrapping the pattern inside a capturing group within the lookahead:
        `rf'(?=({re.escape(sub)}))'`
    Match objects report the exact start index `m.start()` while `m.group(1)` yields
    the matched string.

Edge Cases & Limitations:
    - `m.end()` on a zero-width match returns `m.start()`, not the end of group 1.
      The actual end of the matched token is `m.start() + len(m.group(1)) - 1`.

Repository References:
    - PYTHON/0027_Find-a-string.py (Q27)
    - PYTHON/0116_Re-start-Re-end.py (Q116)
    - PYTHON/0132_Group-Groups-Groupdict.py (Q132)
"""

def find_overlapping_occurrences(text: str, pattern: str) -> list:
    """Returns list of (start_index, end_index) for all occurrences including overlaps."""
    regex = re.compile(rf'(?=({re.escape(pattern)}))')
    matches = []
    for m in regex.finditer(text):
        start = m.start()
        end = start + len(m.group(1)) - 1
        matches.append((start, end))
    return matches


# ==============================================================================
# [ALG-07] Combinatorial Probability via Complementary Counting
# ==============================================================================
"""
Algorithm Name:
    Complementary Combinatorial Probability (At Least One Property)

What It Does:
    Calculates the exact probability that a randomly chosen subset of size K
    contains AT LEAST ONE target element from a population of size N.

When To Recognize / Use:
    - Problems stating "Find the probability that at least one of the selected..."
    - Direct calculation requires complex sum of combinations across sizes 1..K.

Core Idea:
    P(at least one target) = 1.0 - P(zero targets).
    P(zero targets) = C(non_targets_count, K) / C(total_count, K).
    Computing 1 - (non_targets_count choose K) / (N choose K) takes O(1) or O(K) time.

Edge Cases & Limitations:
    - If K > non_targets_count, P(zero targets) = 0.0, so probability is 1.0.
    - If target elements count == 0, probability is 0.0.

Repository References:
    - PYTHON/0113_Iterables-and-Iterators.py (Q113)
"""

def probability_at_least_one(total_n: int, target_count: int, k: int) -> float:
    """Computes probability of selecting >= 1 target when picking k items from total_n."""
    non_target_count = total_n - target_count
    if k > total_n or target_count == 0:
        return 0.0
    if non_target_count < k:
        return 1.0
    
    total_combinations = math.comb(total_n, k)
    non_target_combinations = math.comb(non_target_count, k)
    return 1.0 - (non_target_combinations / total_combinations)


# ==============================================================================
# [ALG-08] Alternating & Consecutive Repetition Detection (Lookahead Chains)
# ==============================================================================
"""
Algorithm Name:
    Backreference Lookahead Pattern Validator

What It Does:
    Validates complex repetition invariants (e.g. at most one alternating repetitive
    digit pair `121` or no 4 consecutive repeated characters `1111`) across
    formatted or hyphenated tokens.

When To Recognize / Use:
    - Validating credit cards, postal codes, ID formats with dynamic repeat constraints.
    - Condition involves looking ahead by fixed strides (e.g., character at i equals i + 2).

Core Idea:
    - Alternating digit pair (e.g. `121` or `505`):
      `r'(\d)(?=\d\1)'` matches any digit that is followed by any digit then itself.
    - Consecutive runs of 4 identical digits across optional separators:
      `r'(\d)(-?\1){3}'` matches 4 occurrences of the same captured group.

Edge Cases & Limitations:
    - Always pre-validate character set and overall length before applying repeat filters.

Repository References:
    - PYTHON/0115_Validating-Postal-Codes-Stub.py (Q115)
    - PYTHON/0125_Validating-Credit-Card-Numbers.py (Q125)
    - PYTHON/0134_Validating-UID.py (Q134)
"""

def count_alternating_repetitive_digit_pairs(s: str) -> int:
    """Counts instances of d1 X d1 in string (e.g., '12145' -> 1)."""
    return len(re.findall(r'(\d)(?=\d\1)', s))

def has_four_consecutive_repeated_digits(s: str) -> bool:
    """Checks for 4 identical consecutive digits with optional hyphens."""
    return bool(re.search(r'(\d)(-?\1){3}', s))


# ==============================================================================
# [ALG-09] Run-Length Encoding via itertools.groupby
# ==============================================================================
"""
Algorithm Name:
    Iterator-Based Run-Length Encoding (RLE)

What It Does:
    Compresses consecutive duplicate elements into (count, key) pairs in a single
    streaming pass of O(N) time and O(1) auxiliary memory.

When To Recognize / Use:
    - Run-length encoding or decoding.
    - Streak calculations (e.g., longest streak of wins, max consecutive ones).
    - Parsing character blocks in strings or streams.

Core Idea:
    `itertools.groupby(iterable)` groups contiguous identical elements.
    Evaluating `(len(list(group)), key)` yields the run length and item.

Edge Cases & Limitations:
    - `groupby` only groups CONTIGUOUS items. Non-adjacent identical items produce
      separate groups.
    - The `group` iterator must be consumed or converted before the outer loop advances.

Repository References:
    - PYTHON/0097_Compress-the-String.py (Q97)
"""

def run_length_encode(data: str) -> list:
    """Returns list of (count, character) tuples for consecutive blocks."""
    return [(len(list(group)), key) for key, group in itertools.groupby(data)]


# ==============================================================================
# [ALG-10] Breadth-First Search (BFS) Tree Level-Order Traversal
# ==============================================================================
"""
Algorithm Name:
    FIFO Queue Level-Order Binary Tree Traversal

What It Does:
    Visits every node of a tree level-by-level from left to right in O(N) time
    and O(W) space (where W is maximum level width).

When To Recognize / Use:
    - Problem asks to print nodes level by level.
    - Shortest path search in unweighted graph/tree.
    - Level-based aggregation (min/max/average per depth).

Core Idea:
    Initialize a `collections.deque` with the root. While the queue is non-empty,
    pop from the left, process the node, and push its non-null left and right children.

Edge Cases & Limitations:
    - Empty tree (root is None) must return immediately.

Repository References:
    - 30 DAYS OF CODE/Day-23-BST-Level-Order-Traversal.cpp (Q63)
    - 30 DAYS OF CODE/Day-18-Queues-and-Stacks.py (Q53)
"""

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def bfs_level_order(root: TreeNode) -> list:
    """Returns a flat list of node values visited in level order."""
    if not root:
        return []
    
    result = []
    q = deque([root])
    while q:
        curr = q.popleft()
        result.append(curr.val)
        if curr.left:
            q.append(curr.left)
        if curr.right:
            q.append(curr.right)
    return result


# ==============================================================================
# [ALG-11] Tree Height & Depth via Recursive Divide-and-Conquer (DFS)
# ==============================================================================
"""
Algorithm Name:
    Recursive Post-Order Maximum Depth / Height Calculation

What It Does:
    Computes the height of a binary tree (number of edges on longest root-to-leaf path)
    in O(N) time and O(H) call stack memory.

When To Recognize / Use:
    - Calculating tree height, diameter, balance factors.
    - Depth-dependent aggregations.

Core Idea:
    height(None) = -1 (definition: leaf node has height 0 = 1 + max(-1, -1)).
    height(node) = 1 + max(height(node.left), height(node.right)).

Edge Cases & Limitations:
    - If height is defined as number of NODES, base case for None is 0.
      HackerRank defines height as number of EDGES, so None returns -1.
    - Deep trees can exceed Python's recursion limit `sys.setrecursionlimit(2000)`.

Repository References:
    - 30 DAYS OF CODE/Day-22-Binary-Search-Trees.py (Q62)
"""

def get_tree_height(root: TreeNode) -> int:
    """Computes tree height in terms of edges (-1 for empty, 0 for single leaf)."""
    if root is None:
        return -1
    return 1 + max(get_tree_height(root.left), get_tree_height(root.right))


# ==============================================================================
# [ALG-12] 3D Vector Geometry: Dihedral (Torsional) Angle Between Planes
# ==============================================================================
"""
Algorithm Name:
    Dihedral (Torsional) Angle via Cross & Dot Products

What It Does:
    Computes the angle between two planes formed by 4 points A, B, C, D in 3D space.

When To Recognize / Use:
    - 3D computational geometry, robotics, molecular structure calculations.
    - Finding the angle between two intersecting triangular facets.

Core Idea:
    Given points A, B, C, D:
    1. Form displacement vectors:
       b1 = B - A
       b2 = C - B
       b3 = D - C
    2. Compute plane normal vectors using cross products:
       n1 = b1 x b2
       n2 = b2 x b3
    3. The angle phi between the normals satisfies:
       cos(phi) = (n1 . n2) / (|n1| * |n2|)
       phi = acos(clamp(cos(phi), -1.0, 1.0)) in radians.
       Convert to degrees via math.degrees(phi).

Edge Cases & Limitations:
    - Floating point rounding can produce cos(phi) = 1.0000000002 which causes
      math.acos() to throw ValueError; always clamp the dot product quotient to [-1.0, 1.0].
    - Collinear points produce zero-length normal vectors (division by zero).

Repository References:
    - PYTHON/0121_Class-2-Find-the-Torsional-Angle.py (Q121)
"""

class Point3D:
    def __init__(self, x: float, y: float, z: float):
        self.x, self.y, self.z = x, y, z

    def sub(self, other: 'Point3D') -> 'Point3D':
        return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def dot(self, other: 'Point3D') -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: 'Point3D') -> 'Point3D':
        return Point3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def magnitude(self) -> float:
        return math.sqrt(self.dot(self))

def calculate_torsional_angle(a: Point3D, b: Point3D, c: Point3D, d: Point3D) -> float:
    """Returns dihedral angle in degrees between plane (A,B,C) and plane (B,C,D)."""
    b1 = b.sub(a)
    b2 = c.sub(b)
    b3 = d.sub(c)
    
    n1 = b1.cross(b2)
    n2 = b2.cross(b3)
    
    cos_phi = n1.dot(n2) / (n1.magnitude() * n2.magnitude())
    cos_phi = max(-1.0, min(1.0, cos_phi))  # Guard against precision drift
    return math.degrees(math.acos(cos_phi))


# ==============================================================================
# [ALG-13] Right-Triangle Median Invariance Theorem (Thales' Circumcenter)
# ==============================================================================
"""
Algorithm Name:
    Right-Triangle Hypotenuse Median Angle Property

What It Does:
    Calculates angle MBC where M is the midpoint of hypotenuse AC in right triangle
    ABC (with right angle at B), given legs AB and BC, in O(1) time.

When To Recognize / Use:
    - Geometry problems involving median to the hypotenuse.

Core Idea:
    By Thales' Theorem, the circumcenter of any right triangle is exactly the midpoint
    M of the hypotenuse AC.
    Therefore, the distance from M to all three vertices is identical:
        AM = BM = CM
    Since BM = CM, triangle BMC is isosceles with base BC.
    Therefore, angle MBC == angle MCB == angle ACB.
    In right triangle ABC:
        tan(angle ACB) = AB / BC
        angle MBC = atan2(AB, BC)

Edge Cases & Limitations:
    - Legs must be positive non-zero floats. Use math.atan2(AB, BC) to handle quadrant safely.

Repository References:
    - PYTHON/0084_Find-Angle-MBC.py (Q84)
"""

def angle_mbc_degrees(ab: float, bc: float) -> int:
    """Computes angle MBC in degrees (rounded to nearest integer) given legs ab, bc."""
    rad = math.atan2(ab, bc)
    return round(math.degrees(rad))


# ==============================================================================
# [ALG-14] Demlo Numbers & Repunit Arithmetic for Constant-Memory Sequences
# ==============================================================================
"""
Algorithm Name:
    Pure-Arithmetic Repunit & Demlo Number Generation

What It Does:
    Generates single-digit repeat lines and palindromic numeric triangles
    using exact integer arithmetic with ZERO string manipulation and O(1) space.

When To Recognize / Use:
    - Problems explicitly disallowing strings, loops, or multiple statements.
    - Generating sequence:
      Row 1: 1
      Row 2: 22
      Row 3: 333
      Or Palindromic:
      Row 1: 1
      Row 2: 121
      Row 3: 12321

Core Idea:
    The repunit of length i is R_i = (10^i - 1) // 9.
    1. Repeated digit i:
       i * R_i = i * (10^i - 1) // 9
    2. Demlo Palindromic number (12...i...21):
       (R_i)^2 = ((10^i - 1) // 9) ** 2

Edge Cases & Limitations:
    - Demlo squaring property holds perfectly for 1 <= i <= 9.
      At i >= 10, digit carries break the pure palindrome sequence.

Repository References:
    - PYTHON/0010_Triangle-Quest.py (Q10)
    - PYTHON/0109_Triangle-Quest-2.py (Q109)
"""

def generate_repdigit(i: int) -> int:
    """Generates digit i repeated i times (e.g. i=3 -> 333) via integer math."""
    return i * (10 ** i - 1) // 9

def generate_demlo_palindrome(i: int) -> int:
    """Generates 12...i...21 (e.g. i=3 -> 12321) via integer math (1 <= i <= 9)."""
    return ((10 ** i - 1) // 9) ** 2


# ==============================================================================
# [ALG-15] Matrix Serialization & Boundary-Preserving Regex Decoding
# ==============================================================================
"""
Algorithm Name:
    Matrix Transpose Serialization & Inter-Alphanumeric Normalization

What It Does:
    Decodes an N x M grid read column-wise into a continuous stream, then replaces
    all sequences of non-alphanumeric characters occurring BETWEEN alphanumeric
    characters with a single space, while strictly preserving leading and trailing symbols.

When To Recognize / Use:
    - 2D grid text decoding (column-major transposition).
    - Sanitizing symbol clusters between text tokens without trimming ends.

Core Idea:
    1. Transpose: `"".join("".join(col) for col in zip(*matrix))`
    2. Regex lookaround assertion:
       `re.sub(r'(?<=\w)[!@#$%& ]+(?=\w)', ' ', decoded_text)`
       Positive lookbehind `(?<=\w)` ensures an alphanumeric precedes the symbols.
       Positive lookahead `(?=\w)` ensures an alphanumeric follows the symbols.

Edge Cases & Limitations:
    - Non-alphanumeric characters at the very beginning or very end of the string
      are untouched because they fail the lookbehind or lookahead condition.

Repository References:
    - PYTHON/0120_Matrix-Script.py (Q120)
"""

def decode_matrix_script(matrix: list) -> str:
    """Transposes matrix column-wise and normalizes internal symbol clusters."""
    # Transpose rows into columns
    raw_stream = "".join("".join(column) for column in zip(*matrix))
    # Replace non-alphanumeric clusters located strictly between alphanumeric chars
    return re.sub(r'(?<=\w)[!@#$%& ]+(?=\w)', ' ', raw_stream)


# ==============================================================================
# [ALG-16] 2D Stencil / Sliding-Window Convolution (Hourglass Scan)
# ==============================================================================
"""
Algorithm Name:
    2D Fixed-Stencil Maximum Convolution

What It Does:
    Scans a 2D matrix with a fixed geometric mask (stencil) and finds the maximum
    convolution sum in O(R * C) time and O(1) auxiliary space.

When To Recognize / Use:
    - Finding local geometric patterns (crosses, hourglasses, plus-signs) in grids.
    - Grid dimensions up to 1000 x 1000.

Core Idea:
    Iterate anchor (r, c) over valid bounds: 0 <= r <= R - height and 0 <= c <= C - width.
    Extract the exact mask values directly using index offsets.

Edge Cases & Limitations:
    - Matrix values can be negative! Initial maximum must be -infinity, NOT 0.

Repository References:
    - PYTHON/0045_Day-11-2D-Arrays.py (Q45)
"""

def max_hourglass_sum(grid: list) -> int:
    """Computes maximum 3x3 hourglass sum in a 2D grid."""
    max_sum = float('-inf')
    for r in range(len(grid) - 2):
        for c in range(len(grid[0]) - 2):
            # Top 3 + Center 1 + Bottom 3
            current = (
                grid[r][c] + grid[r][c + 1] + grid[r][c + 2]
                + grid[r + 1][c + 1]
                + grid[r + 2][c] + grid[r + 2][c + 1] + grid[r + 2][c + 2]
            )
            if current > max_sum:
                max_sum = current
    return max_sum


# ==============================================================================
# [ALG-17] Modular Exponentiation & Coprime Calculations
# ==============================================================================
"""
Algorithm Name:
    Built-In Modular Exponentiation & Functional Rational Reduction

What It Does:
    Computes (base^exp) % mod in O(log exp) time using Python's 3-argument pow(),
    and reduces rational products using functools.reduce and math.gcd.

When To Recognize / Use:
    - Cryptography, hash computations, combinatorial combinations mod 10^9 + 7.
    - Multiplying lists of fractions and returning the reduced numerator and denominator.

Core Idea:
    Python's `pow(a, b, m)` implements binary exponentiation directly in C,
    never computing the massive intermediate integer a^b.
    For rational fractions, multiply all numerators and denominators, then divide
    both by their greatest common divisor: `math.gcd(num, den)`.

Edge Cases & Limitations:
    - pow(a, -1, m) computes the modular inverse if a and m are coprime (Python 3.8+).

Repository References:
    - PYTHON/0008_Power-Mod-Power.py (Q8)
    - PYTHON/0118_Reduce-Function.py (Q118)
"""

def modular_pow(base: int, exp: int, mod: int) -> int:
    """Fast binary exponentiation: (base^exp) % mod."""
    return pow(base, exp, mod)

def reduce_fraction_product(numerators: list, denominators: list) -> tuple:
    """Multiplies lists of numerators and denominators, returning reduced (num, den)."""
    total_num = reduce(lambda x, y: x * y, numerators)
    total_den = reduce(lambda x, y: x * y, denominators)
    g = math.gcd(total_num, total_den)
    return total_num // g, total_den // g


# ==============================================================================
# [ALG-18] In-Place Sorted Linked-List Deduplication
# ==============================================================================
"""
Algorithm Name:
    Pointer-Rewiring Duplicate Removal on Sorted Singly-Linked Lists

What It Does:
    Removes all duplicate elements from an already-sorted linked list in O(N) time
    and O(1) auxiliary space by adjusting pointer links.

When To Recognize / Use:
    - Node structures with single `.next` pointers.
    - List is pre-sorted.

Core Idea:
    Traverse with a single pointer `curr`. If `curr.next` has `curr.val == curr.next.val`,
    bypass the duplicate: `curr.next = curr.next.next`.
    Only advance `curr = curr.next` when the next node has a DIFFERENT value.

Edge Cases & Limitations:
    - Head is None or single element (returns head directly).
    - Long runs of duplicates (e.g. 1 -> 1 -> 1 -> 2): requires `while` without advancing.

Repository References:
    - 30 DAYS OF CODE/Day-24-More-Linked-Lists.cpp (Q64)
    - 30 DAYS OF CODE/Day-15-Linked-List.py (Q50)
"""

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def remove_duplicates_sorted_list(head: ListNode) -> ListNode:
    """Removes duplicate values from a sorted linked list in-place."""
    curr = head
    while curr and curr.next:
        if curr.val == curr.next.val:
            curr.next = curr.next.next
        else:
            curr = curr.next
    return head


# ==============================================================================
# SELF-TEST SUITE
# ==============================================================================
if __name__ == '__main__':
    # Test ALG-01
    assert count_substrings_by_start("BANANA", {'A', 'E', 'I', 'O', 'U'}) == 9
    
    # Test ALG-02
    assert can_stack_from_ends([4, 3, 2, 1, 3, 4]) is True
    assert can_stack_from_ends([1, 3, 2]) is False
    
    # Test ALG-03
    test_lists = [[5, 4], [7, 8, 9], [5, 7, 8, 9, 10]]
    assert maximize_modular_sum(test_lists, 1000) == 206
    
    # Test ALG-04
    assert find_single_outlier([1, 2, 3, 1, 2, 3, 1, 2, 3, 8], 3) == 8
    
    # Test ALG-05
    assert is_prime(29) is True
    assert is_prime(1) is False
    assert is_prime(4) is False
    
    # Test ALG-06
    matches = find_overlapping_occurrences("aaadaa", "aa")
    assert matches == [(0, 1), (1, 2), (4, 5)]
    
    # Test ALG-07
    p = probability_at_least_one(4, 2, 2)
    assert abs(p - 0.8333333333) < 1e-5
    
    # Test ALG-08
    assert count_alternating_repetitive_digit_pairs("121426") == 1
    assert has_four_consecutive_repeated_digits("5123-4567-8912-3455") is False
    assert has_four_consecutive_repeated_digits("5133-3367-8912-3455") is True
    
    # Test ALG-09
    assert run_length_encode("1222311") == [(1, '1'), (3, '2'), (1, '3'), (2, '1')]
    
    # Test ALG-13
    assert angle_mbc_degrees(10, 10) == 45
    
    # Test ALG-14
    assert generate_repdigit(4) == 4444
    assert generate_demlo_palindrome(3) == 12321
    
    # Test ALG-15
    matrix_sample = [
        "Tsi",
        "h%x",
        "i #",
        "sM ",
        "$a ",
        "#t%",
        "ir!"
    ]
    assert decode_matrix_script(matrix_sample) == "This is Matrix#  %!"
    
    # Test ALG-16
    grid_sample = [
        [1, 1, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0],
        [0, 0, 2, 4, 4, 0],
        [0, 0, 0, 2, 0, 0],
        [0, 0, 1, 2, 4, 0]
    ]
    assert max_hourglass_sum(grid_sample) == 19
    
    # Test ALG-17
    assert modular_pow(3, 4, 5) == 1
    assert reduce_fraction_product([1, 2], [2, 4]) == (1, 4)

    print("ALL Algorithms.py tests passed successfully!")
