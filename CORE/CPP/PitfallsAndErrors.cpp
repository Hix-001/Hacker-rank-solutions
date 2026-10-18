/**
 * ================================================================================
 * 000_PitfallsAndErrors.cpp - C++ Competitive Programming Traps & Debugging Guide
 * ================================================================================
 * A comprehensive diagnostic handbook detailing subtle runtime traps, memory
 * leaks, undefined behavior (UB), and performance bottlenecks in C++ that cause
 * Time Limit Exceeded (TLE), Memory Limit Exceeded (MLE), Wrong Answer (WA),
 * and Runtime Errors (RTE / SIGSEGV) on Codeforces, LeetCode, and HackerRank.
 * 
 * Extracted from real issues encountered across 16+ HackerRank C++ problems.
 * 
 * TABLE OF CONTENTS:
 * --------------------------------------------------------------------------------
 * 1.  [PIT-01] The Leftover Newline Trap (Mixing scanf/cin >> with getline)
 * 2.  [PIT-02] Object Slicing in Exception Catch Blocks
 * 3.  [PIT-03] Memory Leaks & delete vs delete[] Mismatches
 * 4.  [PIT-04] Passing std::string to printf("%s") Without .c_str()
 * 5.  [PIT-05] Variable-Length Arrays (VLA) & Stack Overflow on Large N
 * 6.  [PIT-06] Signed vs Unsigned Integer Comparison (size_t vs int)
 * 7.  [PIT-07] Reusing std::stringstream Without Calling .clear()
 * 8.  [PIT-08] Buffer Desynchronization Hazard (Mixing cin with scanf)
 * 9.  [PIT-09] Non-Virtual Destructor Memory Leaks in Base Classes (UB / MLE)
 * 10. [PIT-10] The Inefficient vector::erase in Loops Trap (O(N^2) TLE)
 * 11. [PIT-11] 32-bit Integer Overflow in Intermediate Arithmetic (WA)
 * 12. [PIT-12] Preprocessor Macro Side Effects & Operator Precedence Gotchas (WA)
 * 13. [PIT-13] std::endl vs '\n' Flush Penalty (TLE on High Volume I/O)
 * 14. [PIT-14] std::map operator[] Unintended Default Insertion Gotcha
 * 15. [PIT-15] dynamic_cast on Non-Polymorphic Base Class Compilation Error
 * 16. [PIT-16] 32-bit PRNG Integer Overflow in Cycle Detection (Undefined Behavior)
 * 17. [PIT-17] Missing Virtual Method in Base Class Causing Static Method Slicing
 * ================================================================================
 */

#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <exception>
#include <stdexcept>
#include <cstdio>
#include <map>
#include <cstdint>
#include <cassert>

// ==============================================================================
// [PIT-01] The Leftover Newline Trap (Mixing scanf/cin >> with getline)
// ==============================================================================
/**
 * Trap:
 *     Reading an integer with `scanf("%d", &n)` or `cin >> n` leaves the trailing
 *     newline character (`\n`) in the standard input stream buffer.
 *     When you immediately follow with `getline(cin, line)`, `getline` reads that
 *     residual newline and returns an EMPTY string instead of the intended text.
 * 
 * Why It Happens:
 *     Formatted extraction (`scanf`, `operator>>`) stops immediately when it reaches
 *     whitespace/newline, leaving the delimiter unconsumed in the buffer.
 *     `getline` terminates at the first `\n` it encounters.
 * 
 * How To Fix It:
 *     Consume the leftover newline before calling `getline`:
 *     Method A: `std::string dummy; std::getline(std::cin, dummy);`
 *     Method B: `std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');`
 * 
 * Repository Reference:
 *     - CPP/0004_Attribute-Parser.cpp (Lines 16-19: scanf("%d %d", &n, &q); getline(cin, temp);)
 */

