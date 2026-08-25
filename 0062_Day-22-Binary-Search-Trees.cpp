// 23/07/2026
// 30 DAY OF CODE IN C++ [DAY 22]
// BINARY SEARCH TREE
/*HACKERRANK : Given a pointer to the root of a binary search tree, 
calculate and return the height of the tree, defined as the number of edges in the longest root-to-leaf path. */

#include <iostream>
#include <cstddef>

using namespace std;	

class Node{
    public:
        int data;
        Node *left;
        Node *right;
        Node(int d){
            data = d;
            left = NULL;
            right = NULL;
        }
};
class Solution{
    public:
  		Node* insert(Node* root, int data) {
            if(root == NULL) {
                return new Node(data);
            }
            else {
                Node* cur;
                if(data <= root->data){
                    cur = insert(root->left, data);
                    root->left = cur;
                }
                else{
                    cur = insert(root->right, data);
                    root->right = cur;
               }

               return root;
           }
        }


int getHeight(Node* root) {
    if (root == NULL)
        return -1;

    return 1 + max(getHeight(root->left), getHeight(root->right));
}
};
int main() {
    Solution myTree;
    Node* root = NULL;
    int t;
    int data;

    cin >> t;

    while(t-- > 0){
        cin >> data;
        root = myTree.insert(root, data);
    }
    int height = myTree.getHeight(root);
    cout << height;

    return 0;
}