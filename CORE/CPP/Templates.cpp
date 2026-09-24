/**
 * ================================================================================
 * 000_Templates.cpp - C++ Competitive Programming Production Templates
 * ================================================================================
 * A library of modular, battle-tested, copy-pasteable data structures, I/O
 * optimizers, custom exceptions, and boilerplate templates for Codeforces,
 * LeetCode, and HackerRank contests.
 * 
 * Extracted and generalized from 16+ HackerRank C++ solutions.
 * 
 * TABLE OF CONTENTS:
 * --------------------------------------------------------------------------------
 * 1.  [TMP-01] Contest Fast I/O Boilerplate & Stream Decoupling
 * 2.  [TMP-02] Delimited String Tokenizer via std::stringstream
 * 3.  [TMP-03] Generic 2D Jagged Matrix & Grid Initializer
 * 4.  [TMP-04] Custom Exception Boilerplate with Formatted Diagnostics
 * 5.  [TMP-05] Binary Search Tree (BST) & Singly-Linked List Node Boilerplates
 * 6.  [TMP-06] Generic Vector / Array Pretty-Printer (Templates)
 * 7.  [TMP-07] Hierarchical Tag / Scope Attribute Database Template
 * 8.  [TMP-08] Static Lookup Dispatch Helper (Branchless Table)
 * ================================================================================
 */

#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <map>
#include <memory>
#include <exception>
#include <algorithm>
#include <cassert>

// ==============================================================================
// [TMP-01] Contest Fast I/O Boilerplate & Stream Decoupling
// ==============================================================================
/**
 * Usage:
 *     Call `initFastIO()` at the very top of `main()` in competitive programming.
 *     Unties C++ streams from C standard I/O buffers and prevents cin from flushing
 *     cout before every read, making cin/cout as fast as or faster than scanf/printf.
 * 
 * Repository Reference:
 *     - CPP/0015_Pointer.cpp (Lines 10-11: ios::sync_with_stdio(false); cin.tie(nullptr);)
 */

inline void initFastIO() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
}


// ==============================================================================
// [TMP-02] Delimited String Tokenizer via std::stringstream
// ==============================================================================
/**
 * Usage:
 *     Parses any delimited string (such as CSV "1,2,3" or whitespace "a b c")
 *     into strongly-typed tokens of type T.
 * 
 * Repository Reference:
 *     - CPP/0013_StringStream.cpp (Q13)
 */

template <typename T>
std::vector<T> tokenizeDelimited(const std::string& input, char delimiter = ',') {
    std::vector<T> tokens;
    std::stringstream ss(input);
    std::string item;
    while (std::getline(ss, item, delimiter)) {
        if (!item.empty()) {
            std::stringstream converter(item);
            T val;
            if (converter >> val) {
                tokens.push_back(val);
            }
        }
    }
    return tokens;
}


// ==============================================================================
// [TMP-03] Generic 2D Jagged Matrix & Grid Initializer
// ==============================================================================
/**
 * Usage:
 *     Quickly creates a 2D matrix with variable (jagged) row sizes or rectangular
 *     dimensions with a default fill value.
 * 
 * Repository Reference:
 *     - CPP/0010_Variable-Sized-Arrays.cpp (Q10)
 */

template <typename T>
std::vector<std::vector<T>> createMatrix(size_t rows, size_t cols, T defaultValue = T()) {
    return std::vector<std::vector<T>>(rows, std::vector<T>(cols, defaultValue));
}

template <typename T>
std::vector<std::vector<T>> createJaggedMatrix(const std::vector<size_t>& rowSizes, T defaultValue = T()) {
    std::vector<std::vector<T>> matrix(rowSizes.size());
    for (size_t i = 0; i < rowSizes.size(); ++i) {
        matrix[i].assign(rowSizes[i], defaultValue);
    }
    return matrix;
}


// ==============================================================================
// [TMP-04] Custom Exception Boilerplate with Formatted Diagnostics
// ==============================================================================
/**
 * Usage:
 *     Copy-pasteable boilerplate for defining robust custom exceptions inheriting
 *     from std::exception with custom formatting.
 * 
 * Repository Reference:
 *     - CPP/0011_Inherited-Code.cpp (Q11)
 *     - CPP/0012_Exceptional-Server.cpp (Q12)
 */

class CompetitiveException : public std::exception {
private:
    std::string message;
    int errorCode;

public:
    CompetitiveException(const std::string& msg, int code = 0)
        : message(msg + " (code: " + std::to_string(code) + ")"), errorCode(code) {}

    const char* what() const noexcept override {
        return message.c_str();
    }

    int getErrorCode() const noexcept {
        return errorCode;
    }
};


// ==============================================================================
// [TMP-05] Binary Search Tree (BST) & Singly-Linked List Node Boilerplates
// ==============================================================================
/**
 * Usage:
 *     Clean, robust struct definitions for Tree and Linked List nodes with
 *     constructors and recursive cleanup helpers.
 * 
 * Repository Reference:
 *     - 30 DAYS OF CODE/Day-22-Binary-Search-Trees.cpp (Q62)
 *     - 30 DAYS OF CODE/Day-24-More-Linked-Lists.cpp (Q64)
 */

template <typename T>
struct BSTNode {
    T data;
    BSTNode* left;
    BSTNode* right;

    BSTNode(T val) : data(val), left(nullptr), right(nullptr) {}

    static void destroy(BSTNode* root) {
        if (!root) return;
        destroy(root->left);
        destroy(root->right);
        delete root;
    }
};

template <typename T>
struct SingleNode {
    T data;
    SingleNode* next;

    SingleNode(T val) : data(val), next(nullptr) {}

    static void destroy(SingleNode* head) {
        while (head) {
            SingleNode* temp = head;
            head = head->next;
            delete temp;
        }
    }
};


