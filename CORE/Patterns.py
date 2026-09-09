"""
================================================================================
Patterns.py - Competitive Programming Problem Patterns & Archetypes
================================================================================
A master reference of fundamental problem-solving patterns and algorithmic
archetypes. These patterns bridge the gap between recognizing a problem statement
and choosing the correct data structure and algorithmic approach.

TABLE OF CONTENTS:
--------------------------------------------------------------------------------
1.  [PAT-01] Two Pointers (Opposite Ends & Same Direction)
2.  [PAT-02] Sliding Window (Fixed & Dynamic / Shrinkable)
3.  [PAT-03] Prefix Sums & Difference Arrays (Range Query & Range Update)
4.  [PAT-04] Monotonic Stack & Queue (Next Greater Element & Window Extremum)
5.  [PAT-05] Binary Search on Answer / Monotonic Predicate
6.  [PAT-06] Fast Breadth-First Search (BFS) on Graphs & Grids
7.  [PAT-07] Depth-First Search (DFS) & Backtracking State Space Tree
8.  [PAT-08] Disjoint Set Union (DSU / Union-Find)
9.  [PAT-09] Greedy Choice Property with Sorting / Heap Scheduling
10. [PAT-10] Coordinate Compression & Value Discretization
11. [PAT-11] Frequency & Hash Invariant Matching
12. [PAT-12] Matrix Grid Traversal & Directional Offsets
================================================================================
"""

import math
from collections import deque, defaultdict, Counter
import bisect


# ==============================================================================
# [PAT-01] Two Pointers (Opposite Ends & Same Direction)
# ==============================================================================
"""
Pattern Name:
    Two Pointers (Bidirectional & Forward/Fast-Slow)

Recognition Cues:
    - Array is sorted (or can be sorted).
    - Looking for pairs, triplets, or subsegments satisfying sum/difference criteria.
    - Symmetrical reduction (e.g. palindrome checks, container with most water).

Mental Model:
    Instead of nested loops O(N^2), use two index variables (left and right).
    Based on the comparison of the current state with the target, monotonically
    advance one of the pointers, pruning entire subproblems in O(N) total steps.

Core Variations:
    1. Opposite Ends: left = 0, right = N - 1. Move inwards based on condition.
    2. Same Direction (Fast/Slow): slow tracks write position, fast reads.

Edge Cases:
    - Even vs. odd length sequences.
    - Duplicate elements causing duplicate count inflation.
"""

def two_sum_sorted(arr: list, target: int) -> tuple:
    """Finds 0-based indices of two numbers in sorted array that sum to target, or None."""
    left, right = 0, len(arr) - 1
    while left < right:
        curr_sum = arr[left] + arr[right]
        if curr_sum == target:
            return (left, right)
        elif curr_sum < target:
            left += 1
        else:
            right -= 1
    return None

def remove_duplicates_in_place(arr: list) -> int:
    """Modifies sorted array in-place to contain unique elements, returns new length."""
    if not arr:
        return 0
    slow = 0
    for fast in range(1, len(arr)):
        if arr[fast] != arr[slow]:
            slow += 1
            arr[slow] = arr[fast]
    return slow + 1


# ==============================================================================
# [PAT-02] Sliding Window (Fixed & Dynamic / Shrinkable)
# ==============================================================================
"""
Pattern Name:
    Sliding Window (Fixed-Size & Dynamic-Size)

Recognition Cues:
    - Continuous subarrays or substrings.
    - Asking for minimum/maximum length subarray with sum >= K or <= K.
    - Maximum elements in every window of size K.

Mental Model:
    Maintain a window [left, right] and an aggregated state (sum, character frequency).
    Expand right to explore new elements. When the window becomes invalid, advance left
    to shrink the window until validity is restored.

Time Complexity:
    O(N) amortized because each pointer moves at most N times.
"""

def max_sum_fixed_window(arr: list, k: int) -> int:
    """Computes maximum sum of any contiguous subarray of fixed length k."""
    if len(arr) < k:
        return 0
    window_sum = sum(arr[:k])
    max_val = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        if window_sum > max_val:
            max_val = window_sum
    return max_val

def min_subarray_len_with_sum(arr: list, target: int) -> int:
    """Finds minimal length of subarray whose sum is >= target, or 0 if none exists."""
    left = 0
    curr_sum = 0
    min_len = float('inf')
    
    for right in range(len(arr)):
        curr_sum += arr[right]
        while curr_sum >= target:
            min_len = min(min_len, right - left + 1)
            curr_sum -= arr[left]
            left += 1
            
    return min_len if min_len != float('inf') else 0


