/**
 * ================================================================================
 * 000_Patterns.cpp - C++ Competitive Programming Archetypes & Design Patterns
 * ================================================================================
 * A master reference of recurring problem-solving archetypes, structural design
 * patterns, and container manipulation idioms in C++. These patterns bridge the
 * gap between recognizing a problem statement and selecting the optimal C++
 * idiom, avoiding Time Limit Exceeded (TLE) and Memory Limit Exceeded (MLE).
 * 
 * Extracted and distilled from 16+ HackerRank C++ problems.
 * 
 * TABLE OF CONTENTS:
 * --------------------------------------------------------------------------------
 * 1.  [PAT-01] Jagged Dynamic Matrix & 2D Vector Allocation Pattern
 * 2.  [PAT-02] Hierarchical Scope Stack (Markup / Lexer Parsing Archetype)
 * 3.  [PAT-03] Defensive Exception Shield & Fault-Tolerant Processing
 * 4.  [PAT-04] Tree Pointer Traversal & Structural Divide-and-Conquer
 * 5.  [PAT-05] Queue-Driven Frontier Expansion (BFS Archetype)
 * 6.  [PAT-06] In-Place Pointer Splicing & Node Removal (Linked List Pattern)
 * 7.  [PAT-07] Static Dispatch Table & Branchless Predicate Lookup
 * 8.  [PAT-08] Two-Pointer Bidirectional Scanning & In-Place Swap
 * 9.  [PAT-09] Logarithmic STL Bounding Filter (std::lower_bound)
 * 10. [PAT-10] Polymorphic Factory & Heterogeneous Container Pattern
 * 11. [PAT-11] Unique Existence Probing & Streaming Filter (std::set)
 * 12. [PAT-12] Multi-Tier Lexicographical Tie-Breaking Pattern (std::tie)
 * 13. [PAT-13] Scope-Resolved Multiple Inheritance Delegation Pattern
 * ================================================================================
 */

#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <map>
#include <set>
#include <queue>
#include <algorithm>
#include <tuple>
#include <memory>
#include <cassert>

// ==============================================================================
// [PAT-01] Jagged Dynamic Matrix & 2D Vector Allocation Pattern
// ==============================================================================
/**
 * Pattern Name:
 *     Jagged / Variable-Sized 2D Vector Allocation
 * 
 * Recognition Cues:
 *     - Matrix where each row $i$ has a distinct length $k_i$ (non-rectangular).
 *     - Total elements $\sum k_i \le 10^5$, but declaring a fixed $N \times M$ grid
 *       would exceed memory limits ($O(N \cdot \max(k)) \gg$ RAM).
 * 
 * Mental Model:
 *     Allocate an outer vector of empty inner vectors: `std::vector<std::vector<int>> grid(n);`
 *     Then for each row $i$, either call `.resize(k)` and fill, or `.reserve(k)` and `.push_back()`.
 * 
 * Repository References:
 *     - CPP/0010_Variable-Sized-Arrays.cpp (Q10)
 */

class JaggedGrid {
private:
    std::vector<std::vector<int>> rows;

public:
    JaggedGrid(size_t numRows) : rows(numRows) {}

    void setRow(size_t rowIndex, const std::vector<int>& rowData) {
        if (rowIndex < rows.size()) {
            rows[rowIndex] = rowData;
        }
    }

    int query(size_t rowIndex, size_t colIndex) const {
        if (rowIndex < rows.size() && colIndex < rows[rowIndex].size()) {
            return rows[rowIndex][colIndex];
        }
        return -1; // Out of bounds indicator
    }

    size_t getRowCount() const { return rows.size(); }
};


