// 19/09/2026
// Easy
// Variable Sized Arrays
// HackerRank: Handle jagged arrays and multidimensional queries using std::vector.

#include <cstdio>
#include <vector>
using namespace std;
int main() {
    int n, q;
    scanf("%d %d", &n, &q);
    vector<vector<int>> arr(n);
    for (int i = 0; i < n; ++i) {
        int k;
        scanf("%d", &k);
        arr[i].resize(k);
        for (int j = 0; j < k; ++j) {
            scanf("%d", &arr[i][j]);
        }
    }
    for (int query = 0; query < q; ++query) {
        int i, j;
        scanf("%d %d", &i, &j);
        printf("%d\n", arr[i][j]);
    }
    return 0;
}