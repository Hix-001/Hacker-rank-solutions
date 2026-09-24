/**
 * ================================================================================
 * 000_Concepts.cpp - C++ Competitive Programming Core Concept Reference
 * ================================================================================
 * A curated reference of deep, reusable programming concepts, C++ memory models,
 * object lifecycle mechanics, pointer arithmetic, polymorphism, and stream I/O
 * principles extracted from 16+ HackerRank C++ solutions.
 * 
 * Organized for quick study and long-term retention before competing in Codeforces,
 * LeetCode, and HackerRank contests.
 * 
 * TABLE OF CONTENTS:
 * --------------------------------------------------------------------------------
 * 1.  [CON-01] Memory Model: Automatic (Stack) vs Dynamic (Heap / Free Store)
 * 2.  [CON-02] Pointer Semantics, Addresses (&), and Dereferencing (*)
 * 3.  [CON-03] Parameter Passing Semantics: By Value vs Reference vs Pointer
 * 4.  [CON-04] Exception Hierarchy, Catch Polymorphism & Slicing Prevention
 * 5.  [CON-05] Template Metaprogramming & Generic Function Instantiation
 * 6.  [CON-06] Object Encapsulation: Structs vs Classes & Access Control
 * 7.  [CON-07] Stream Buffer Mechanics & Internal State Flags (std::stringstream)
 * 8.  [CON-08] C-Style stdio (cstdio) vs C++ Streams (iostream) & Interoperability
 * ================================================================================
 */

#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <exception>
#include <stdexcept>
#include <new>
#include <cstring>
#include <cassert>
#include <cmath>

// ==============================================================================
// [CON-01] Memory Model: Automatic (Stack) vs Dynamic (Heap / Free Store)
// ==============================================================================
/**
 * Concept Name:
 *     Automatic Storage (Stack) vs Dynamic Storage (Free Store / Heap)
 * 
 * Simple Explanation:
 *     Variables declared inside a function or block (e.g., `int x;`, `int arr[10];`)
 *     are allocated on the call stack. They are automatically deallocated when leaving scope.
 *     However, stack memory is limited (typically 1MB to 8MB). Large allocations
 *     (e.g., arrays of size >= 10^6) cause stack overflow and runtime crash (SIGSEGV).
 * 
 *     Dynamic memory (`new`, `new[]`) allocates from the free store (heap), which is
 *     constrained only by system RAM. It persists until explicitly freed (`delete`, `delete[]`).
 * 
 * Why It Matters for Competitive Programming:
 *     - If N can be up to 10^6, allocating `int arr[N];` on the stack causes RTE.
 *     - Either allocate dynamically (`new int[N]`, `delete[] arr`), use `std::vector<int>`,
 *       or declare large arrays globally (static/BSS segment).
 *     - For custom linked lists or trees, every node allocated via `new` must be freed
 *       or cleaned up to prevent memory leaks during stress testing.
 * 
 * Repository References:
 *     - CPP/0016_Classes-and-Objects.cpp (Student *s = new Student[n]; ... delete[] s;)
 *     - CPP/0009_Arrays-Introduction.cpp
 *     - 30 DAYS OF CODE/Day-24-More-Linked-Lists.cpp (delete temp;)
 */

void demonstrateMemoryAllocations() {
    int n = 5;
    // Dynamic allocation of primitive array
    int* dynamic_arr = new int[n];
    for (int i = 0; i < n; ++i) dynamic_arr[i] = (i + 1) * 10;
    
    assert(dynamic_arr[0] == 10 && dynamic_arr[4] == 50);
    
    // Always pair `new[]` with `delete[]`
    delete[] dynamic_arr;
}


// ==============================================================================
// [CON-02] Pointer Semantics, Addresses (&), and Dereferencing (*)
// ==============================================================================
/**
 * Concept Name:
 *     Pointer Mechanics, Address Resolution, and Indirection
 * 
 * Simple Explanation:
 *     A variable resides at a specific hexadecimal memory address.
 *     The address-of operator `&x` extracts the memory location of `x`.
 *     A pointer `int* ptr = &x;` stores that memory address.
 *     The dereference operator `*ptr` reads or mutates the value stored at that address.
 * 
 * Why It Matters for Competitive Programming:
 *     - Pointer manipulation is essential for dynamic data structures (trees, graphs, lists).
 *     - Functions can directly modify caller variables in place without returning tuples.
 * 
 * Repository References:
 *     - CPP/0015_Pointer.cpp (Q15)
 *     - 30 DAYS OF CODE/Day-22-Binary-Search-Trees.cpp
 *     - 30 DAYS OF CODE/Day-24-More-Linked-Lists.cpp
 */