// ==============================================================================
// [PAT-02] Hierarchical Scope Stack (Markup / Lexer Parsing Archetype)
// ==============================================================================
/**
 * Pattern Name:
 *     Hierarchical Scope Stack / State Machine
 * 
 * Recognition Cues:
 *     - Input has nested blocks, tags, brackets, or scopes (`<tag>`, `</tag>`, `{`, `}`).
 *     - Queries ask for properties defined within a qualified ancestral path:
 *       `parent.child~property`.
 * 
 * Mental Model:
 *     - Maintain an explicit vector acting as a stack of active scope identifiers.
 *     - When entering a scope (open tag): push tag name. Concatenate active stack
 *       elements to form current fully-qualified prefix.
 *     - When exiting a scope (close tag): pop tag name from the stack.
 *     - Store key-value pairs in a hash table or balanced search tree keyed by
 *       the complete composite path.
 * 
 * Repository References:
 *     - CPP/0004_Attribute-Parser.cpp (Q4)
 */

class ScopeStackParser {
private:
    std::vector<std::string> scopeStack;
    std::map<std::string, std::string> lookupTable;

public:
    void enterScope(const std::string& scopeName) {
        scopeStack.push_back(scopeName);
    }

    void exitScope() {
        if (!scopeStack.empty()) {
            scopeStack.pop_back();
        }
    }

    std::string getCompositePath() const {
        std::string path = "";
        for (size_t i = 0; i < scopeStack.size(); ++i) {
            path += scopeStack[i];
            if (i + 1 < scopeStack.size()) path += ".";
        }
        return path;
    }

    void recordAttribute(const std::string& key, const std::string& value) {
        std::string fullKey = getCompositePath() + "~" + key;
        lookupTable[fullKey] = value;
    }

    std::string query(const std::string& fullKey) const {
        auto it = lookupTable.find(fullKey);
        if (it != lookupTable.end()) {
            return it->second;
        }
        return "Not Found!";
    }
};


// ==============================================================================
// [PAT-03] Defensive Exception Shield & Fault-Tolerant Processing
// ==============================================================================
/**
 * Pattern Name:
 *     Stratified Exception Boundary / Circuit Breaker
 * 
 * Recognition Cues:
 *     - Code executes a batch of tasks where individual tasks may throw various
 *       types of exceptions (bad alloc, logic errors, invalid arguments, untyped errors).
 *     - A failure in one task must NOT abort the entire batch; errors must be logged
 *       or mapped to standardized output codes.
 * 
 * Mental Model:
 *     Wrap the dangerous invocation in a multi-stage `try-catch` ladder:
 *     1. Catch specific resource failures (`std::bad_alloc`).
 *     2. Catch standard library exceptions (`const std::exception&`).
 *     3. Catch wildcard (`...`) for untyped or foreign throws.
 * 
 * Repository References:
 *     - CPP/0012_Exceptional-Server.cpp (Q12)
 *     - CPP/0011_Inherited-Code.cpp (Q11)
 */

enum class ExecutionStatus { SUCCESS, OUT_OF_MEMORY, STANDARD_ERROR, UNKNOWN_ERROR };

struct TaskResult {
    ExecutionStatus status;
    std::string message;
    int payload;
};

template <typename Func>
TaskResult executeShielded(Func&& action) {
    try {
        int val = action();
        return {ExecutionStatus::SUCCESS, "OK", val};
    } catch (const std::bad_alloc&) {
        return {ExecutionStatus::OUT_OF_MEMORY, "Not enough memory", -1};
    } catch (const std::exception& e) {
        return {ExecutionStatus::STANDARD_ERROR, e.what(), -1};
    } catch (...) {
        return {ExecutionStatus::UNKNOWN_ERROR, "Unknown failure occurred", -1};
    }
}


// ==============================================================================
// [PAT-04] Tree Pointer Traversal & Structural Divide-and-Conquer
// ==============================================================================
/**
 * Pattern Name:
 *     Pointer-Based Tree Structural Recursion
 * 
 * Recognition Cues:
 *     - Binary search trees, expression trees, or hierarchical trees defined by pointer nodes.
 *     - Aggregate properties: height, size, subtree sums, validation (isBST).
 * 
 * Mental Model:
 *     Base Case: If `node == nullptr`, return identity value (0 for sum/size, -1 for edge-height, true for validity).
 *     Recursive Step:
 *         `leftRes = solve(node->left);`
 *         `rightRes = solve(node->right);`
 *     Combine: `return combine(leftRes, rightRes, node->val);`
 * 
 * Repository References:
 *     - 30 DAYS OF CODE/Day-22-Binary-Search-Trees.cpp (Q62)
 */

