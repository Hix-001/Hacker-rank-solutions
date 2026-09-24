/**
 * ================================================================================
 * 000_Algorithms.cpp - C++ Competitive Programming Algorithm Reference
 * ================================================================================
 * A curated, reusable reference of algorithmic techniques, pointer mechanics,
 * tree/graph traversals, string parsing, and problem-solving patterns extracted
 * from 16+ HackerRank C++ solutions.
 * 
 * Organized for quick retrieval during Codeforces, LeetCode, and HackerRank contests.
 * Every algorithm is directly grounded in problems from this repository.
 * 
 * TABLE OF CONTENTS:
 * --------------------------------------------------------------------------------
 * 1.  [ALG-01] Delimited String Tokenization & Integer Extraction (StringStream)
 * 2.  [ALG-02] Hierarchical Scope-Path Resolution & Tag Parsing (HRML Parser)
 * 3.  [ALG-03] Level-Order Tree Traversal via Queue-Based BFS
 * 4.  [ALG-04] Tree Height & Max Depth via Recursive Post-Order DFS
 * 5.  [ALG-05] In-Place Sorted Linked-List Deduplication & Memory Management
 * 6.  [ALG-06] Symmetrical Two-Pointer In-Place Sequence Reversal
 * 7.  [ALG-07] Multi-Variable Extrema Reduction & Branchless Comparison
 * 8.  [ALG-08] Linear Multi-Criteria Aggregation & Outlier Scoring
 * ================================================================================
 */

#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <map>
#include <queue>
#include <algorithm>
#include <cassert>
#include <cmath>

// ==============================================================================
// [ALG-01] Delimited String Tokenization & Integer Extraction (StringStream)
// ==============================================================================
/**
 * Algorithm Name:
 *     Delimited Token Extraction via std::stringstream
 * 
 * What It Does:
 *     Parses separated tokens (such as comma-delimited integers "23,4,56") from
 *     a formatted string into a strongly-typed std::vector<int> in O(N) time.
 * 
 * When To Recognize / Use:
 *     - Reading comma-separated values (CSV) or arbitrary character-delimited records.
 *     - When input lines have variable numbers of tokens on a single line.
 *     - Bypasses unsafe C-style strtok or manual character-by-character slicing.
 * 
 * Core Idea:
 *     Stream extraction operator `>>` parses typed primitives while discarding
 *     or extracting interstitial punctuation characters.
 * 
 * Repository References:
 *     - CPP/0013_StringStream.cpp (Q13)
 *     - CPP/0004_Attribute-Parser.cpp (Q4)
 */

std::vector<int> parseDelimitedInts(const std::string& str, char delimiter = ',') {
    std::stringstream ss(str);
    std::vector<int> result;
    int num;
    char ch;
    
    // Read the first integer, then repeatedly extract the delimiter followed by next integer
    while (ss >> num) {
        result.push_back(num);
        if (!(ss >> ch) || ch != delimiter) {
            // Delimiter was not the expected char or EOF reached
            break;
        }
    }
    return result;
}


// ==============================================================================
// [ALG-02] Hierarchical Scope-Path Resolution & Tag Parsing (HRML Parser)
// ==============================================================================
/**
 * Algorithm Name:
 *     Hierarchical Scope-Path Resolution (Nested Tag Lexer & Query Engine)
 * 
 * What It Does:
 *     Maintains a stack of nested tags to build fully-qualified hierarchical
 *     attribute keys (e.g., "tag1.tag2~attributeName") and indexes them into
 *     a hash map or balanced tree map for O(1) or O(log N) query lookup.
 * 
 * When To Recognize / Use:
 *     - Parsing nested markup (XML, HTML, HRML, JSON-like object hierarchies).
 *     - Answering path queries with scoped inheritance or nested definitions.
 *     - Handling tag entrance (<tag>) and tag exit (</tag>).
 * 
 * Core Idea:
 *     Use std::vector<std::string> as a scope stack. On an opening tag, push the tag name
 *     and construct the scope path joined by '.'. On a closing tag, pop from the stack.
 *     Store attributes with key format `scope + "~" + attr_name`.
 * 
 * Repository References:
 *     - CPP/0004_Attribute-Parser.cpp (Q4)
 */