std::pair<int, std::string> simulateInputWithNewlineTrap(const std::string& simulatedInput, bool applyFix) {
    std::stringstream stream(simulatedInput);
    int number;
    stream >> number; // Leaves '\n' in stream buffer
    
    std::string text;
    if (applyFix) {
        std::string dummy;
        std::getline(stream, dummy); // Discard residual newline
        std::getline(stream, text);  // Read actual line
    } else {
        std::getline(stream, text);  // Erroneously consumes residual newline!
    }
    return {number, text};
}


// ==============================================================================
// [PIT-02] Object Slicing in Exception Catch Blocks
// ==============================================================================
/**
 * Trap:
 *     Catching polymorphic exceptions by value:
 *         `catch (std::exception e)` // BUG: SLICED!
 *     instead of by reference:
 *         `catch (const std::exception& e)` // CORRECT
 * 
 * Why It Happens:
 *     Catching by value constructs a base `std::exception` copy of the thrown object,
 *     slicing off derived member variables and preventing virtual dispatch to
 *     the derived class's `what()` override.
 * 
 * How To Fix It:
 *     Always catch polymorphic exceptions by `const std::exception& e`.
 * 
 * Repository Reference:
 *     - CPP/0012_Exceptional-Server.cpp (Lines 48-52: catch (const std::bad_alloc& e) ... catch (const std::exception& e))
 */

class DerivedException : public std::exception {
private:
    std::string details;
public:
    DerivedException(std::string d) : details(d) {}
    const char* what() const noexcept override {
        return details.c_str();
    }
};

std::string demonstrateCatchByReference() {
    try {
        throw DerivedException("Custom derived error payload");
    } catch (const std::exception& e) {
        // By reference: virtual what() correctly resolves to DerivedException
        return e.what();
    }
}


// ==============================================================================
// [PIT-03] Memory Leaks & delete vs delete[] Mismatches
// ==============================================================================
/**
 * Trap:
 *     1. Allocating an array with `new Type[N]` but freeing with scalar `delete ptr;`
 *        instead of `delete[] ptr;`. This causes undefined behavior (destructors of
 *        subsequent elements are never invoked, and allocator heap metadata corrupts).
 *     2. Dropping pointer nodes in linked lists or trees without `delete`, leading to MLE.
 * 
 * How To Fix It:
 *     - Always match `new[]` with `delete[]`.
 *     - When removing linked list nodes, store `Node* temp = curr->next; curr->next = temp->next; delete temp;`.
 *     - In modern C++, prefer `std::vector` or `std::unique_ptr`.
 * 
 * Repository Reference:
 *     - CPP/0016_Classes-and-Objects.cpp (Lines 27, 40: Student *s = new Student[n]; ... delete[] s;)
 *     - 30 DAYS OF CODE/Day-24-More-Linked-Lists.cpp (Lines 27-29: delete temp;)
 */

void demonstrateArrayAllocationCleanup() {
    int* data = new int[100];
    for (int i = 0; i < 100; ++i) data[i] = i;
    // Correct array deallocation
    delete[] data;
}


// ==============================================================================
// [PIT-04] Passing std::string to printf("%s") Without .c_str()
// ==============================================================================
/**
 * Trap:
 *     Writing `printf("%s\n", myString);` where `myString` is a `std::string`.
 * 
 * Why It Happens:
 *     `printf` is a C function that expects a raw `const char*` pointer pointing to
 *     a null-terminated C string. Passing a C++ class object pushes internal class
 *     pointers and size fields onto the variadic stack, causing garbage output or SIGSEGV.
 * 
 * How To Fix It:
 *     Always call `.c_str()`:
 *     `printf("%s\n", myString.c_str());`
 * 
 * Repository Reference:
 *     - CPP/0004_Attribute-Parser.cpp (Line 61: printf("%s\n", db[query].c_str());)
 *     - CPP/0007_Strings.cpp (Line 18: printf("%s\n", c.c_str());)
 *     - CPP/0014_Structs.cpp (Line 26: printf("%s", st.first_name.c_str());)
 */

