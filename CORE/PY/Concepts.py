"""
================================================================================
000_Concepts.py - Competitive Programming Core Concept Reference
================================================================================
A curated reference of deep, reusable programming concepts, Python runtime
mechanics, and optimization principles discovered from 139 HackerRank solutions.

Organized for quick study and long-term retention before competing in Codeforces,
LeetCode, and HackerRank contests.

TABLE OF CONTENTS:
--------------------------------------------------------------------------------
1.  [CON-01] Mutable Default Argument Trap (Early Binding & State Leakage)
2.  [CON-02] Function Decorators & Input/Output Transformation Wrappers
3.  [CON-03] Lexicographical Multi-Criteria Tuple Sorting
4.  [CON-04] Regex Lookaround Assertions: Non-Consuming Lookaheads & Lookbehinds
5.  [CON-05] High-Performance Specialized Collections (deque, Counter, defaultdict, OrderedDict)
6.  [CON-06] Python Set Algebra & In-Place Mutation Mechanics
7.  [CON-07] Dynamic Method Dispatch via Reflection (getattr)
8.  [CON-08] Operator Overloading & Custom Class Arithmetic via Dunder Methods
9.  [CON-09] Memory-Efficient Combinatorial Generators (itertools)
10. [CON-10] NumPy Vectorized Array Operations & Axis Semantics
11. [CON-11] Fast Stream Ingestion & EOF Handling (sys.stdin.read)
12. [CON-12] Recursive Tree Traversal & Accumulative Depth Tracking
13. [CON-13] Short-Circuit Boolean Evaluation (any & all with Generators)
================================================================================
"""

import sys
import math
import re
import itertools
from collections import deque, Counter, defaultdict, OrderedDict
from functools import reduce


# ==============================================================================
# [CON-01] Mutable Default Argument Trap (Early Binding & State Leakage)
# ==============================================================================
"""
Concept Name:
    Mutable Default Arguments & Definition-Time Binding

Simple Explanation:
    In Python, default parameter expressions are evaluated ONCE at function definition
    time, NOT each time the function is called.
    If you use a mutable object (like a list, dictionary, or set) as a default argument:
        `def append_to(element, target_list=[]):`
    that single list object is shared across ALL subsequent invocations of the function.

Why It Matters for Competitive Programming:
    In recursion, tree traversals, and backtracking (e.g. DFS, pathfinding),
    passing `path=[]` or `visited={}` as a default argument causes state to bleed
    across separate test cases or recursive branches, leading to bizarre bugs and WA.

When Is It Useful:
    - Recognizing and fixing hidden state-leak bugs in starter code.
    - Intentionally caching state across function calls without global variables
      (memoization trick).

Python Idiom / Solution:
    Always use `None` as the sentinel default value, and create a fresh instance
    inside the function body.

Related Repository Problems:
    - PYTHON/0123_Default-Arguments.py (Q123)
"""

def safe_accumulator(item, collection=None):
    """Correct pattern: instantiate a fresh mutable container on each call."""
    if collection is None:
        collection = []
    collection.append(item)
    return collection

def bugged_accumulator(item, collection=[]):
    """The trap: 'collection' persists between calls!"""
    collection.append(item)
    return collection


# ==============================================================================
# [CON-02] Function Decorators & Input/Output Transformation Wrappers
# ==============================================================================
"""
Concept Name:
    Function Decorators, Closures, and Higher-Order Wrappers

Simple Explanation:
    A decorator is a higher-order function that takes another function as input,
    extends or modifies its behavior without modifying its source code, and returns
    the wrapped callable.

Why It Matters for Competitive Programming:
    - Memoization: Attaching `@functools.lru_cache(None)` turns exponential O(2^N)
      recursive functions into polynomial O(N) dynamic programming without rewriting.
    - Input Normalization: Pre-processing formatted input arrays (e.g. standardizing
      mobile prefixes '+91 XXXXX XXXXX' or names 'Mr. / Ms.') before passing to logic.
    - Custom Sorters: Pre-sorting inputs using a decorator wrapper.

When Is It Useful:
    - When multiple functions share identical preprocessing, validation, or caching logic.
    - Modularizing competitive programming pipelines.

Python Idiom:
    ```python
    def my_decorator(func):
        def wrapper(*args, **kwargs):
            # Pre-processing
            modified_args = [modify(a) for a in args]
            result = func(*modified_args, **kwargs)
            # Post-processing
            return result
        return wrapper
    ```

Related Repository Problems:
    - PYTHON/0122_Decorators-2-Name-Directory.py (Q122)
    - PYTHON/0126_Decorators-2-Name-Directory.py (Q126)
    - PYTHON/0128_Standardize-Mobile-Number-Using-Dec.py (Q128)
"""