class ScopePathResolver {
private:
    std::vector<std::string> tag_stack;
    std::map<std::string, std::string> attribute_db;

public:
    void openTag(const std::string& tagName, const std::vector<std::pair<std::string, std::string>>& attributes) {
        tag_stack.push_back(tagName);
        std::string current_scope = getCurrentScope();
        for (const auto& attr : attributes) {
            attribute_db[current_scope + "~" + attr.first] = attr.second;
        }
    }

    void closeTag() {
        if (!tag_stack.empty()) {
            tag_stack.pop_back();
        }
    }

    std::string getCurrentScope() const {
        std::string scope = "";
        for (size_t i = 0; i < tag_stack.size(); ++i) {
            scope += tag_stack[i];
            if (i + 1 < tag_stack.size()) {
                scope += ".";
            }
        }
        return scope;
    }

    bool query(const std::string& queryStr, std::string& outValue) const {
        auto it = attribute_db.find(queryStr);
        if (it != attribute_db.end()) {
            outValue = it->second;
            return true;
        }
        return false;
    }
};


// ==============================================================================
// [ALG-03] Level-Order Tree Traversal via Queue-Based BFS
// ==============================================================================
/**
 * Algorithm Name:
 *     Binary Tree Level-Order Traversal (Breadth-First Search)
 * 
 * What It Does:
 *     Visits all nodes in a binary tree level by level, from left to right,
 *     returning or printing the traversal order in O(N) time and O(W) space
 *     (where W is the maximum width of the tree).
 * 
 * When To Recognize / Use:
 *     - Tree printing / serialization by depth level.
 *     - Finding the shortest path in unweighted tree / graph structures.
 *     - Minimum depth or level-sum problems.
 * 
 * Core Idea:
 *     Use a FIFO queue (`std::queue<Node*>`). Push root, then loop while the queue
 *     is non-empty: pop front, record value, and enqueue non-null left and right children.
 * 
 * Repository References:
 *     - 30 DAYS OF CODE/Day-23-BST-Level-Order-Traversal.cpp (Q63)
 */

struct TreeNode {
    int data;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int val) : data(val), left(nullptr), right(nullptr) {}
};

std::vector<int> levelOrderTraversal(TreeNode* root) {
    std::vector<int> result;
    if (!root) return result;

    std::queue<TreeNode*> q;
    q.push(root);

    while (!q.empty()) {
        TreeNode* curr = q.front();
        q.pop();

        result.push_back(curr->data);

        if (curr->left)  q.push(curr->left);
        if (curr->right) q.push(curr->right);
    }
    return result;
}


// ==============================================================================
// [ALG-04] Tree Height & Max Depth via Recursive Post-Order DFS
// ==============================================================================
/**
 * Algorithm Name:
 *     Tree Height Computation via Recursive Divide-and-Conquer
 * 
 * What It Does:
 *     Computes the height of a binary search tree (number of edges on the longest
 *     path from root to leaf) in O(N) time and O(H) call stack space.
 * 
 * When To Recognize / Use:
 *     - Any binary tree depth, balance verification (AVL / Red-Black), or diameter calculation.
 * 
 * Core Idea:
 *     Height of a null pointer is -1 (so a single root node has height 0).
 *     Height(node) = 1 + max(Height(node->left), Height(node->right)).
 * 
 * Repository References:
 *     - 30 DAYS OF CODE/Day-22-Binary-Search-Trees.cpp (Q62)
 */

int getTreeHeight(TreeNode* root) {
    if (!root) {
        return -1; // Standard HackerRank convention: height of empty tree is -1
    }
    int leftHeight = getTreeHeight(root->left);
    int rightHeight = getTreeHeight(root->right);
    return 1 + std::max(leftHeight, rightHeight);
}


