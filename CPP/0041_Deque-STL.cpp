// 18/10/2026
// Medium
// STL / Deque-STL
// HackerRank: Implement an O(N) sliding window maximum algorithm using a double-ended queue.

#include <iostream>
#include <deque>

using namespace std;

void printKMax(int arr[], int n, int k) {
    deque<int> dq;
    
    for (int i = 0; i < n; i++) {
        while (!dq.empty() && dq.front() <= i - k) {
            dq.pop_front();
        }
        
        while (!dq.empty() && arr[dq.back()] <= arr[i]) {
            dq.pop_back();
        }
        
        dq.push_back(i);
        
        if (i >= k - 1) {
            cout << arr[dq.front()] << " ";
        }
    }
    cout << "\n";
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    int t;
    if (cin >> t) {
        while (t--) {
            int n, k;
            cin >> n >> k;
            
            int* arr = new int[n];
            for (int i = 0; i < n; i++) {
                cin >> arr[i];
            }
            
            printKMax(arr, n, k);
            delete[] arr;
        }
    }
    return 0;
}