void inPlaceMathUpdate(int* a, int* b) {
    int sum = *a + *b;
    int diff = std::abs(*a - *b);
    *a = sum;
    *b = diff;
}


// ==============================================================================
// [CON-03] Parameter Passing Semantics: By Value vs Reference vs Pointer
// ==============================================================================
/**
 * Concept Name:
 *     Pass-by-Value vs Pass-by-Reference vs Pass-by-Pointer
 * 
 * Mechanics:
 *     1. Pass-by-Value (`void func(std::vector<int> v)`):
 *        Creates a deep copy of the entire container! If vector size is 10^5,
 *        calling this in a loop causes instant O(N * K) TLE and MLE.
 *     2. Pass-by-Const-Reference (`void func(const std::vector<int>& v)`):
 *        Zero copy overhead (passes an alias/pointer under the hood), and prevents accidental mutation.
 *     3. Pass-by-Reference (`void func(std::vector<int>& v)`):
 *        Zero copy overhead, allows in-place mutation.
 *     4. Pass-by-Pointer (`void func(int* ptr)`):
 *        Can be null (`nullptr`), requires explicit dereference `*ptr` or arrow `ptr->member`.
 * 
 * Repository References:
 *     - CPP/0008_Functions.cpp (Q8)
 *     - CPP/0015_Pointer.cpp (Q15)
 */

void appendSquares(const std::vector<int>& source, std::vector<int>& destination) {
    // source is read-only (const ref), destination is modified in place (ref)
    destination.reserve(destination.size() + source.size());
    for (int val : source) {
        destination.push_back(val * val);
    }
}


// ==============================================================================
// [CON-04] Exception Hierarchy, Catch Polymorphism & Slicing Prevention
// ==============================================================================
/**
 * Concept Name:
 *     Polymorphic Exception Dispatch & Catch Order
 * 
 * Mechanics:
 *     All standard exceptions derive from `std::exception` (e.g., `std::bad_alloc`,
 *     `std::out_of_range`, `std::invalid_argument`).
 *     Exception handlers (`catch` blocks) are evaluated sequentially from top to bottom.
 * 
 * Critical Rules:
 *     1. Catch derived exceptions FIRST, and base classes LAST:
 *        `catch (const std::bad_alloc& e)` must appear BEFORE `catch (const std::exception& e)`.
 *        If `std::exception` is first, it intercepts `bad_alloc`, hiding the specialized handler.
 *     2. ALWAYS catch by reference (`const std::exception& e`):
 *        Catching by value (`catch (std::exception e)`) triggers Object Slicing, stripping
 *        the derived class members and virtual table overrides.
 *     3. Catch-all `catch (...)` handles untyped or third-party throws (e.g. `throw 0;`).
 * 
 * Repository References:
 *     - CPP/0012_Exceptional-Server.cpp (Q12)
 *     - CPP/0011_Inherited-Code.cpp (Q11)
 */

class CustomLengthException : public std::exception {
private:
    int length;
    std::string msg;
public:
    CustomLengthException(int len) : length(len) {
        msg = "BadLengthException: " + std::to_string(len);
    }
    int getLength() const noexcept { return length; }
    const char* what() const noexcept override {
        return msg.c_str();
    }
};

std::string processRequest(long long sizeCode) {
    try {
        if (sizeCode < 0) {
            throw std::invalid_argument("Negative parameter error");
        } else if (sizeCode == 0) {
            throw 404; // Untyped exception
        } else if (sizeCode > 1000000000000LL) {
            throw std::bad_alloc(); // Memory exhaustion simulation
        } else if (sizeCode < 5) {
            throw CustomLengthException(static_cast<int>(sizeCode));
        }
        return "SUCCESS";
    } catch (const CustomLengthException& e) {
        return "Length too short: " + std::to_string(e.getLength());
    } catch (const std::bad_alloc&) {
        return "Not enough memory";
    } catch (const std::exception& e) {
        return std::string("Standard Exception: ") + e.what();
    } catch (...) {
        return "Unknown Exception";
    }
}