std::string safeFormatString(const std::string& input) {
    char buf[128];
    // .c_str() is strictly mandatory here
    std::snprintf(buf, sizeof(buf), "Value: %s", input.c_str());
    return std::string(buf);
}


// ==============================================================================
// [PIT-05] Variable-Length Arrays (VLA) & Stack Overflow on Large N
// ==============================================================================
/**
 * Trap:
 *     Using non-standard C-style Variable Length Arrays on the stack:
 *     `int arr[n];`
 *     where $N$ is taken from user input.
 * 
 * Why It Happens:
 *     Thread call stacks typically have a strict limit (1MB to 8MB).
 *     If $N = 10^6$ ints, that requires $\approx 4$ MB of stack space, causing
 *     instant stack overflow and SIGSEGV before execution even reaches your logic.
 * 
 * How To Fix It:
 *     Use `std::vector<int> arr(n);` (heap allocated) or global static storage.
 * 
 * Repository Reference:
 *     - CPP/0009_Arrays-Introduction.cpp (Shows int arr[n]; acceptable only for small N <= 1000)
 *     - CPP/0010_Variable-Sized-Arrays.cpp (Uses vector<vector<int>> for dynamic sizing)
 */

std::vector<int> allocateSafeVector(size_t n) {
    // Vector allocates on heap, immune to stack overflow
    return std::vector<int>(n, 0);
}


// ==============================================================================
// [PIT-06] Signed vs Unsigned Integer Comparison (size_t vs int)
// ==============================================================================
/**
 * Trap:
 *     Comparing signed `int` with unsigned `container.size()` (`size_t`):
 *     `int i = -1; if (i < v.size())` evaluates to FALSE!
 * 
 * Why It Happens:
 *     Under C++ integer promotion rules, when a signed int is compared with an
 *     unsigned type of the same or larger rank, the signed value is converted to
 *     unsigned. A negative value like `-1` becomes `18446744073709551615ULL`!
 * 
 * How To Fix It:
 *     - Use `size_t` for index variables: `for (size_t i = 0; i < v.size(); ++i)`
 *     - Or cast explicitly: `static_cast<int>(v.size())`
 * 
 * Repository Reference:
 *     - CPP/0004_Attribute-Parser.cpp (Line 44: for (size_t j = 0; j < tag_stack.size(); ++j))
 *     - CPP/0013_StringStream.cpp (Line 28: for (size_t i = 0; i < integers.size(); i++))
 */

bool demonstrateSignedUnsignedTrap() {
    std::vector<int> vec = {10, 20, 30};
    int negativeIndex = -1;
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wsign-compare"
    bool buggyComparison = (negativeIndex < vec.size()); // Evaluates to false!
#pragma GCC diagnostic pop
    bool safeComparison = (negativeIndex < static_cast<int>(vec.size())); // Evaluates to true!
    
    assert(!buggyComparison);
    assert(safeComparison);
    return safeComparison;
}


// ==============================================================================
// [PIT-07] Reusing std::stringstream Without Calling .clear()
// ==============================================================================
/**
 * Trap:
 *     Reusing a `std::stringstream` by setting `.str("new content")` after it hit EOF:
 *     All subsequent extractions `ss >> x` will SILENTLY FAIL!
 * 
 * Why It Happens:
 *     When a stream reaches the end of its buffer, it sets the `eofbit` and `failbit`.
 *     Calling `ss.str("new content")` replaces the internal buffer, but does NOT
 *     clear the error flags.
 * 
 * How To Fix It:
 *     Always call `ss.clear()` before reusing the stream:
 *     `ss.clear();`
 *     `ss.str("new content");`
 * 
 * Repository Reference:
 *     - CPP/0013_StringStream.cpp
 */