struct Node {
    int val;
    Node* left;
    Node* right;
    Node(int v) : val(v), left(nullptr), right(nullptr) {}
};

int countNodes(Node* root) {
    if (!root) return 0;
    return 1 + countNodes(root->left) + countNodes(root->right);
}

int calculateSubtreeSum(Node* root) {
    if (!root) return 0;
    return root->val + calculateSubtreeSum(root->left) + calculateSubtreeSum(root->right);
}


// ==============================================================================
// [PAT-05] Queue-Driven Frontier Expansion (BFS Archetype)
// ==============================================================================
/**
 * Pattern Name:
 *     Queue-Driven Frontier BFS
 * 
 * Recognition Cues:
 *     - Level-order processing, shortest unweighted distance, flood-fill.
 * 
 * Mental Model:
 *     Push initial frontier (root or start node).
 *     While queue is not empty: pop the next element, visit it, and enqueue all
 *     unvisited or valid neighbors/children.
 * 
 * Repository References:
 *     - 30 DAYS OF CODE/Day-23-BST-Level-Order-Traversal.cpp (Q63)
 */

std::vector<std::vector<int>> getLevels(Node* root) {
    std::vector<std::vector<int>> levels;
    if (!root) return levels;

    std::queue<Node*> q;
    q.push(root);

    while (!q.empty()) {
        size_t levelSize = q.size();
        std::vector<int> currentLevel;
        currentLevel.reserve(levelSize);

        for (size_t i = 0; i < levelSize; ++i) {
            Node* curr = q.front();
            q.pop();
            currentLevel.push_back(curr->val);

            if (curr->left) q.push(curr->left);
            if (curr->right) q.push(curr->right);
        }
        levels.push_back(currentLevel);
    }
    return levels;
}


// ==============================================================================
// [PAT-06] In-Place Pointer Splicing & Node Removal (Linked List Pattern)
// ==============================================================================
/**
 * Pattern Name:
 *     Sentinel / Two-Pointer Node Splicing
 * 
 * Recognition Cues:
 *     - Modifying, filtering, or deduplicating linked lists without allocating a new list.
 * 
 * Mental Model:
 *     Traverse using `curr`. When `curr->next` satisfies the removal predicate
 *     (e.g., `curr->data == curr->next->data`), extract `temp = curr->next`,
 *     re-link `curr->next = curr->next->next`, and delete `temp`.
 *     Advance `curr` ONLY when no deletion took place.
 * 
 * Repository References:
 *     - 30 DAYS OF CODE/Day-24-More-Linked-Lists.cpp (Q64)
 */

struct ListNodeItem {
    int data;
    ListNodeItem* next;
    ListNodeItem(int d) : data(d), next(nullptr) {}
};

void deleteValue(ListNodeItem*& head, int target) {
    // Handle head removals
    while (head && head->data == target) {
        ListNodeItem* toDelete = head;
        head = head->next;
        delete toDelete;
    }
    if (!head) return;

    ListNodeItem* curr = head;
    while (curr->next) {
        if (curr->next->data == target) {
            ListNodeItem* toDelete = curr->next;
            curr->next = curr->next->next;
            delete toDelete;
        } else {
            curr = curr->next;
        }
    }
}


// ==============================================================================
// [PAT-07] Static Dispatch Table & Branchless Predicate Lookup
// ==============================================================================
/**
 * Pattern Name:
 *     Static Array Lookup Table (Branchless Dispatch)
 * 
 * Recognition Cues:
 *     - Transforming small discrete integer IDs or conditions into strings/actions
 *       (e.g., 1 -> "one", 2 -> "two", ..., 9 -> "nine").
 *     - Eliminates deep if-else or switch ladders with $O(1)$ memory lookup.
 * 
 * Repository References:
 *     - CPP/0006_For-Loop.cpp (const char* words[] = {"", "one", ...})
 *     - CPP/0005_Conditional-Statements.cpp (Q5)
 */