// ==============================================================================
// [ALG-05] In-Place Sorted Linked-List Deduplication & Memory Management
// ==============================================================================
/**
 * Algorithm Name:
 *     Sorted Singly-Linked List In-Place Deduplication
 * 
 * What It Does:
 *     Removes duplicate values from a sorted singly-linked list in O(N) time
 *     and O(1) auxiliary space, properly deallocating removed nodes via `delete`.
 * 
 * When To Recognize / Use:
 *     - Linked list unique filtering without creating a new list.
 *     - Direct pointer re-linking: `curr->next = curr->next->next`.
 *     - Demonstrates explicit memory deallocation in C++.
 * 
 * Repository References:
 *     - 30 DAYS OF CODE/Day-24-More-Linked-Lists.cpp (Q64)
 */

struct ListNode {
    int data;
    ListNode* next;
    ListNode(int d) : data(d), next(nullptr) {}
};

ListNode* removeDuplicates(ListNode* head) {
    if (!head) return nullptr;

    ListNode* current = head;
    while (current->next != nullptr) {
        if (current->data == current->next->data) {
            ListNode* duplicate = current->next;
            current->next = current->next->next;
            delete duplicate; // Avoid memory leaks in C++
        } else {
            current = current->next;
        }
    }
    return head;
}


// ==============================================================================
// [ALG-06] Symmetrical Two-Pointer In-Place Sequence Reversal
// ==============================================================================
/**
 * Algorithm Name:
 *     In-Place Two-Pointer Array/Vector Reversal
 * 
 * What It Does:
 *     Reverses an array, vector, or string in O(N) time and O(1) extra space
 *     by swapping elements from both ends moving towards the center.
 * 
 * When To Recognize / Use:
 *     - Palindrome verification, string reflection, array reversal.
 * 
 * Repository References:
 *     - CPP/0009_Arrays-Introduction.cpp (Q9)
 *     - CPP/0007_Strings.cpp (Q7)
 */

template <typename T>
void reverseSequence(std::vector<T>& arr) {
    if (arr.empty()) return;
    int left = 0;
    int right = static_cast<int>(arr.size()) - 1;
    while (left < right) {
        std::swap(arr[left], arr[right]);
        left++;
        right--;
    }
}


// ==============================================================================
// [ALG-07] Multi-Variable Extrema Reduction & Branchless Comparison
// ==============================================================================
/**
 * Algorithm Name:
 *     Pairwise / Initializer-List Extrema Reduction
 * 
 * What It Does:
 *     Finds the maximum (or minimum) across multiple arguments without deep nesting.
 * 
 * When To Recognize / Use:
 *     - Multiple coordinate bounding boxes, finding maximum score among fixed inputs.
 * 
 * Repository References:
 *     - CPP/0008_Functions.cpp (Q8)
 */

int maxOfFour(int a, int b, int c, int d) {
    return std::max({a, b, c, d});
}


// ==============================================================================
// [ALG-08] Linear Multi-Criteria Aggregation & Outlier Scoring
// ==============================================================================
/**
 * Algorithm Name:
 *     Structured Record Score Comparison & Rank Outlier Counting
 * 
 * What It Does:
 *     Evaluates aggregated scores across multiple records (e.g., student examination
 *     marks) and counts how many entities strictly exceed a benchmark entity's score.
 * 
 * When To Recognize / Use:
 *     - Leaderboards, relative rank determination, percentile calculations.
 * 
 * Repository References:
 *     - CPP/0016_Classes-and-Objects.cpp (Q16)
 */

struct StudentRecord {
    std::string name;
    std::vector<int> scores;

    int totalScore() const {
        int sum = 0;
        for (int s : scores) sum += s;
        return sum;
    }
};

int countExceedingBenchmark(const std::vector<StudentRecord>& students, size_t benchmarkIndex) {
    if (benchmarkIndex >= students.size()) return 0;
    int benchmarkScore = students[benchmarkIndex].totalScore();
    int count = 0;
    for (size_t i = 0; i < students.size(); ++i) {
        if (i == benchmarkIndex) continue;
        if (students[i].totalScore() > benchmarkScore) {
            count++;
        }
    }
    return count;
}