// ==============================================================================
// [CON-05] Template Metaprogramming & Generic Function Instantiation
// ==============================================================================
/**
 * Concept Name:
 *     Function Templates & Compile-Time Polymorphism
 * 
 * Simple Explanation:
 *     Templates allow writing algorithms that work over arbitrary data types
 *     (`int`, `double`, `std::string`, custom classes) without duplicating code.
 *     The compiler instantiates a concrete function specialization for each unique
 *     type invoked at call sites.
 * 
 * Why It Matters for Competitive Programming:
 *     - Write generic tree traversals, array printers, matrix multipliers, and search functions.
 *     - Eliminates type-casting bugs and maintains 100% type safety.
 * 
 * Repository References:
 *     - 30 DAYS OF CODE/Day-21-Generics.cpp (Q61)
 */

template <typename T>
std::string formatCollection(const std::vector<T>& items, const std::string& delimiter = " ") {
    std::stringstream ss;
    for (size_t i = 0; i < items.size(); ++i) {
        ss << items[i];
        if (i + 1 < items.size()) {
            ss << delimiter;
        }
    }
    return ss.str();
}


// ==============================================================================
// [CON-06] Object Encapsulation: Structs vs Classes & Access Control
// ==============================================================================
/**
 * Concept Name:
 *     Access Specifiers & Object-Oriented Encapsulation
 * 
 * Mechanics:
 *     In C++:
 *     - `struct`: Members are `public` by default. Used primarily for Plain Old Data (POD)
 *       or simple data aggregates (e.g., Graph edges, Point2D, TreeNode).
 *     - `class`: Members are `private` by default. Used when invariants need protection
 *       and data must be manipulated via public member functions.
 * 
 * Repository References:
 *     - CPP/0014_Structs.cpp (Q14)
 *     - CPP/0016_Classes-and-Objects.cpp (Q16)
 */

class StudentAccount {
private:
    std::string id;
    int scores[5];

public:
    StudentAccount(std::string studentId) : id(studentId) {
        for (int i = 0; i < 5; ++i) scores[i] = 0;
    }

    void setScore(int index, int value) {
        if (index >= 0 && index < 5) {
            scores[index] = value;
        }
    }

    int getTotalScore() const {
        int sum = 0;
        for (int i = 0; i < 5; ++i) sum += scores[i];
        return sum;
    }

    std::string getId() const { return id; }
};


// ==============================================================================
// [CON-07] Stream Buffer Mechanics & Internal State Flags (std::stringstream)
// ==============================================================================
/**
 * Concept Name:
 *     Stream State Flags: good(), eof(), fail(), bad()
 * 
 * Mechanics:
 *     `std::stringstream` maintains stream state bits:
 *     - `goodbit`: No error, ready for I/O.
 *     - `eofbit`: End of stream buffer reached.
 *     - `failbit`: Formatting error (e.g. attempting to read an int when the next char is 'x').
 * 
 * Pitfall:
 *     When reusing a `stringstream` object for multiple lines:
 *     Calling `ss.str("new string")` is NOT ENOUGH if EOF was reached!
 *     You MUST call `ss.clear()` to reset the error/eof state bits back to goodbit.
 * 
 * Repository References:
 *     - CPP/0013_StringStream.cpp (Q13)
 *     - CPP/0004_Attribute-Parser.cpp (Q4)
 */

bool safeExtractInt(std::stringstream& ss, int& outNum) {
    if (ss >> outNum) {
        return true;
    }
    // Clear fail state if we want to skip bad token
    ss.clear();
    std::string badToken;
    ss >> badToken; // Discard invalid characters
    return false;
}


