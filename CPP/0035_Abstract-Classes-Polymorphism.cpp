// 17/10/2026
// Hard
// Abstract Classes - Polymorphism
// HackerRank: Implement an LRU Cache using a map, doubly linked list, and polymorphism.

#include <iostream>
#include <vector>
#include <map>
#include <string>
#include <algorithm>
#include <set>
#include <cassert>

using namespace std;

// --- RECONSTRUCTED HIDDEN STUB ---
struct Node {
    Node* next;
    Node* prev;
    int value;
    int key;
    Node(Node* p, Node* n, int k, int val) : prev(p), next(n), key(k), value(val) {};
    Node(int k, int val) : prev(NULL), next(NULL), key(k), value(val) {};
};

class Cache {
protected:
    map<int, Node*> mp; // map the key to the node in the linked list
    int cp;             // capacity
    Node* tail;         // double linked list tail pointer
    Node* head;         // double linked list head pointer
    virtual void set(int, int) = 0; // set function
    virtual int get(int) = 0;       // get function
};
// ---------------------------------

class LRUCache : public Cache {
private:
    void moveToHead(Node* node) {
        if (node == head) {
            return;
        }
        
        // Detach node from current position
        if (node->prev) {
            node->prev->next = node->next;
        }
        if (node->next) {
            node->next->prev = node->prev;
        }
        
        // If the detached node was the tail, update the tail
        if (node == tail) {
            tail = node->prev;
        }
        
        // Move to head
        node->next = head;
        node->prev = nullptr;
        
        if (head) {
            head->prev = node;
        }
        
        head = node;
        
        // If list was empty (shouldn't happen here, but safe practice)
        if (tail == nullptr) {
            tail = head;
        }
    }

public:
    LRUCache(int capacity) {
        cp = capacity;
        head = nullptr;
        tail = nullptr;
    }
    
    void set(int key, int value) override {
        // Case 1: Key already exists. Update value and move to head.
        if (mp.find(key) != mp.end()) {
            Node* node = mp[key];
            node->value = value;
            moveToHead(node);
        } 
        // Case 2: Key does not exist. Insert new node.
        else {
            Node* newNode = new Node(key, value);
            mp[key] = newNode;
            
            if (head == nullptr) {
                // List is currently empty
                head = tail = newNode;
            } else {
                // Insert at head
                newNode->next = head;
                head->prev = newNode;
                head = newNode;
            }
            
            // Handle capacity overflow
            if (mp.size() > cp) {
                // Remove tail from map
                mp.erase(tail->key);
                
                // Remove tail from linked list
                Node* oldTail = tail;
                tail = tail->prev;
                if (tail) {
                    tail->next = nullptr;
                }
                
                // Free memory
                delete oldTail;
            }
        }
    }
    
    int get(int key) override {
        if (mp.find(key) != mp.end()) {
            Node* node = mp[key];
            moveToHead(node);
            return node->value;
        }
        return -1;
    }
};

int main() {
    int n, capacity, i;
    if (cin >> n >> capacity) {
        LRUCache l(capacity);
        for (i = 0; i < n; i++) {
            string command;
            cin >> command;
            if (command == "get") {
                int key;
                cin >> key;
                cout << l.get(key) << endl;
            } else if (command == "set") {
                int key, value;
                cin >> key >> value;
                l.set(key, value);
            }
        }
    }
    return 0;
}