// ==============================================================================
// SELF-TEST VERIFICATION SUITE
// ==============================================================================
int main() {
    std::cout << "[RUNNING] Algorithms.cpp Self-Test Suite...\n";

    // Test ALG-01: StringStream Delimited Parsing
    std::string csv = "23,4,56,108";
    std::vector<int> parsed = parseDelimitedInts(csv);
    assert(parsed.size() == 4);
    assert(parsed[0] == 23 && parsed[1] == 4 && parsed[2] == 56 && parsed[3] == 108);

    // Test ALG-02: Scope-Path HRML Parser
    ScopePathResolver parser;
    parser.openTag("tag1", {{"value", "HelloWorld"}, {"id", "101"}});
    parser.openTag("tag2", {{"name", "NestedTag"}});
    
    std::string val;
    assert(parser.query("tag1.tag2~name", val) && val == "NestedTag");
    assert(parser.query("tag1~value", val) && val == "HelloWorld");
    assert(!parser.query("tag1~missing", val));

    parser.closeTag(); // Exits tag2
    // In HRML, once parsed, the attribute DB retains all scoped attributes for offline querying
    assert(parser.query("tag1.tag2~name", val) && val == "NestedTag");

    // Test ALG-03 & ALG-04: Tree BFS & Tree Height
    // Construct BST:
    //        3
    //       / |
    //      2   5
    //     /   / |
    //    1   4   6
    TreeNode* root = new TreeNode(3);
    root->left = new TreeNode(2);
    root->left->left = new TreeNode(1);
    root->right = new TreeNode(5);
    root->right->left = new TreeNode(4);
    root->right->right = new TreeNode(6);

    std::vector<int> bfs = levelOrderTraversal(root);
    std::vector<int> expected_bfs = {3, 2, 5, 1, 4, 6};
    assert(bfs == expected_bfs);

    assert(getTreeHeight(root) == 2);
    assert(getTreeHeight(nullptr) == -1);

    // Clean up tree memory
    delete root->right->right;
    delete root->right->left;
    delete root->right;
    delete root->left->left;
    delete root->left;
    delete root;

    // Test ALG-05: Linked List Deduplication
    // 1 -> 2 -> 2 -> 3 -> 3 -> 3 -> 4
    ListNode* head = new ListNode(1);
    head->next = new ListNode(2);
    head->next->next = new ListNode(2);
    head->next->next->next = new ListNode(3);
    head->next->next->next->next = new ListNode(3);
    head->next->next->next->next->next = new ListNode(3);
    head->next->next->next->next->next->next = new ListNode(4);

    head = removeDuplicates(head);
    std::vector<int> list_vals;
    ListNode* curr = head;
    while (curr) {
        list_vals.push_back(curr->data);
        ListNode* to_free = curr;
        curr = curr->next;
        delete to_free;
    }
    std::vector<int> expected_list = {1, 2, 3, 4};
    assert(list_vals == expected_list);

    // Test ALG-06: Symmetrical Array Reversal
    std::vector<int> arr = {1, 2, 3, 4, 5};
    reverseSequence(arr);
    assert((arr == std::vector<int>{5, 4, 3, 2, 1}));

    // Test ALG-07: Max of Four
    assert(maxOfFour(12, 45, 9, 30) == 45);

    // Test ALG-08: Student Score Exceeding Count
    std::vector<StudentRecord> students = {
        {"Kristen", {80, 80, 80, 80, 80}}, // Total = 400
        {"Alice",   {90, 90, 90, 90, 90}}, // Total = 450 (> 400)
        {"Bob",     {70, 70, 70, 70, 70}}, // Total = 350
        {"Charlie", {85, 85, 85, 85, 85}}  // Total = 425 (> 400)
    };
    assert(countExceedingBenchmark(students, 0) == 2);

    std::cout << "[SUCCESS] ALL Algorithms.cpp tests passed cleanly!\n";
    return 0;
}