def mobile_number_standardizer(func):
    """Decorator that standardizes 10-digit/11-digit/12-digit Indian phone numbers."""
    def wrapper(numbers):
        formatted = []
        for n in numbers:
            # Extract last 10 digits
            clean = n[-10:]
            formatted.append(f"+91 {clean[:5]} {clean[5:]}")
        return func(formatted)
    return wrapper

@mobile_number_standardizer
def sort_phone_numbers(numbers):
    return sorted(numbers)


# ==============================================================================
# [CON-03] Lexicographical Multi-Criteria Tuple Sorting
# ==============================================================================
"""
Concept Name:
    Multi-Key Lexicographical Tuple Comparison (Timsort Optimization)

Simple Explanation:
    Python compares tuples position-by-position:
        (a1, b1, c1) < (a2, b2, c2)
    It compares a1 vs a2; only if they are equal does it compare b1 vs b2, and so on.
    We can map arbitrary priority rules (e.g., lowercase first, then uppercase,
    then odd numbers, then even numbers) into a tuple key function.

Why It Matters for Competitive Programming:
    - Completely eliminates the need to write custom comparator classes or implement
      complex multiple sorting passes.
    - Executes at full C-speed using Python's native Timsort algorithm.
    - Handles tie-breakers naturally and stably.

When Is It Useful:
    - Multi-level sorting: Sort by score descending (-score), then by name ascending (name).
    - Custom character sorting rules (e.g. ginortS: lower < upper < odd < even).
    - Athlete sorting across a specific matrix column attribute.

Python Idiom:
    ```python
    # Sort students by highest score, tie-break by youngest age, then by name alphabetically:
    students.sort(key=lambda s: (-s['score'], s['age'], s['name']))
    ```

Related Repository Problems:
    - PYTHON/0077_Company-Logo.py (Q77)
    - PYTHON/0078_ginortS.py (Q78)
    - PYTHON/0139_Athlete-Sort.py (Q139)
"""

def ginorts_sort_key(char: str) -> tuple:
    """Encodes custom sorting priority:
    1. Lowercase letters (priority 1)
    2. Uppercase letters (priority 2)
    3. Odd digits (priority 3)
    4. Even digits (priority 4)
    5. Alphabetical value tie-breaker
    """
    if char.islower():
        return (1, char)
    elif char.isupper():
        return (2, char)
    elif char.isdigit():
        if int(char) % 2 != 0:
            return (3, char)  # Odd digit
        else:
            return (4, char)  # Even digit
    return (5, char)

def ginorts_sort(s: str) -> str:
    """Sorts string according to the ginortS rules."""
    return "".join(sorted(s, key=ginorts_sort_key))