bool demonstrateStringStreamReset() {
    std::stringstream ss("100");
    int val1 = 0, val2 = 0;
    ss >> val1;
    assert(val1 == 100);
    assert(ss.eof()); // eofbit is now set

    // Attempt reuse without clear() -> FAILS!
    ss.str("200");
    ss >> val2;
    assert(val2 == 0); // Did not extract because eofbit was still active

    // Proper reuse with clear() -> SUCCEEDS!
    ss.clear(); // Resets eofbit/failbit to goodbit
    ss.str("300");
    ss >> val2;
    assert(val2 == 300);
    return true;
}


// ==============================================================================
// [PIT-08] Buffer Desynchronization Hazard (Mixing cin with scanf)
// ==============================================================================
/**
 * Trap:
 *     Calling `std::ios::sync_with_stdio(false);` and then mixing `cin` with `scanf`
 *     or `cout` with `printf`.
 * 
 * Why It Happens:
 *     `sync_with_stdio(false)` disconnects the C++ standard stream buffers from the
 *     underlying C stdio buffers to maximize performance.
 *     If you subsequently read from both, the two buffers read independent chunks
 *     from the operating system, interleaving and corrupting your input order!
 * 
 * How To Fix It:
 *     Once `std::ios::sync_with_stdio(false)` is enabled, use ONLY `cin` and `cout`.
 *     Never mix with `scanf` or `printf`.
 * 
 * Repository Reference:
 *     - CPP/0015_Pointer.cpp (Lines 10-11: uses sync_with_stdio(false) with pure cin/cout)
 */


// ==============================================================================
// [PIT-09] Non-Virtual Destructor Memory Leaks in Base Classes (UB / MLE)
// ==============================================================================
/**
 * Trap:
 *     Deleting an object through a pointer to its base class:
 *         `Base* ptr = new Derived(); delete ptr;`
 *     when `Base` does NOT have a virtual destructor: `virtual ~Base() {}`.
 * 
 * Why It Happens:
 *     Without a virtual destructor, the delete operator performs static binding,
 *     calling only `Base::~Base()`. The `Derived::~Derived()` destructor is completely skipped!
 *     Any dynamic memory, open handles, or vectors held by `Derived` will leak silently.
 * 
 * How To Fix It:
 *     Always declare `virtual ~Base() {}` in any class intended for polymorphism.
 * 
 * Repository Reference:
 *     - CPP/0018_Virtual-Functions.cpp (Line 18: virtual ~Person() {})
 */

class SafeBase {
public:
    static int destructorCalls;
    virtual ~SafeBase() { destructorCalls++; }
};
int SafeBase::destructorCalls = 0;

class SafeDerived : public SafeBase {
public:
    ~SafeDerived() override { destructorCalls++; }
};


// ==============================================================================
// [PIT-10] The Inefficient vector::erase in Loops Trap (O(N^2) TLE)
// ==============================================================================
/**
 * Trap:
 *     Removing matching elements from a vector in a loop using `v.erase(it)`.
 * 
 * Why It Happens:
 *     `std::vector` is contiguous. Every call to `erase()` shifts all subsequent elements
 *     leftward by 1 slot ($O(N)$). Calling this inside a loop for $K$ removals results
 *     in $O(N \cdot K) = O(N^2)$ execution time, causing instant TLE on $N \ge 10^5$.
 * 
 * How To Fix It:
 *     1. If order does NOT matter: Swap with `v.back()` and call `v.pop_back()` (O(1)).
 *     2. If order MUST be preserved: Use the standard Erase-Remove idiom:
 *        `v.erase(std::remove(v.begin(), v.end(), val), v.end());` (O(N) single-pass!).
 * 
 * Repository Reference:
 *     - CPP/0021_Vector-Erase.cpp (Q21)
 */

#include <algorithm>

void efficientEraseValue(std::vector<int>& vec, int valueToRemove) {
    vec.erase(std::remove(vec.begin(), vec.end(), valueToRemove), vec.end());
}