# ==============================================================================
# [PAT-03] Prefix Sums & Difference Arrays (Range Query & Range Update)
# ==============================================================================
"""
Pattern Name:
    Prefix Sums (Range Queries) & Difference Arrays (Batch Range Updates)

Recognition Cues:
    - Multiple queries asking for sum of subarray A[L..R] in O(1).
    - Multiple operations adding a value V across range [L..R], querying final array.

Mental Model:
    1. Prefix Sum: P[i] = A[0] + ... + A[i - 1].
       Sum of A[L..R] = P[R + 1] - P[L].
    2. Difference Array: D[i] = A[i] - A[i - 1].
       Adding V to [L..R] is accomplished by:
       D[L] += V
       D[R + 1] -= V
       Reconstructing the array is simply the prefix sum of D.
"""

class PrefixSum1D:
    def __init__(self, arr: list):
        self.pref = [0] * (len(arr) + 1)
        for i, val in enumerate(arr):
            self.pref[i + 1] = self.pref[i] + val

    def query(self, l: int, r: int) -> int:
        """Returns sum of elements in 0-indexed range [l, r] inclusive in O(1)."""
        return self.pref[r + 1] - self.pref[l]

class DifferenceArray1D:
    def __init__(self, size: int):
        self.size = size
        self.diff = [0] * (size + 2)

    def add_range(self, l: int, r: int, val: int):
        """Adds val to all elements in range [l, r] inclusive in O(1)."""
        self.diff[l] += val
        self.diff[r + 1] -= val

    def build(self) -> list:
        """Constructs final array via cumulative sum in O(N)."""
        res = [0] * self.size
        curr = 0
        for i in range(self.size):
            curr += self.diff[i]
            res[i] = curr
        return res


# ==============================================================================
# [PAT-04] Monotonic Stack & Queue (Next Greater Element & Window Extremum)
# ==============================================================================
"""
Pattern Name:
    Monotonic Stack & Monotonic Deque

Recognition Cues:
    - Next greater or next smaller element for each index in an array.
    - Largest rectangle in histogram / stock span.
    - Sliding window minimum or maximum in O(N) total time.

Mental Model:
    Maintain a stack or deque whose values are strictly monotonic (increasing/decreasing).
    Before inserting element x, pop all elements that violate monotonicity.
    Those popped elements have found their "next boundary" (x).
"""

def next_greater_elements(arr: list) -> list:
    """Returns an array where result[i] is the next greater element to the right of arr[i], or -1."""
    n = len(arr)
    result = [-1] * n
    stack = []  # stores indices
    
    for i in range(n):
        while stack and arr[i] > arr[stack[-1]]:
            idx = stack.pop()
            result[idx] = arr[i]
        stack.append(i)
        
    return result

def sliding_window_maximum(arr: list, k: int) -> list:
    """Computes maximum element in every sliding window of size k in O(N)."""
    dq = deque()  # stores indices, maintains descending order of values
    res = []
    
    for i in range(len(arr)):
        # Remove elements outside current window
        if dq and dq[0] < i - k + 1:
            dq.popleft()
            
        # Pop smaller elements from back
        while dq and arr[dq[-1]] <= arr[i]:
            dq.pop()
            
        dq.append(i)
        
        # Window is fully formed
        if i >= k - 1:
            res.append(arr[dq[0]])
            
    return res


# ==============================================================================
# [PAT-05] Binary Search on Answer / Monotonic Predicate
# ==============================================================================
"""
Pattern Name:
    Binary Search on Monotonic Predicate ("Search on Answer")

Recognition Cues:
    - Problem asks for "minimum maximum", "maximum minimum", or optimal threshold.
    - Direct calculation is intractable, but testing if a candidate answer X
      is feasible (`can_achieve(X) -> bool`) is easy and monotonic:
      False, False, ..., False, True, True, True (or vice-versa).

Mental Model:
    Define low and high bounds for the answer.
    Mid = (low + high) // 2.
    Evaluate feasibility via helper function `is_valid(mid)`.
    Narrow search space by half each iteration: O(log(range) * cost_of_check).
"""

def binary_search_answer(low: int, high: int, is_valid_fn) -> int:
    """Finds minimal integer in [low, high] satisfying is_valid_fn(x) == True."""
    ans = high
    while low <= high:
        mid = (low + high) // 2
        if is_valid_fn(mid):
            ans = mid
            high = mid - 1  # Try to find a smaller valid value
        else:
            low = mid + 1   # Must be larger
    return ans


# ==============================================================================
# [PAT-06] Fast Breadth-First Search (BFS) on Graphs & Grids
# ==============================================================================
"""
Pattern Name:
    Queue-Based Breadth-First Search (BFS) for Shortest Path

Recognition Cues:
    - Shortest path or minimum steps in unweighted graph or 2D grid.
    - Level-order distance propagation (infection, fire, multi-source flood fill).

Mental Model:
    Use `collections.deque` as a FIFO queue.
    Maintain `dist` dictionary or 2D matrix initialized to -1 / infinity.
    Push start node with dist = 0. Enqueue unvisited neighbors with dist = curr + 1.
"""