# ==============================================================================
# [CON-04] Regex Lookaround Assertions: Non-Consuming Lookaheads & Lookbehinds
# ==============================================================================
"""
Concept Name:
    Zero-Width Lookaround Assertions (Lookahead & Lookbehind)

Simple Explanation:
    Lookaround assertions are zero-width matches: they check whether a pattern
    exists immediately before or after the current position, WITHOUT including those
    characters in the match or advancing the regex engine's cursor.
    - Positive Lookahead:  `(?=pattern)`   - Next characters must match pattern
    - Negative Lookahead:  `(?!pattern)`   - Next characters must NOT match pattern
    - Positive Lookbehind: `(?<=pattern)`  - Preceding characters must match pattern
    - Negative Lookbehind: `(?<!pattern)`  - Preceding characters must NOT match pattern

Why It Matters for Competitive Programming:
    1. Overlapping Matches: Normal regex consumes characters; `(?=(pattern))` allows
       finding all overlapping occurrences.
    2. Context-Dependent Substitution: Replacing symbols only when flanked by spaces
       or alphanumerics without replacing the boundaries themselves.
    3. Concurrency / Multi-Condition Validation: Validating that a string satisfies
       multiple independent rules in a single regex:
       `^(?=.*[A-Z]{2,})(?=.*\d{3,})(?!.*(.).*\1)[A-Za-z0-9]{10}$` (Validating UID).

Related Repository Problems:
    - PYTHON/0115_Validating-Postal-Codes-Stub.py (Q115)
    - PYTHON/0116_Re-start-Re-end.py (Q116)
    - PYTHON/0120_Matrix-Script.py (Q120)
    - PYTHON/0125_Validating-Credit-Card-Numbers.py (Q125)
    - PYTHON/0131_Regex-Substitution.py (Q131)
    - PYTHON/0134_Validating-UID.py (Q134)
"""

def substitute_logical_operators(text: str) -> str:
    """Replaces '&&' with 'and' and '||' with 'or' strictly when flanked by spaces."""
    # Lookbehind ensures leading space; lookahead ensures trailing space
    text = re.sub(r'(?<= )&&(?= )', 'and', text)
    text = re.sub(r'(?<= )\|\|(?= )', 'or', text)
    return text


# ==============================================================================
# [CON-05] High-Performance Specialized Collections (deque, Counter, defaultdict, OrderedDict)
# ==============================================================================
"""
Concept Name:
    Specialized C-Accelerated Data Structures in `collections`

Simple Explanation:
    Python's standard `list` is a dynamic array. Operations at the beginning:
    `list.pop(0)` or `list.insert(0, val)` take O(N) time because all N elements
    must be shifted in memory.
    The `collections` module provides C-level data structures optimized for specific tasks:
    1. `deque`: Double-ended queue with O(1) appends and pops at BOTH ends.
    2. `Counter`: Hash map designed for frequency counting, multiset arithmetic
       (union |, intersection &, sum +, subtraction -).
    3. `defaultdict`: Hash map that automatically initializes missing keys using
       a factory function (e.g. `list`, `int`, `set`).
    4. `OrderedDict`: Hash map preserving insertion order with O(1) `move_to_end()`
       (vital for LRU Cache implementations).

Why It Matters for Competitive Programming:
    - Using `list.pop(0)` inside a loop of size 10^5 results in 10^10 operations (TLE).
      Using `deque.popleft()` reduces this to 10^5 operations (0.05s).
    - `Counter` drastically simplifies anagram, frequency, and multiset problems.

Related Repository Problems:
    - PYTHON/0032_Collections-Counter.py (Q32)
    - PYTHON/0067_DefaultDict-Tutorial.py (Q67)
    - PYTHON/0075_Collections-deque.py (Q75)
    - PYTHON/0079_Collections-OrderedDict.py (Q79)
    - PYTHON/0080_Word-Order.py (Q80)
"""

def frequency_analysis(items: list) -> tuple:
    """Demonstrates Counter multiset operations and defaultdict grouping."""
    counts = Counter(items)
    # Most common elements: list of (item, frequency) sorted descending
    top_two = counts.most_common(2)
    
    # Inverted mapping: frequency -> list of items
    grouped = defaultdict(list)
    for item, freq in counts.items():
        grouped[freq].append(item)
        
    return top_two, dict(grouped)


