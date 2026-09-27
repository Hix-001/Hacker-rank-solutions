// 27/09/2026
// Easy
// STL
// HackerRank: Sort a sequence of integers using std::vector and std::sort.

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
    sort(v.begin(), v.end());
    for (int i = 0; i < n; ++i) {
        printf("%d ", v[i]);
    }
    printf("\n");
    return 0;
}