// 30/09/2026
// Easy
// STL
// HackerRank: Search a sorted array using binary search via std::lower_bound.

#include <cstdio>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    scanf("%d", &n);
    vector<int> v(n);
    for (int i = 0; i < n; ++i) {
        scanf("%d", &v[i]);
    }
    int q;
    scanf("%d", &q);
    for (int i = 0; i < q; ++i) {
        int y;
        scanf("%d", &y);
        // lower_bound returns an iterator to the first element >= y
        auto it = lower_bound(v.begin(), v.end(), y);
        // Calculate the 1-based index
        int index = (it - v.begin()) + 1;
        // Check if the element at the iterator is exactly y
        if (it != v.end() && *it == y) {
            printf("Yes %d\n", index);
        } else {
            printf("No %d\n", index);
        }
    }
    return 0;
}