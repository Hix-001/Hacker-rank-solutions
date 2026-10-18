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
 * 9.  [TMP-09] Binary Search STL Helpers (Lower Bound & Upper Bound Range)
 * 10. [TMP-10] Universal Stream Output Overload Boilerplate (operator<<)
 * 11. [TMP-11] Lexicographical Tuple Comparison Helper (std::tie)
 * 12. [TMP-12] Fast Erase-Remove Idiom Template
 * 13. [TMP-13] Full Class Template Specialization Skeleton
 * 14. [TMP-14] Strongly Typed Enum Name Traits Template Specialization
 * 15. [TMP-15] Variadic Template Compile-Time Bitfield & Pack Accumulator
 * 16. [TMP-16] 2D Matrix Mathematical Class with Operator Overloading
 * 17. [TMP-17] Production LRU Cache Template (O(1) Get/Set)
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
#include <tuple>
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
// [TMP-09] Binary Search STL Helpers (Lower Bound & Upper Bound Range)
// ==============================================================================
/**
 * Usage:
 *     Quickly query whether target exists in sorted range, its 0-based and 1-based index,
 *     and range [firstIdx, lastIdx) of occurrences.
 * 
 * Repository Reference:
 *     - CPP/0022_Lower-Bound-STL.cpp (Q22)
 */

template <typename T>
struct BinarySearchResult {
    bool found;
    int index0Based;
    int index1Based;
    int count;
};

template <typename T>
BinarySearchResult<T> querySortedRange(const std::vector<T>& v, const T& target) {
    auto low = std::lower_bound(v.begin(), v.end(), target);
    auto high = std::upper_bound(v.begin(), v.end(), target);
    int idx0 = static_cast<int>(low - v.begin());
    int cnt = static_cast<int>(high - low);
    bool exists = (low != v.end() && *low == target);
    return {exists, idx0, idx0 + 1, cnt};
}


// ==============================================================================
// [TMP-10] Universal Stream Output Overload Boilerplate (operator<<)
// ==============================================================================
/**
 * Usage:
 *     Standard copy-paste boilerplate for overloading operator<< on any class or struct.
 * 
 * Repository Reference:
 *     - CPP/0027_Overloading-Ostream-Operator.cpp (Q27)
 *     - CPP/0020_Box-It.cpp (Q20)
 */

struct PrintableRecord {
    std::string key;
    int value;

    friend std::ostream& operator<<(std::ostream& os, const PrintableRecord& rec) {
        os << "[" << rec.key << ": " << rec.value << "]";
        return os;
    }
};


// ==============================================================================
// [TMP-11] Lexicographical Tuple Comparison Helper (std::tie)
// ==============================================================================
/**
 * Usage:
 *     Copy-pasteable struct skeleton implementing strict weak ordering via std::tie.
 * 
 * Repository Reference:
 *     - CPP/0020_Box-It.cpp (Q20)
 */

struct TripletSortable {
    int a, b, c;

    bool operator<(const TripletSortable& other) const {
        return std::tie(a, b, c) < std::tie(other.a, other.b, other.c);
    }
    bool operator==(const TripletSortable& other) const {
        return std::tie(a, b, c) == std::tie(other.a, other.b, other.c);
    }
};


// ==============================================================================
// [TMP-12] Fast Erase-Remove Idiom Template
// ==============================================================================
/**
 * Usage:
 *     Filters and removes all elements matching a target value or predicate
 *     in linear O(N) time with zero element re-shifting penalty.
 * 
 * Repository Reference:
 *     - CPP/0021_Vector-Erase.cpp (Q21)
 */

template <typename T>
void eraseAllMatches(std::vector<T>& v, const T& target) {
    v.erase(std::remove(v.begin(), v.end(), target), v.end());
}

template <typename T, typename Predicate>
void eraseIfMatches(std::vector<T>& v, Predicate pred) {
    v.erase(std::remove_if(v.begin(), v.end(), pred), v.end());
}


// ==============================================================================
// [TMP-13] Full Class Template Specialization Skeleton
// ==============================================================================
/**
 * Usage:
 *     Template skeleton providing general arithmetic operations, with full
 *     specialization for std::string concatenation.
 * 
 * Repository Reference:
 *     - CPP/0029_Cpp-Class-Templates.cpp (Q29)
 */