// ==============================================================================
// [PIT-11] 32-bit Integer Overflow in Intermediate Arithmetic (WA)
// ==============================================================================
/**
 * Trap:
 *     Writing `long long volume = l * b * h;` when `l, b, h` are 32-bit `int`.
 * 
 * Why It Happens:
 *     In C++, the type of an arithmetic expression is determined SOLELY by its operands,
 *     NOT by the target variable receiving the assignment.
 *     If `l = 10^5, b = 10^5, h = 10^5`, `l * b * h` evaluates to $10^{15}$, which exceeds
 *     the maximum signed 32-bit integer ($2.14 \times 10^9$). The expression overflows in
 *     32-bit registers, and only the corrupted truncated value is converted to `long long`.
 * 
 * How To Fix It:
 *     Cast at least one factor to `long long` before multiplication:
 *     `long long volume = static_cast<long long>(l) * b * h;`
 * 
 * Repository Reference:
 *     - CPP/0020_Box-It.cpp (Line 47: return (long long)l * b * h;)
 */

long long safeVolumeCalculation(int l, int b, int h) {
    return static_cast<long long>(l) * b * h;
}


// ==============================================================================
// [PIT-12] Preprocessor Macro Side Effects & Operator Precedence Gotchas (WA)
// ==============================================================================
/**
 * Trap:
 *     Defining functional macros without enclosing parameters and bodies in parentheses:
 *     `#define MULT(a, b) a * b`
 *     Calling `MULT(2 + 3, 4 + 5)` expands to `2 + 3 * 4 + 5 = 2 + 12 + 5 = 19`!
 * 
 * Why It Happens:
 *     The preprocessor performs blind textual replacement without understanding syntax
 *     trees or mathematical operator precedence.
 * 
 * How To Fix It:
 *     Always parenthesize both every argument AND the entire macro body:
 *     `#define MULT(a, b) ((a) * (b))`
 *     Or better yet, use C++ `inline` or `constexpr` template functions.
 * 
 * Repository Reference:
 *     - CPP/0030_Preprocessor-Solution.cpp (Q30)
 */

#define SAFE_MULT(a, b) ((a) * (b))


// ==============================================================================
// [PIT-13] std::endl vs '\n' Flush Penalty (TLE on High Volume I/O)
// ==============================================================================
/**
 * Trap:
 *     Writing `std::cout << result << std::endl;` inside high-frequency loops.
 * 
 * Why It Happens:
 *     `std::endl` does TWO distinct actions:
 *     1. Writes the newline character `\n`.
 *     2. Calls `std::cout.flush()`, forcing a hardware/OS system call.
 *     For $10^5$ outputs, this causes $10^5$ distinct system calls instead of batching
 *     in memory buffers, degrading throughput by 20x–100x and causing TLE.
 * 
 * How To Fix It:
 *     Always output `'\n'` instead of `std::endl`:
 *     `std::cout << result << '\n';`
 * 
 * Repository Reference:
 *     - CPP/0029_Cpp-Class-Templates.cpp (Line 50: cout << myint.add(element2) << '\n';)
 *     - CPP/0030_Preprocessor-Solution.cpp (Line 37: cout << ... << '\n';)
 */


// ==============================================================================
// [PIT-14] std::map operator[] Unintended Default Insertion Gotcha
// ==============================================================================
/**
 * Trap:
 *     Using `myMap[key]` simply to check whether a key exists or to read its value.
 * 
 * Why It Happens:
 *     `std::map::operator[]` is NON-CONST. If `key` is not present, it inserts a new
 *     key-value pair with a default-constructed value (e.g., 0, empty string, nullptr).
 *     This silently modifies the map's size, degrades performance, and can trigger
 *     false positives in subsequent `.size()` or empty checks!
 * 
 * How To Fix It:
 *     Use `.find(key)` or `.count(key)` for read-only access / existence checks:
 *     `if (myMap.find(key) != myMap.end()) { ... }`
 *     Or `myMap.at(key)` if the key MUST exist (throws `std::out_of_range` on absence).
 * 
 * Repository Reference:
 *     - CPP/0033_Maps-STL.cpp (Q33)
 */

inline bool safeMapContains(const std::map<std::string, int>& m, const std::string& key) {
    return m.find(key) != m.end();
}