def bfs_shortest_path_grid(grid: list, start: tuple, target: tuple) -> int:
    """Finds shortest distance from start (r,c) to target (r,c) avoiding obstacle '1's."""
    rows, cols = len(grid), len(grid[0])
    sr, sc = start
    tr, tc = target
    
    if grid[sr][sc] == 1 or grid[tr][tc] == 1:
        return -1
    if start == target:
        return 0
        
    q = deque([(sr, sc, 0)])
    visited = {(sr, sc)}
    
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        r, c, d = q.popleft()
        if (r, c) == (tr, tc):
            return d
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                q.append((nr, nc, d + 1))
                
    return -1


# ==============================================================================
# [PAT-07] Depth-First Search (DFS) & Backtracking State Space Tree
# ==============================================================================
"""
Pattern Name:
    Backtracking State Space Traversal

Recognition Cues:
    - Generate all permutations, subsets, combinations, or board configurations (N-Queens).
    - Constraints are small (N <= 20).

Mental Model:
    State tree exploration:
    1. Base case: If state is complete, record solution and return.
    2. Recursive step: Iterate over choices.
       - Check if choice is valid (prune invalid branches early!).
       - Make choice (modify state).
       - Recurse deeper.
       - Undo choice (backtrack to restore state).
"""

def generate_subsets(nums: list) -> list:
    """Generates all 2^N subsets of a list using backtracking."""
    subsets = []
    
    def backtrack(index, current_path):
        subsets.append(list(current_path))
        for i in range(index, len(nums)):
            current_path.append(nums[i])
            backtrack(i + 1, current_path)
            current_path.pop()  # Backtrack step
            
    backtrack(0, [])
    return subsets


# ==============================================================================
# [PAT-08] Disjoint Set Union (DSU / Union-Find)
# ==============================================================================
"""
Pattern Name:
    Disjoint Set Union (DSU) with Path Compression & Union by Rank

Recognition Cues:
    - Dynamic connectivity: nodes being connected incrementally.
    - Kruskal's Minimum Spanning Tree algorithm.
    - Cycle detection in undirected graphs.
    - Group count / connected component sizes.

Mental Model:
    Each element belongs to a tree whose root represents the group.
    `find(x)`: Recursively follows parent pointers to root, flattening the tree (path compression).
    `union(x, y)`: Merges smaller tree under root of larger tree (union by rank/size).
    Amortized time per operation: O(alpha(N)) ≈ O(1).
"""

class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n
        self.num_sets = n

    def find(self, i: int) -> int:
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])  # Path compression
        return self.parent[i]

    def union(self, i: int, j: int) -> bool:
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i == root_j:
            return False  # Already in same set
        
        # Union by size
        if self.size[root_i] < self.size[root_j]:
            root_i, root_j = root_j, root_i
        self.parent[root_j] = root_i
        self.size[root_i] += self.size[root_j]
        self.num_sets -= 1
        return True


# ==============================================================================
# [PAT-09] Greedy Choice Property with Sorting / Heap Scheduling
# ==============================================================================
"""
Pattern Name:
    Interval Scheduling / Greedy Activity Selection

Recognition Cues:
    - Non-overlapping interval selection (meeting rooms, tasks, activity selection).
    - Maximizing number of completed tasks given start and end times.

Mental Model:
    Sort intervals by their END TIME.
    Greedily pick the interval that finishes earliest to leave the maximum possible
    room for subsequent intervals.
"""

def max_non_overlapping_intervals(intervals: list) -> int:
    """Finds maximum number of mutually non-overlapping intervals [start, end]."""
    if not intervals:
        return 0
    # Sort by end time
    sorted_intervals = sorted(intervals, key=lambda x: x[1])
    count = 0
    last_end = float('-inf')
    
    for start, end in sorted_intervals:
        if start >= last_end:
            count += 1
            last_end = end
            
    return count


# ==============================================================================
# [PAT-10] Coordinate Compression & Value Discretization
# ==============================================================================
"""
Pattern Name:
    Coordinate Compression (Rank Discretization)

Recognition Cues:
    - Coordinates or values can be up to 10^9 or 10^18, but the number of elements N <= 10^5.
    - Need to index elements into an array, Fenwick Tree, or Segment Tree where
      indices must be compact integers [0..N - 1].

Mental Model:
    Extract all distinct coordinates, sort them, and map each value to its rank
    using binary search (`bisect_left`).
"""