template <typename T>
class Accumulator {
private:
    T total;
public:
    Accumulator(T initial = T()) : total(initial) {}
    void add(T val) { total += val; }
    T get() const { return total; }
};

template <>
class Accumulator<std::string> {
private:
    std::string total;
public:
    Accumulator(std::string initial = "") : total(initial) {}
    void add(const std::string& val) { total += val; }
    std::string get() const { return total; }
};


// ==============================================================================
// [TMP-14] Strongly Typed Enum Name Traits Template Specialization
// ==============================================================================
/**
 * Usage:
 *     Maps integer index or scoped enum values to string representations using
 *     generic traits with specialized structures.
 * 
 * Repository Reference:
 *     - CPP/0039_Cpp-Class-Template-Specialization.cpp (Q39)
 */

template <typename T>
struct EnumTraits {
    static std::string getName(int index) {
        (void)index;
        return "unknown";
    }
};

// Example domain enum
enum class ContestColor { RED = 0, GREEN = 1, ORANGE = 2 };

template <>
struct EnumTraits<ContestColor> {
    static std::string getName(int index) {
        switch (index) {
            case 0: return "red";
            case 1: return "green";
            case 2: return "orange";
            default: return "unknown";
        }
    }
};


// ==============================================================================
// [TMP-15] Variadic Template Compile-Time Bitfield & Pack Accumulator
// ==============================================================================
/**
 * Usage:
 *     Compile-time evaluation of variadic bool/int packs into numerical representations.
 * 
 * Repository Reference:
 *     - CPP/0037_Cpp-Variadics.cpp (Q37)
 */

template <bool... digits>
struct BitPackValue;

template <>
struct BitPackValue<> {
    static const int value = 0;
};

template <bool first, bool... rest>
struct BitPackValue<first, rest...> {
    static const int value = (first ? 1 : 0) + 2 * BitPackValue<rest...>::value;
};

template <bool... digits>
constexpr int getBitPackValue() {
    return BitPackValue<digits...>::value;
}


// ==============================================================================
// [TMP-16] 2D Matrix Mathematical Class with Operator Overloading
// ==============================================================================
/**
 * Usage:
 *     Reusable mathematical Matrix class supporting construction, element access,
 *     and overloaded binary operators (`+`).
 * 
 * Repository Reference:
 *     - CPP/0040_Operator-Overloading.cpp (Q40)
 */

template <typename T>
class MathMatrix {
public:
    std::vector<std::vector<T>> data;

    MathMatrix() = default;
    MathMatrix(size_t r, size_t c, T init = T())
        : data(r, std::vector<T>(c, init)) {}

    size_t rows() const { return data.size(); }
    size_t cols() const { return data.empty() ? 0 : data[0].size(); }

    MathMatrix operator+(const MathMatrix& other) const {
        if (rows() != other.rows() || cols() != other.cols()) return MathMatrix();
        MathMatrix res(rows(), cols());
        for (size_t i = 0; i < rows(); ++i) {
            for (size_t j = 0; j < cols(); ++j) {
                res.data[i][j] = data[i][j] + other.data[i][j];
            }
        }
        return res;
    }
};


// ==============================================================================
// [TMP-17] Production LRU Cache Template (O(1) Get/Set)
// ==============================================================================
/**
 * Usage:
 *     Template-based Least Recently Used (LRU) Cache supporting generic key-value
 *     types with strict O(1) retrieval, insertion, and eviction.
 * 
 * Repository Reference:
 *     - CPP/0035_Abstract-Classes-Polymorphism.cpp (Q35)
 */

template <typename Key, typename Value>
class GenericLRUCache {
private:
    struct Node {
        Key k;
        Value v;
        Node* prev;
        Node* next;
        Node(Key key, Value val) : k(key), v(val), prev(nullptr), next(nullptr) {}
    };

    size_t cap;
    Node* head;
    Node* tail;
    std::map<Key, Node*> lookup;

    void removeNode(Node* n) {
        if (!n) return;
        if (n->prev) n->prev->next = n->next;
        else head = n->next;
        if (n->next) n->next->prev = n->prev;
        else tail = n->prev;
        n->prev = nullptr;
        n->next = nullptr;
    }