// ==============================================================================
// [PIT-15] dynamic_cast on Non-Polymorphic Base Class Compilation Error
// ==============================================================================
/**
 * Trap:
 *     Attempting to use `dynamic_cast<Derived*>(basePtr)` when `Base` has NO virtual functions.
 * 
 * Why It Happens:
 *     `dynamic_cast` relies on Run-Time Type Information (RTTI) stored inside the object's vtable.
 *     If `Base` lacks any virtual functions, the compiler generates no vtable/vptr for it.
 *     Compiling `dynamic_cast` on a non-polymorphic type fails with:
 *     "error: cannot dynamic_cast 'ptr' (of type 'class Base*') to type 'class Derived*'
 *      (source type is not polymorphic)"
 * 
 * How To Fix It:
 *     Ensure the base class defines at least one virtual function, typically the virtual destructor:
 *     `virtual ~Base() = default;`
 * 
 * Repository Reference:
 *     - CPP/0036_Magic-Spells.cpp (Q36)
 */

class PolymorphicBase {
public:
    virtual ~PolymorphicBase() = default; // Required for dynamic_cast
};

class PolymorphicDerived : public PolymorphicBase {
public:
    int specializedValue() const { return 999; }
};

inline bool canCastToDerived(PolymorphicBase* ptr) {
    return dynamic_cast<PolymorphicDerived*>(ptr) != nullptr;
}


// ==============================================================================
// [PIT-16] 32-bit PRNG Integer Overflow in Cycle Detection (Undefined Behavior)
// ==============================================================================
/**
 * Trap:
 *     Using signed 32-bit `int` for PRNG congruential formulas:
 *     `int next = (curr * p + q) % m;`
 *     When `curr * p` exceeds $2^{31} - 1 \approx 2.14 \times 10^9$, signed integer
 *     overflow occurs, resulting in undefined behavior (UB), negative array indices, or wrong answers.
 * 
 * How To Fix It:
 *     Use `unsigned int` (which wraps safely modulo $2^{32}$) or 64-bit `uint64_t`:
 *     `unsigned int next = (1ULL * curr * p + q) % (1ULL << 31);`
 * 
 * Repository Reference:
 *     - CPP/0034_Bit-Array.cpp (Q34)
 */

inline uint32_t safePrngStep(uint32_t curr, uint32_t p, uint32_t q) {
    // 64-bit calculation guarantees no intermediate 32-bit overflow
    uint64_t product = static_cast<uint64_t>(curr) * p + q;
    return static_cast<uint32_t>(product & 0x7FFFFFFF); // Modulo 2^31
}


// ==============================================================================
// [PIT-17] Missing Virtual Method in Base Class Causing Static Method Slicing
// ==============================================================================
/**
 * Trap:
 *     Subclass overrides a base method `int getPrice()`, but the base class declared it
 *     WITHOUT the `virtual` keyword.
 * 
 * Why It Happens:
 *     When calling through a base pointer/reference `Base* room = new LuxurySuite();`,
 *     C++ uses early (static) binding. Because `getPrice()` is not virtual, the compiler
 *     binds directly to `Base::getPrice()`, completely ignoring `LuxurySuite::getPrice()`.
 *     The room price is calculated incorrectly without emitting any warnings.
 * 
 * How To Fix It:
 *     Declare `virtual int getPrice() const;` in the base class, and use the `override`
 *     specifier in the derived class.
 * 
 * Repository Reference:
 *     - CPP/0042_Hotel-Prices.cpp (Q42)
 */

class TrapRoomBase {
public:
    virtual ~TrapRoomBase() = default;
    virtual int getPrice() const { return 100; } // virtual ensures late binding
};

class TrapRoomDerived : public TrapRoomBase {
public:
    int getPrice() const override { return 150; }
};