// ==============================================================================
// [CON-08] C-Style stdio (cstdio) vs C++ Streams (iostream) & Interoperability
// ==============================================================================
/**
 * Concept Name:
 *     I/O Stream Synchronization & C-String Conversion (.c_str())
 * 
 * Mechanics:
 *     1. `printf` / `scanf` (`<cstdio>`):
 *        Very fast by default, but requires precise format specifiers:
 *        - `int`: `%d`
 *        - `long`: `%ld`, `long long`: `%lld`
 *        - `float`: `%f` (or `%.3f`), `double`: `%lf` (or `%.9lf`)
 *        - `char`: `%c`, C-string: `%s`
 *     2. Printing `std::string` with `printf("%s")`:
 *        Passing a `std::string` directly is undefined behavior!
 *        Must call `str.c_str()` to pass a null-terminated `const char*`.
 *     3. `std::cin` / `std::cout` (`<iostream>`):
 *        Type-safe, but slower by default because it synchronizes with C stdio.
 *        To match or exceed `scanf`/`printf` speed:
 *        `std::ios::sync_with_stdio(false); std::cin.tie(nullptr);`
 * 
 * Repository References:
 *     - CPP/0001_Hello-World.cpp
 *     - CPP/0002_Input-and-Output.cpp
 *     - CPP/0003_Basic-Data-Types.cpp
 *     - CPP/0007_Strings.cpp
 *     - CPP/0015_Pointer.cpp
 */

std::string formatPrimitiveTypes(int i, long l, char c, float f, double d) {
    char buffer[256];
    std::snprintf(buffer, sizeof(buffer), "%d | %ld | %c | %.3f | %.9lf", i, l, c, f, d);
    return std::string(buffer);
}


// ==============================================================================
// SELF-TEST VERIFICATION SUITE
// ==============================================================================
int main() {
    std::cout << "[RUNNING] Concepts.cpp Self-Test Suite...\n";

    // Test CON-01: Memory Allocation
    demonstrateMemoryAllocations();

    // Test CON-02: Pointer In-Place Update
    int valA = 4;
    int valB = 5;
    inPlaceMathUpdate(&valA, &valB);
    assert(valA == 9); // 4 + 5
    assert(valB == 1); // |4 - 5|

    // Test CON-03: Pass by Reference vs Value
    std::vector<int> src = {1, 2, 3};
    std::vector<int> dest;
    appendSquares(src, dest);
    assert((dest == std::vector<int>{1, 4, 9}));

    // Test CON-04: Exception Handling Hierarchy
    assert(processRequest(-1) == "Standard Exception: Negative parameter error");
    assert(processRequest(0) == "Unknown Exception");
    assert(processRequest(2000000000000LL) == "Not enough memory");
    assert(processRequest(3) == "Length too short: 3");
    assert(processRequest(100) == "SUCCESS");

    // Test CON-05: Template Generics
    std::vector<int> nums = {10, 20, 30};
    assert(formatCollection(nums, " -> ") == "10 -> 20 -> 30");
    std::vector<std::string> words = {"C++", "Templates", "Rock"};
    assert(formatCollection(words, " ") == "C++ Templates Rock");

    // Test CON-06: Encapsulation
    StudentAccount account("STU_42");
    account.setScore(0, 95);
    account.setScore(1, 85);
    account.setScore(2, 90);
    account.setScore(3, 100);
    account.setScore(4, 80);
    assert(account.getTotalScore() == 450);
    assert(account.getId() == "STU_42");

    // Test CON-07: StringStream Flag Reset
    std::stringstream ss("42 bad 100");
    int num1, num2;
    assert(safeExtractInt(ss, num1) && num1 == 42);
    // Next token is "bad" -> extraction will fail and recover
    assert(!safeExtractInt(ss, num2));
    assert(safeExtractInt(ss, num2) && num2 == 100);

    // Test CON-08: Format Primitives
    // Note: On Windows (LLP64), long is 32-bit (max ~2*10^9), whereas on Linux (LP64) long is 64-bit.
    // For universal 64-bit precision, long long (%lld) is used.
    std::string formatted = formatPrimitiveTypes(3, 123456789L, 'e', 334.230f, 14049.304930000);
    assert(formatted.find("3 | 123456789 | e") != std::string::npos);

    std::cout << "[SUCCESS] ALL Concepts.cpp tests passed cleanly!\n";
    return 0;
}
