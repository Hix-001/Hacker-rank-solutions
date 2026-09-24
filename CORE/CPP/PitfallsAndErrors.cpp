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
 * ================================================================================
 */

#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <exception>
#include <stdexcept>
#include <cstdio>
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

    std::cout << "[SUCCESS] ALL PitfallsAndErrors.cpp tests passed cleanly!\n";
    return 0;
}