# ==============================================================================
# [CON-06] Python Set Algebra & In-Place Mutation Mechanics
# ==============================================================================
"""
Concept Name:
    Mathematical Set Algebra, Hash Collisions & In-Place Mutations

Simple Explanation:
    Python `set` is implemented as an open-addressing hash table with average O(1)
    insertion, deletion, and lookup.
    Sets support mathematical operators and equivalent in-place mutation methods:
    - Union:               `A | B`    (in-place: `A.update(B)` or `A |= B`)
    - Intersection:        `A & B`    (in-place: `A.intersection_update(B)` or `A &= B`)
    - Difference:          `A - B`    (in-place: `A.difference_update(B)` or `A -= B`)
    - Symmetric Diff:      `A ^ B`    (in-place: `A.symmetric_difference_update(B)` or `A ^= B`)

Why It Matters for Competitive Programming:
    - In-place mutation methods (like `A.difference_update(B)`) avoid allocating
      a new set object in memory, saving significant memory and execution time.
    - Crucial difference between `.remove(x)` and `.discard(x)`:
      - `s.remove(x)` raises `KeyError` if x is not present.
      - `s.discard(x)` is a safe no-op if x is not present.
    - Subset checks: `A <= B` (issubset) and `A < B` (strict subset).

Related Repository Problems:
    - PYTHON/0060_Introduction-to-Sets.py (Q60)
    - PYTHON/0074_Symmetric-Difference.py (Q74)
    - PYTHON/0083_Set-union-Operation.py (Q83)
    - PYTHON/0087_Set-add.py (Q87)
    - PYTHON/0089_Set-discard-remove-pop.py (Q89)
    - PYTHON/0091_Set-difference-Operation.py (Q91)
    - PYTHON/0092_Set-intersection-Operation.py (Q92)
    - PYTHON/0093_Set-symmetric_difference-Operation.py (Q93)
    - PYTHON/0094_Set-Mutations.py (Q94)
    - PYTHON/0095_Check-Subset.py (Q95)
    - PYTHON/0096_Check-Strict-Superset.py (Q96)
"""

def execute_set_command(base_set: set, command: str, other_set: set) -> None:
    """Executes dynamic set mutation safely using getattr."""
    if hasattr(base_set, command):
        getattr(base_set, command)(other_set)


# ==============================================================================
# [CON-07] Dynamic Method Dispatch via Reflection (getattr)
# ==============================================================================
"""
Concept Name:
    Dynamic Attribute Reflection (`getattr`, `hasattr`)

Simple Explanation:
    `getattr(object, attribute_name_string)` retrieves an attribute or method from
    an object dynamically at runtime using its string name.

Why It Matters for Competitive Programming:
    HackerRank and competitive programming tasks frequently present input formats like:
        insert 0 5
        append 10
        remove 5
        pop
        reverse
    Instead of writing 10 tedious `if cmd == 'insert': ... elif cmd == 'append': ...`
    branches, one line handles all commands:
        `getattr(my_list, cmd)(*args)`

When Is It Useful:
    - Command-driven simulation problems.
    - Dynamic dispatch based on input tokens.

Related Repository Problems:
    - PYTHON/0016_Lists.py (Q16)
    - PYTHON/0089_Set-discard-remove-pop.py (Q89)
    - PYTHON/0094_Set-Mutations.py (Q94)
"""

def execute_list_commands(commands: list) -> list:
    """Executes a list of string commands dynamically on a Python list."""
    target = []
    for line in commands:
        cmd, *args = line.split()
        args = list(map(int, args))
        if cmd == "print":
            pass  # Output step
        else:
            getattr(target, cmd)(*args)
    return target


# ==============================================================================
# [CON-08] Operator Overloading & Custom Class Arithmetic via Dunder Methods
# ==============================================================================
"""
Concept Name:
    Operator Overloading via Python Magic (Dunder) Methods

Simple Explanation:
    Python allows user-defined classes to intercept built-in operators (+, -, *, /, abs)
    by defining double-underscore ("dunder") methods:
    - `__add__(self, other)`:      `+` operator
    - `__sub__(self, other)`:      `-` operator
    - `__mul__(self, other)`:      `*` operator
    - `__truediv__(self, other)`:  `/` operator
    - `__abs__(self)`:             `abs()` function
    - `__str__(self)`:             `str()` / `print()` output

Why It Matters for Competitive Programming:
    - Writing clean, expressive geometry (2D/3D vectors, points, rays).
    - Complex number arithmetic, fractional mathematics, or custom modular arithmetic
      (e.g., a `ModInt` class that automatically computes `(a + b) % MOD` on every `+`).

Related Repository Problems:
    - PYTHON/0114_Classes-Dealing-with-Complex-Number.py (Q114)
    - PYTHON/0121_Class-2-Find-the-Torsional-Angle.py (Q121)
"""