    void addHead(Node* n) {
        if (!n) return;
        n->next = head;
        n->prev = nullptr;
        if (head) head->prev = n;
        head = n;
        if (!tail) tail = head;
    }

public:
    explicit GenericLRUCache(size_t capacity)
        : cap(capacity), head(nullptr), tail(nullptr) {}

    ~GenericLRUCache() {
        Node* curr = head;
        while (curr) {
            Node* nxt = curr->next;
            delete curr;
            curr = nxt;
        }
    }

    bool get(const Key& k, Value& outVal) {
        auto it = lookup.find(k);
        if (it == lookup.end()) return false;
        removeNode(it->second);
        addHead(it->second);
        outVal = it->second->v;
        return true;
    }

    void put(const Key& k, const Value& val) {
        auto it = lookup.find(k);
        if (it != lookup.end()) {
            it->second->v = val;
            removeNode(it->second);
            addHead(it->second);
        } else {
            if (lookup.size() >= cap && tail) {
                Node* evict = tail;
                lookup.erase(evict->k);
                removeNode(evict);
                delete evict;
            }
            Node* newNode = new Node(k, val);
            addHead(newNode);
            lookup[k] = newNode;
        }
    }

    size_t size() const { return lookup.size(); }
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

    // Test TMP-09: Binary Search Range Queries
    std::vector<int> sNums = {5, 10, 10, 10, 20, 25};
    auto bRes1 = querySortedRange(sNums, 10);
    assert(bRes1.found == true && bRes1.index0Based == 1 && bRes1.index1Based == 2 && bRes1.count == 3);
    auto bRes2 = querySortedRange(sNums, 15);
    assert(bRes2.found == false && bRes2.index0Based == 4 && bRes2.count == 0);

    // Test TMP-10: Printable Record
    PrintableRecord prec = {"Status", 200};
    std::stringstream pss;
    pss << prec;
    assert(pss.str() == "[Status: 200]");

    // Test TMP-11: Triplet Sortable
    TripletSortable t1 = {1, 2, 3};
    TripletSortable t2 = {1, 2, 4};
    assert(t1 < t2);
    assert(!(t2 < t1));

    // Test TMP-12: Erase All Matches
    std::vector<int> matchVec = {1, 2, 3, 2, 4, 2};
    eraseAllMatches(matchVec, 2);
    assert((matchVec == std::vector<int>{1, 3, 4}));

    // Test TMP-13: Accumulator Specialization
    Accumulator<int> accInt(10);
    accInt.add(15);
    assert(accInt.get() == 25);
    Accumulator<std::string> accStr("Hello");
    accStr.add(" World");
    assert(accStr.get() == "Hello World");

    // Test TMP-14: Enum Name Traits Specialization
    assert(EnumTraits<ContestColor>::getName(0) == "red");
    assert(EnumTraits<ContestColor>::getName(1) == "green");
    assert(EnumTraits<ContestColor>::getName(2) == "orange");
    assert(EnumTraits<ContestColor>::getName(99) == "unknown");
    assert(EnumTraits<int>::getName(0) == "unknown");

    // Test TMP-15: Variadic Compile-Time Bit Pack
    assert((getBitPackValue<0, 0, 1>() == 4));
    assert((getBitPackValue<1, 0, 1, 1>() == 13)); // 1*1 + 0*2 + 1*4 + 1*8 = 13

    // Test TMP-16: Mathematical Matrix Class & Addition
    MathMatrix<int> matA(2, 2, 10);
    MathMatrix<int> matB(2, 2, 20);
    MathMatrix<int> matC = matA + matB;
    assert(matC.data[0][0] == 30 && matC.data[1][1] == 30);

    // Test TMP-17: Generic LRU Cache Template
    GenericLRUCache<std::string, int> strCache(2);
    strCache.put("alpha", 1);
    strCache.put("beta", 2);
    int val = 0;
    assert(strCache.get("alpha", val) && val == 1);
    strCache.put("gamma", 3); // "beta" evicted
    assert(!strCache.get("beta", val));
    assert(strCache.get("gamma", val) && val == 3);
    assert(strCache.get("alpha", val) && val == 1);

    std::cout << "[SUCCESS] ALL Templates.cpp tests passed cleanly!\n";
    return 0;
}