// ==============================================================================
// SELF-TEST VERIFICATION SUITE
// ==============================================================================
int main() {
    std::cout << "[RUNNING] PitfallsAndErrors.cpp Self-Test Suite...\n";

    // Test PIT-01: Newline Trap Simulation
    std::string testInput = "42\nHelloWorld\n";
    auto trapped = simulateInputWithNewlineTrap(testInput, false);
    assert(trapped.first == 42);
    assert(trapped.second == ""); // Trapped: consumed empty newline!

    auto fixed = simulateInputWithNewlineTrap(testInput, true);
    assert(fixed.first == 42);
    assert(fixed.second == "HelloWorld"); // Fixed!

    // Test PIT-02: Catch by Reference Slicing Prevention
    assert(demonstrateCatchByReference() == "Custom derived error payload");

    // Test PIT-03: Array Cleanup
    demonstrateArrayAllocationCleanup();

    // Test PIT-04: .c_str() Safe Formatting
    assert(safeFormatString("Antigravity") == "Value: Antigravity");

    // Test PIT-05: Heap Vector
    auto safeVec = allocateSafeVector(1000);
    assert(safeVec.size() == 1000);

    // Test PIT-06: Signed vs Unsigned Comparison
    assert(demonstrateSignedUnsignedTrap() == true);

    // Test PIT-07: StringStream Reset
    assert(demonstrateStringStreamReset() == true);

    // Test PIT-09: Virtual Destructor Execution
    SafeBase::destructorCalls = 0;
    SafeBase* polymorphicPtr = new SafeDerived();
    delete polymorphicPtr;
    assert(SafeBase::destructorCalls == 2); // Both SafeDerived and SafeBase destructors called!

    // Test PIT-10: Efficient Erase-Remove Idiom
    std::vector<int> numbers = {1, 2, 3, 2, 4, 2, 5};
    efficientEraseValue(numbers, 2);
    assert((numbers == std::vector<int>{1, 3, 4, 5}));

    // Test PIT-11: Intermediate Overflow Prevention
    long long safeVol = safeVolumeCalculation(100000, 100000, 100000);
    assert(safeVol == 1000000000000000LL);

    // Test PIT-12: Macro Parenthesization
    int calc = SAFE_MULT(2 + 3, 4 + 5);
    assert(calc == 45); // (5) * (9) == 45, NOT 19

    // Test PIT-14: std::map Safe Contains vs operator[]
    std::map<std::string, int> myMap;
    assert(!safeMapContains(myMap, "ghost_key"));
    assert(myMap.size() == 0); // No accidental element inserted!
    myMap["present"] = 42;
    assert(safeMapContains(myMap, "present"));

    // Test PIT-15: dynamic_cast on Polymorphic Type
    PolymorphicBase* polyDerived = new PolymorphicDerived();
    PolymorphicBase* polyBase = new PolymorphicBase();
    assert(canCastToDerived(polyDerived) == true);
    assert(canCastToDerived(polyBase) == false);
    delete polyDerived;
    delete polyBase;

    // Test PIT-16: Safe PRNG Step (no 32-bit overflow)
    // S=1, P=2, Q=3 -> (1*2 + 3) = 5
    assert(safePrngStep(1, 2, 3) == 5);
    // Large values that would overflow signed 32-bit int:
    uint32_t bigNext = safePrngStep(2000000000U, 3U, 5U);
    // (2000000000 * 3 + 5) = 6000000005
    // 6000000005 % 2^31 = 6000000005 - 2 * 2147483648 = 1705032709
    assert(bigNext == (6000000005ULL & 0x7FFFFFFF));

    // Test PIT-17: Dynamic Late Binding
    TrapRoomBase* r1 = new TrapRoomBase();
    TrapRoomBase* r2 = new TrapRoomDerived();
    assert(r1->getPrice() == 100);
    assert(r2->getPrice() == 150); // Virtual dispatch ensures derived price is called!
    delete r1;
    delete r2;

    std::cout << "[SUCCESS] ALL PitfallsAndErrors.cpp tests passed cleanly!\n";
    return 0;
}