const char* digitToEnglish(int digit) {
    static const char* lookup[] = {
        "zero", "one", "two", "three", "four",
        "five", "six", "seven", "eight", "nine"
    };
    if (digit >= 0 && digit <= 9) {
        return lookup[digit];
    }
    return (digit % 2 == 0) ? "even" : "odd";
}


// ==============================================================================
// [PAT-08] Two-Pointer Bidirectional Scanning & In-Place Swap
// ==============================================================================
/**
 * Pattern Name:
 *     Converging Two-Pointer Scan
 * 
 * Recognition Cues:
 *     - Array, string, or vector reversal, palindrome verification, partition (quicksort).
 * 
 * Mental Model:
 *     Initialize `left = 0`, `right = size - 1`.
 *     While `left < right`: process / swap elements, increment `left`, decrement `right`.
 * 
 * Repository References:
 *     - CPP/0007_Strings.cpp (Q7)
 *     - CPP/0009_Arrays-Introduction.cpp (Q9)
 */

bool isPalindrome(const std::string& str) {
    if (str.empty()) return true;
    int left = 0;
    int right = static_cast<int>(str.length()) - 1;
    while (left < right) {
        if (str[left] != str[right]) {
            return false;
        }
        left++;
        right--;
    }
    return true;
}


// ==============================================================================
// [PAT-09] Logarithmic STL Bounding Filter (std::lower_bound)
// ==============================================================================
/**
 * Pattern Name:
 *     Sorted STL Bound Querying
 * 
 * Recognition Cues:
 *     - Looking up positions, insertion points, or checking existence across many queries in sorted data.
 *     - Bypasses linear scanning O(N) with logarithmic O(log N) bisection.
 * 
 * Repository References:
 *     - CPP/0022_Lower-Bound-STL.cpp (Q22)
 */

struct BoundQueryResult {
    bool exactMatch;
    int index1Based;
    int valueFound;
};

BoundQueryResult binarySearchBounds(const std::vector<int>& sortedVec, int queryVal) {
    auto it = std::lower_bound(sortedVec.begin(), sortedVec.end(), queryVal);
    int idx = static_cast<int>(it - sortedVec.begin()) + 1;
    if (it != sortedVec.end()) {
        return {*it == queryVal, idx, *it};
    }
    return {false, idx, -1};
}


// ==============================================================================
// [PAT-10] Polymorphic Factory & Heterogeneous Container Pattern
// ==============================================================================
/**
 * Pattern Name:
 *     Polymorphic Factory & Heterogeneous Processing
 * 
 * Recognition Cues:
 *     - Problem processes heterogeneous entities (e.g. Students vs Professors)
 *       via a unified interface using base class pointers.
 * 
 * Mental Model:
 *     - Base class defines virtual interface.
 *     - Factory instantiates concrete derived objects based on type tags.
 *     - Container stores std::unique_ptr<Base> or pointers, processing in a single uniform loop.
 * 
 * Repository References:
 *     - CPP/0018_Virtual-Functions.cpp (Q18)
 */

class AbstractWorker {
public:
    virtual ~AbstractWorker() {}
    virtual std::string getTitle() const = 0;
    virtual int getProductivity() const = 0;
};

class Researcher : public AbstractWorker {
private:
    int papers;
public:
    Researcher(int p) : papers(p) {}
    std::string getTitle() const override { return "Researcher"; }
    int getProductivity() const override { return papers * 10; }
};

class Developer : public AbstractWorker {
private:
    int commits;
public:
    Developer(int c) : commits(c) {}
    std::string getTitle() const override { return "Developer"; }
    int getProductivity() const override { return commits * 2; }
};

std::unique_ptr<AbstractWorker> createWorker(int type, int metric) {
    if (type == 1) return std::unique_ptr<AbstractWorker>(new Researcher(metric));
    return std::unique_ptr<AbstractWorker>(new Developer(metric));
}


// ==============================================================================
// [PAT-11] Unique Existence Probing & Streaming Filter (std::set)
// ==============================================================================
/**
 * Pattern Name:
 *     Balanced Tree State Filter
 * 
 * Recognition Cues:
 *     - Stream of commands: insert element, delete element, query presence.
 *     - Requires unique storage and guaranteed O(log N) worst-case performance.
 * 
 * Repository References:
 *     - CPP/0024_Sets-STL.cpp (Q24)
 */