// ==============================================================================
// [TMP-06] Generic Vector / Array Pretty-Printer (Templates)
// ==============================================================================
/**
 * Usage:
 *     Serializes any std::vector<T> to a string or stream with custom delimiters.
 * 
 * Repository Reference:
 *     - 30 DAYS OF CODE/Day-21-Generics.cpp (Q61)
 */

template <typename T>
std::string vectorToString(const std::vector<T>& vec, const std::string& sep = " ") {
    std::stringstream ss;
    for (size_t i = 0; i < vec.size(); ++i) {
        ss << vec[i];
        if (i + 1 < vec.size()) {
            ss << sep;
        }
    }
    return ss.str();
}


// ==============================================================================
// [TMP-07] Hierarchical Tag / Scope Attribute Database Template
// ==============================================================================
/**
 * Usage:
 *     Lightweight, copy-pasteable manager for nested tag / attribute parsing.
 * 
 * Repository Reference:
 *     - CPP/0004_Attribute-Parser.cpp (Q4)
 */

class ScopeDatabase {
private:
    std::vector<std::string> stack;
    std::map<std::string, std::string> db;

public:
    void push(const std::string& tag) { stack.push_back(tag); }
    void pop() { if (!stack.empty()) stack.pop_back(); }

    std::string currentPath() const {
        std::string p = "";
        for (size_t i = 0; i < stack.size(); ++i) {
            p += stack[i];
            if (i + 1 < stack.size()) p += ".";
        }
        return p;
    }

    void set(const std::string& attr, const std::string& val) {
        db[currentPath() + "~" + attr] = val;
    }

    std::string get(const std::string& query, const std::string& defaultVal = "Not Found!") const {
        auto it = db.find(query);
        return (it != db.end()) ? it->second : defaultVal;
    }
};


// ==============================================================================
// [TMP-08] Static Lookup Dispatch Helper (Branchless Table)
// ==============================================================================
/**
 * Usage:
 *     O(1) mapping of small indices to string literals without branch prediction penalties.
 * 
 * Repository Reference:
 *     - CPP/0006_For-Loop.cpp (Q6)
 */

template <size_t N>
class StaticLookupTable {
private:
    const char* entries[N];
    const char* fallback;

public:
    template <typename... Args>
    StaticLookupTable(const char* fb, Args... args) : fallback(fb) {
        const char* initList[] = {args...};
        for (size_t i = 0; i < N; ++i) {
            entries[i] = initList[i];
        }
    }

    const char* lookup(size_t index) const {
        if (index < N) {
            return entries[index];
        }
        return fallback;
    }
};


// ==============================================================================
// SELF-TEST VERIFICATION SUITE
// ==============================================================================
int main() {
    std::cout << "[RUNNING] Templates.cpp Self-Test Suite...\n";

    // Test TMP-01: Fast IO invocation
    initFastIO();

    // Test TMP-02: Delimited Tokenizer
    std::string csv = "10,20,30,40,50";
    auto tokens = tokenizeDelimited<int>(csv, ',');
    assert(tokens.size() == 5);
    assert(tokens[0] == 10 && tokens[4] == 50);

    std::string words = "hello world from cpp";
    auto strTokens = tokenizeDelimited<std::string>(words, ' ');
    assert(strTokens.size() == 4);
    assert(strTokens[0] == "hello" && strTokens[3] == "cpp");

    // Test TMP-03: Matrix Allocators
    auto rectMat = createMatrix<int>(2, 3, 7);
    assert(rectMat.size() == 2 && rectMat[0].size() == 3);
    assert(rectMat[1][2] == 7);

    auto jaggedMat = createJaggedMatrix<int>({2, 4, 1}, 99);
    assert(jaggedMat.size() == 3);
    assert(jaggedMat[0].size() == 2 && jaggedMat[1].size() == 4 && jaggedMat[2].size() == 1);
    assert(jaggedMat[1][3] == 99);

    // Test TMP-04: Custom Exception
    try {
        throw CompetitiveException("TLE limit reached", 101);
    } catch (const CompetitiveException& e) {
        assert(e.getErrorCode() == 101);
        std::string errStr = e.what();
        assert(errStr.find("TLE limit reached") != std::string::npos);
    }

    // Test TMP-05: BST & List Nodes with safe cleanup
    BSTNode<int>* tree = new BSTNode<int>(10);
    tree->left = new BSTNode<int>(5);
    tree->right = new BSTNode<int>(15);
    assert(tree->left->data == 5 && tree->right->data == 15);
    BSTNode<int>::destroy(tree);

    SingleNode<int>* list = new SingleNode<int>(1);
    list->next = new SingleNode<int>(2);
    assert(list->next->data == 2);
    SingleNode<int>::destroy(list);

    // Test TMP-06: Vector To String
    std::vector<int> nums = {1, 2, 3, 4};
    assert(vectorToString(nums, ", ") == "1, 2, 3, 4");

    // Test TMP-07: Scope Database
    ScopeDatabase scopeDB;
    scopeDB.push("html");
    scopeDB.push("body");
    scopeDB.set("bgcolor", "white");
    assert(scopeDB.get("html.body~bgcolor") == "white");
    assert(scopeDB.get("html.body~color") == "Not Found!");
    scopeDB.pop();

    // Test TMP-08: Static Lookup Table
    StaticLookupTable<4> cardinal("UNKNOWN", "NORTH", "EAST", "SOUTH", "WEST");
    assert(std::string(cardinal.lookup(0)) == "NORTH");
    assert(std::string(cardinal.lookup(3)) == "WEST");
    assert(std::string(cardinal.lookup(10)) == "UNKNOWN");

    std::cout << "[SUCCESS] ALL Templates.cpp tests passed cleanly!\n";
    return 0;
}