class ComplexNumber:
    """Custom complex number implementing full operator overloading."""
    def __init__(self, real: float, imag: float):
        self.real = real
        self.imag = imag

    def __add__(self, other: 'ComplexNumber') -> 'ComplexNumber':
        return ComplexNumber(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other: 'ComplexNumber') -> 'ComplexNumber':
        return ComplexNumber(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other: 'ComplexNumber') -> 'ComplexNumber':
        # (a + bi)(c + di) = (ac - bd) + (ad + bc)i
        return ComplexNumber(
            self.real * other.real - self.imag * other.imag,
            self.real * other.imag + self.imag * other.real
        )

    def __abs__(self) -> float:
        return math.hypot(self.real, self.imag)

    def __str__(self) -> str:
        sign = "+" if self.imag >= 0 else "-"
        return f"{self.real:.2f} {sign} {abs(self.imag):.2f}i"


# ==============================================================================
# [CON-09] Memory-Efficient Combinatorial Generators (itertools)
# ==============================================================================
"""
Concept Name:
    Combinatorics Stream Processing via `itertools`

Simple Explanation:
    `itertools` provides memory-efficient, C-implemented combinatorial iterators:
    1. `itertools.product(*iterables)`: Cartesian product (equivalent to nested for-loops).
    2. `itertools.permutations(iterable, r)`: Ordered arrangements without repetition.
    3. `itertools.combinations(iterable, r)`: Unordered subsets of size r without repetition.
    4. `itertools.combinations_with_replacement(iterable, r)`: Subsets allowing duplicate items.

Why It Matters for Competitive Programming:
    - Generates items one by one lazily. If N=20 and r=10, there are 184,756 combinations.
      Generating a list consumes memory; iterating via a generator uses O(r) memory.
    - Always output combinations in lexicographical sort order (if the input was sorted).

Related Repository Problems:
    - PYTHON/0020_Maximize-It.py (Q20)
    - PYTHON/0047_itertools-product.py (Q47)
    - PYTHON/0059_itertools-permutations.py (Q59)
    - PYTHON/0082_itertools-combinations.py (Q82)
    - PYTHON/0088_itertools-combinations_with_replacement.py (Q88)
"""

def generate_sorted_combinations(s: str, k: int) -> list:
    """Generates all combinations up to size k in strict lexicographical order."""
    chars = sorted(s)
    result = []
    for length in range(1, k + 1):
        for comb in itertools.combinations(chars, length):
            result.append("".join(comb))
    return result


# ==============================================================================
# [CON-10] NumPy Vectorized Array Operations & Axis Semantics
# ==============================================================================
"""
Concept Name:
    Array Vectorization & Multi-Dimensional Axis Semantics

Simple Explanation:
    NumPy executes operations over contiguous blocks of memory at C-speed,
    bypassing Python bytecode interpretation.
    The `axis` parameter defines the direction of reduction:
    - `axis=0`: Operates ALONG rows (collapses vertically down columns).
      Result length equals number of columns.
    - `axis=1`: Operates ALONG columns (collapses horizontally across rows).
      Result length equals number of rows.
    - `axis=None`: Operates over the entire flattened array (returns scalar).

Why It Matters for Competitive Programming:
    - Matrix multiplication (`np.dot`, `np.matmul`), inner/outer products,
      determinants (`np.linalg.det`), and polynomial evaluations (`np.polyval`)
      run in milliseconds even on 500x500 matrices where pure Python loops time out.

Related Repository Problems:
    - PYTHON/0018_Zeros-and-Ones.py (Q18)
    - PYTHON/0019_Eye-and-Identity.py (Q19)
    - PYTHON/0106_Min-and-Max.py (Q106)
    - PYTHON/0110_Sum-and-Prod.py (Q110)
    - PYTHON/0111_Inner-and-Outer.py (Q111)
    - PYTHON/0112_Concatenate.py (Q112)
    - PYTHON/0127_Min-and-Max.py (Q127)
    - PYTHON/0137_Polynomials.py (Q137)
    - PYTHON/0138_Linear-Algebra.py (Q138)
    - PYTHON/0140_Dot-and-Cross.py (Q140)
    - PYTHON/0141_Array-Mathematics.py (Q141)
    - PYTHON/0142_Floor-Ceil-and-Rint.py (Q142)
"""