def coordinate_compress(values: list) -> tuple:
    """Maps arbitrary values into compact 0-based rank indices [0..U - 1].
    Returns (compressed_list, rank_to_original_mapping).
    """
    unique_sorted = sorted(set(values))
    val_to_rank = {v: i for i, v in enumerate(unique_sorted)}
    compressed = [val_to_rank[v] for v in values]
    return compressed, unique_sorted


# ==============================================================================
# [PAT-11] Frequency & Hash Invariant Matching
# ==============================================================================
"""
Pattern Name:
    Frequency Invariant / Target Difference Matching

Recognition Cues:
    - Subarrays with exact sum K (Prefix Sum + Hash Map).
    - Pair differences: A[i] - A[j] = K.
    - Anagram groupings: strings with identical character counts.

Mental Model:
    Transform the condition `A[i] - A[j] = K` into `A[j] = A[i] - K`.
    Store seen elements in a hash set or frequency map and check membership in O(1).
"""

def count_subarrays_with_sum(arr: list, target: int) -> int:
    """Counts number of continuous subarrays that sum to target in O(N)."""
    prefix_counts = defaultdict(int)
    prefix_counts[0] = 1  # Base case for subarray starting at index 0
    
    curr_sum = 0
    total_count = 0
    
    for x in arr:
        curr_sum += x
        # curr_sum - prev_sum = target  =>  prev_sum = curr_sum - target
        total_count += prefix_counts[curr_sum - target]
        prefix_counts[curr_sum] += 1
        
    return total_count


# ==============================================================================
# [PAT-12] Matrix Grid Traversal & Directional Offsets
# ==============================================================================
"""
Pattern Name:
    Standard 4-Way & 8-Way Direction Vector Grid Navigation

Recognition Cues:
    - Navigating 2D boards, matrices, mazes.
    - Avoiding 4 separate copy-pasted boundary check blocks.

Mental Model:
    Define neighbor offsets as a compact list of tuples:
    `DIRS_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]`
    `DIRS_8 = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]`
    Iterate over (dr, dc) with standard bounds check `0 <= nr < R and 0 <= nc < C`.
"""

DIRS_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIRS_8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

def get_valid_neighbors(r: int, c: int, rows: int, cols: int, diagonal: bool = False):
    """Yields valid in-bound neighbor coordinates."""
    directions = DIRS_8 if diagonal else DIRS_4
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc


# ==============================================================================
# SELF-TEST SUITE
# ==============================================================================
if __name__ == '__main__':
    # Test PAT-01
    assert two_sum_sorted([2, 7, 11, 15], 9) == (0, 1)
    test_arr = [1, 1, 2, 2, 3]
    assert remove_duplicates_in_place(test_arr) == 3
    assert test_arr[:3] == [1, 2, 3]
    
    # Test PAT-02
    assert max_sum_fixed_window([2, 1, 5, 1, 3, 2], 3) == 9
    assert min_subarray_len_with_sum([2, 3, 1, 2, 4, 3], 7) == 2
    
    # Test PAT-03
    ps = PrefixSum1D([10, 20, 30, 40, 50])
    assert ps.query(1, 3) == 90  # 20 + 30 + 40
    diff = DifferenceArray1D(5)
    diff.add_range(1, 3, 10)
    diff.add_range(2, 4, 5)
    assert diff.build() == [0, 10, 15, 15, 5]
    
    # Test PAT-04
    assert next_greater_elements([4, 5, 2, 25]) == [5, 25, 25, -1]
    assert sliding_window_maximum([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    
    # Test PAT-05
    # Find minimal x such that x * x >= 50
    assert binary_search_answer(1, 100, lambda x: x * x >= 50) == 8
    
    # Test PAT-06
    maze = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]
    assert bfs_shortest_path_grid(maze, (0, 0), (2, 2)) == 4
    
    # Test PAT-07
    assert len(generate_subsets([1, 2, 3])) == 8
    
    # Test PAT-08
    dsu = DSU(5)
    assert dsu.union(0, 1) is True
    assert dsu.union(1, 2) is True
    assert dsu.find(0) == dsu.find(2)
    assert dsu.union(0, 2) is False  # Already connected
    assert dsu.num_sets == 3
    
    # Test PAT-09
    assert max_non_overlapping_intervals([[1, 4], [2, 3], [3, 5], [7, 9]]) == 3
    
    # Test PAT-10
    compressed, orig_map = coordinate_compress([1000, 5, 1000, 250])
    assert compressed == [2, 0, 2, 1]
    assert orig_map == [5, 250, 1000]
    
    # Test PAT-11
    assert count_subarrays_with_sum([1, 1, 1], 2) == 2
    assert count_subarrays_with_sum([1, -1, 0], 0) == 3
    
    # Test PAT-12
    neighbors = list(get_valid_neighbors(0, 0, 3, 3))
    assert set(neighbors) == {(0, 1), (1, 0)}

    print("ALL Patterns.py tests passed successfully!")