class StreamingSetFilter {
private:
    std::set<int> liveSet;
public:
    void executeCommand(int cmdType, int val, std::string& outResult) {
        if (cmdType == 1) {
            liveSet.insert(val);
        } else if (cmdType == 2) {
            liveSet.erase(val);
        } else if (cmdType == 3) {
            outResult = (liveSet.find(val) != liveSet.end()) ? "Yes" : "No";
        }
    }
    size_t activeCount() const { return liveSet.size(); }
};


// ==============================================================================
// [PAT-12] Multi-Tier Lexicographical Tie-Breaking Pattern (std::tie)
// ==============================================================================
/**
 * Pattern Name:
 *     Tuple-Driven Multi-Tier Comparison
 * 
 * Recognition Cues:
 *     - Ordering objects by primary key, breaking ties with secondary key, then tertiary key.
 *     - Eliminates nested if-else ladders with zero runtime overhead using std::tie.
 * 
 * Repository References:
 *     - CPP/0020_Box-It.cpp (Q20)
 */

struct PriorityItem {
    int priority;
    int timestamp;
    std::string name;

    bool operator<(const PriorityItem& other) const {
        return std::tie(other.priority, timestamp, name) <
               std::tie(priority, other.timestamp, other.name);
    }
};


// ==============================================================================
// [PAT-13] Scope-Resolved Multiple Inheritance Delegation Pattern
// ==============================================================================
/**
 * Pattern Name:
 *     Scope-Resolved Multi-Base Delegation
 * 
 * Recognition Cues:
 *     - Class combines capabilities of multiple independent base classes.
 *     - Resolves method name collisions explicitly by qualifying base namespaces.
 * 
 * Repository References:
 *     - CPP/0026_Accessing-Inherited-Functions.cpp (Q26)
 */

class EngineSubsystem {
public:
    int status() const { return 1; }
};

class SensorSubsystem {
public:
    int status() const { return 2; }
};

class IntegratedDrone : public EngineSubsystem, public SensorSubsystem {
public:
    int getEngineStatus() const { return EngineSubsystem::status(); }
    int getSensorStatus() const { return SensorSubsystem::status(); }
};