# Pure Python equivalent demonstrating axis=0 vs axis=1 reduction semantics:
def min_along_axis_0(matrix: list) -> list:
    """Computes minimum along axis=0 (column minimums) without numpy."""
    return [min(col) for col in zip(*matrix)]

def min_along_axis_1(matrix: list) -> list:
    """Computes minimum along axis=1 (row minimums) without numpy."""
    return [min(row) for row in matrix]


# ==============================================================================
# [CON-11] Fast Stream Ingestion & EOF Handling (sys.stdin.read)
# ==============================================================================
"""
Concept Name:
    Single-Syscall Stream Ingestion & Graceful EOF Handling

Simple Explanation:
    `sys.stdin.read().splitlines()` reads the entire standard input stream
    into memory in a single OS system call and splits on newlines.

Why It Matters for Competitive Programming:
    - Repeatedly calling `input()` inside a loop incurs significant Python overhead.
      `sys.stdin.read()` is up to 10x faster when reading 10^5+ lines.
    - Many problems state: "Input continues until EOF" without providing the number of queries.
      Calling `input()` after EOF raises `EOFError`; `sys.stdin.read().splitlines()` handles
      this naturally and yields an exact list of lines.

Related Repository Problems:
    - 30 DAYS OF CODE/Day-08-Dictionaries-and-Maps.py (Q42)
    - PYTHON/0070_Exceptions.py (Q70)
"""

def fast_query_processor(raw_input_stream: str) -> dict:
    """Simulates single-pass batch query processing from an EOF stream."""
    lines = raw_input_stream.strip().splitlines()
    if not lines:
        return {}
    
    n = int(lines[0])
    phone_book = {}
    for i in range(1, n + 1):
        name, num = lines[i].split()
        phone_book[name] = num
        
    results = {}
    for query in lines[n + 1:]:
        results[query] = phone_book.get(query, "Not found")
        
    return results


# ==============================================================================
# [CON-12] Recursive Tree Traversal & Accumulative Depth Tracking
# ==============================================================================
"""
Concept Name:
    Depth-Accumulating Tree Recursion (XML / Hierarchy Traversal)

Simple Explanation:
    When traversing hierarchical recursive structures (XML nodes, ASTs, file systems),
    state is tracked in two directions:
    1. Top-Down: Current depth/level passed as a parameter (`level + 1`).
    2. Bottom-Up: Subtree metrics (attribute counts, total weights, maximum depths)
       aggregated and returned from recursive calls.

Why It Matters for Competitive Programming:
    - Solves Tree Depth, Subtree Node Counts, Lowest Common Ancestor (LCA),
      and Diameter problems cleanly.

Related Repository Problems:
    - PYTHON/0135_XML-1-Find-the-Score.py (Q135)
    - PYTHON/0136_XML2-Find-the-Maximum-Depth.py (Q136)
"""

class MockElement:
    """Mock XML element for pure-Python demonstration."""
    def __init__(self, tag: str, attrib: dict, children=None):
        self.tag = tag
        self.attrib = attrib
        self.children = children or []

def get_xml_score(element: MockElement) -> int:
    """Counts total number of attributes across entire XML tree."""
    return len(element.attrib) + sum(get_xml_score(child) for child in element.children)

def get_max_tree_depth(element: MockElement, level: int = 0) -> int:
    """Computes maximum depth of a hierarchical tree."""
    if not element.children:
        return level
    return max(get_max_tree_depth(child, level + 1) for child in element.children)