// ==============================================================================
// SELF-TEST VERIFICATION SUITE
// ==============================================================================
int main() {
    std::cout << "[RUNNING] Patterns.cpp Self-Test Suite...\n";

    // Test PAT-01: Jagged Dynamic Grid
    JaggedGrid grid(3);
    grid.setRow(0, {1, 2, 3});
    grid.setRow(1, {4, 5});
    grid.setRow(2, {6, 7, 8, 9, 10});
    assert(grid.query(0, 2) == 3);
    assert(grid.query(1, 1) == 5);
    assert(grid.query(2, 4) == 10);
    assert(grid.query(1, 4) == -1); // Out of bounds

    // Test PAT-02: Scope Stack Parser
    ScopeStackParser parser;
    parser.enterScope("window");
    parser.enterScope("frame");
    parser.recordAttribute("border", "solid");
    parser.recordAttribute("width", "100px");
    
    assert(parser.query("window.frame~border") == "solid");
    assert(parser.query("window.frame~width") == "100px");
    assert(parser.query("window.frame~color") == "Not Found!");

    parser.exitScope(); // Exit frame
    assert(parser.getCompositePath() == "window");

    // Test PAT-03: Defensive Exception Shield
    auto goodTask = []() { return 42; };
    auto memTask = []() -> int { throw std::bad_alloc(); };
    auto errorTask = []() -> int { throw std::runtime_error("Bad State"); };
    auto foreignTask = []() -> int { throw "Raw string throw"; };

    assert(executeShielded(goodTask).status == ExecutionStatus::SUCCESS);
    assert(executeShielded(memTask).status == ExecutionStatus::OUT_OF_MEMORY);
    assert(executeShielded(errorTask).status == ExecutionStatus::STANDARD_ERROR);
    assert(executeShielded(foreignTask).status == ExecutionStatus::UNKNOWN_ERROR);

    // Test PAT-04 & PAT-05: Tree Recursion & Level Order BFS
    //        10
    //       /  |
    //      5    20
    //          /  |
    //         15  30
    Node* root = new Node(10);
    root->left = new Node(5);
    root->right = new Node(20);
    root->right->left = new Node(15);
    root->right->right = new Node(30);

    assert(countNodes(root) == 5);
    assert(calculateSubtreeSum(root) == 80);

    auto levels = getLevels(root);
    assert(levels.size() == 3);
    assert((levels[0] == std::vector<int>{10}));
    assert((levels[1] == std::vector<int>{5, 20}));
    assert((levels[2] == std::vector<int>{15, 30}));

    delete root->right->right;
    delete root->right->left;
    delete root->right;
    delete root->left;
    delete root;

    // Test PAT-06: Linked List Splicing
    // 1 -> 2 -> 3 -> 2 -> 4 -> 2
    ListNodeItem* lhead = new ListNodeItem(1);
    lhead->next = new ListNodeItem(2);
    lhead->next->next = new ListNodeItem(3);
    lhead->next->next->next = new ListNodeItem(2);
    lhead->next->next->next->next = new ListNodeItem(4);
    lhead->next->next->next->next->next = new ListNodeItem(2);

    deleteValue(lhead, 2);
    std::vector<int> remaining;
    ListNodeItem* curr = lhead;
    while (curr) {
        remaining.push_back(curr->data);
        ListNodeItem* nxt = curr->next;
        delete curr;
        curr = nxt;
    }
    assert((remaining == std::vector<int>{1, 3, 4}));

    // Test PAT-07: Lookup Table
    assert(std::string(digitToEnglish(5)) == "five");
    assert(std::string(digitToEnglish(12)) == "even");
    assert(std::string(digitToEnglish(15)) == "odd");

    // Test PAT-08: Palindrome Two-Pointer
    assert(isPalindrome("racecar") == true);
    assert(isPalindrome("hacker") == false);
    assert(isPalindrome("") == true);

    // Test PAT-09: Logarithmic Bounding Filter
    std::vector<int> sortedArr = {10, 20, 30, 40, 50};
    auto r1 = binarySearchBounds(sortedArr, 30);
    assert(r1.exactMatch == true && r1.index1Based == 3);
    auto r2 = binarySearchBounds(sortedArr, 25);
    assert(r2.exactMatch == false && r2.index1Based == 3 && r2.valueFound == 30);

    // Test PAT-10: Polymorphic Factory
    auto w1 = createWorker(1, 5); // Researcher with 5 papers
    auto w2 = createWorker(2, 40); // Developer with 40 commits
    assert(w1->getTitle() == "Researcher" && w1->getProductivity() == 50);
    assert(w2->getTitle() == "Developer" && w2->getProductivity() == 80);

    // Test PAT-11: Streaming Set Filter
    StreamingSetFilter sf;
    std::string ans;
    sf.executeCommand(1, 100, ans);
    sf.executeCommand(1, 200, ans);
    sf.executeCommand(3, 100, ans);
    assert(ans == "Yes");
    sf.executeCommand(2, 100, ans);
    sf.executeCommand(3, 100, ans);
    assert(ans == "No");

    // Test PAT-12: Multi-Tier Tuple Tie Breaking
    PriorityItem taskA = {10, 100, "HighPriOld"};
    PriorityItem taskB = {10, 200, "HighPriNew"};
    PriorityItem taskC = {5, 50, "LowPri"};
    assert(taskA < taskB); // Same priority, earlier timestamp wins
    assert(taskA < taskC); // Higher priority wins

    // Test PAT-13: Multiple Inheritance Scope Resolution
    IntegratedDrone drone;
    assert(drone.getEngineStatus() == 1);
    assert(drone.getSensorStatus() == 2);

    std::cout << "[SUCCESS] ALL Patterns.cpp tests passed cleanly!\n";
    return 0;
}