# ==============================================================================
# [CON-13] Short-Circuit Boolean Evaluation (any & all with Generators)
# ==============================================================================
"""
Concept Name:
    Short-Circuit Generator Evaluation with `any()` and `all()`

Simple Explanation:
    - `any(gen)` evaluates truth values lazily and returns `True` at the FIRST `True`.
      Subsequent elements in the generator are NEVER computed.
    - `all(gen)` evaluates truth values lazily and returns `False` at the FIRST `False`.

Why It Matters for Competitive Programming:
    - Avoids unnecessary computation: if checking if any integer in an array is negative,
      `any(x < 0 for x in arr)` stops immediately upon finding the first negative number.
    - Turning a list comprehension `any([x < 0 for x in arr])` into a generator expression
      `any(x < 0 for x in arr)` drops memory usage from O(N) to O(1) and time from O(N) to O(1)
      in favorable cases.

Related Repository Problems:
    - PYTHON/0028_String-Validators.py (Q28)
    - PYTHON/0099_Any-or-All.py (Q99)
"""

def is_palindromic_integer(n: int) -> bool:
    s = str(n)
    return s == s[::-1]

def any_or_all_check(numbers: list) -> bool:
    """Returns True if all numbers are positive and at least one is a palindrome."""
    all_positive = all(x > 0 for x in numbers)
    any_palindrome = any(is_palindromic_integer(x) for x in numbers)
    return all_positive and any_palindrome


# ==============================================================================
# SELF-TEST SUITE
# ==============================================================================
if __name__ == '__main__':
    # Test CON-01
    a1 = safe_accumulator(1)
    a2 = safe_accumulator(2)
    assert a1 == [1] and a2 == [2], "safe_accumulator should not share state"
    
    # Test CON-02
    phones = ["07895462130", "919875641230", "9195969878"]
    sorted_phones = sort_phone_numbers(phones)
    assert sorted_phones == ["+91 78954 62130", "+91 91959 69878", "+91 98756 41230"]
    
    # Test CON-03
    assert ginorts_sort("Sorting1234") == "ginortS1324"
    
    # Test CON-04
    sample_text = "a && b || c &&& d"
    assert substitute_logical_operators(sample_text) == "a and b or c &&& d"
    
    # Test CON-05
    top, grouped = frequency_analysis(["apple", "banana", "apple", "cherry", "banana", "apple"])
    assert top[0] == ("apple", 3)
    assert grouped[3] == ["apple"]
    
    # Test CON-06
    s = {1, 2, 3}
    execute_set_command(s, "discard", 2)
    assert s == {1, 3}
    
    # Test CON-07
    cmds = ["append 1", "append 2", "insert 1 3"]
    assert execute_list_commands(cmds) == [1, 3, 2]
    
    # Test CON-08
    c1 = ComplexNumber(2, 3)
    c2 = ComplexNumber(5, 6)
    c_sum = c1 + c2
    assert c_sum.real == 7 and c_sum.imag == 9
    
    # Test CON-09
    combs = generate_sorted_combinations("BAC", 2)
    assert combs == ['A', 'B', 'C', 'AB', 'AC', 'BC']
    
    # Test CON-10
    mat = [[1, 5, 3], [4, 2, 6]]
    assert min_along_axis_0(mat) == [1, 2, 3]
    assert min_along_axis_1(mat) == [1, 2]
    
    # Test CON-11
    stream = "2\nshubham 9876543210\nalice 1234567890\nshubham\nbob"
    q_res = fast_query_processor(stream)
    assert q_res["shubham"] == "9876543210"
    assert q_res["bob"] == "Not found"
    
    # Test CON-12
    root = MockElement("feed", {"id": "1", "title": "news"}, [
        MockElement("entry", {"id": "2"}),
        MockElement("entry", {"id": "3", "updated": "2026"})
    ])
    assert get_xml_score(root) == 5
    assert get_max_tree_depth(root) == 1
    
    # Test CON-13
    assert any_or_all_check([12, 9, 61, 5, 14]) is True
    assert any_or_all_check([12, -9, 5]) is False

    print("ALL Concepts.py tests passed successfully!")
