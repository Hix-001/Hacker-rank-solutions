// 29/09/2026
// Easy
// STL
// HackerRank: Manipulate dynamic arrays using the vector::erase iterator method.

#include <cstdio>
#include <vector>
using namespace std;

int main() {
    int n;
    scanf("%d", &n);
    vector<int> v(n);
    for (int i = 0; i < n; ++i) {
        scanf("%d", &v[i]);
    }
    int x;
    scanf("%d", &x);
    v.erase(v.begin() + x - 1);
    int a, b;
    scanf("%d %d", &a, &b);
    v.erase(v.begin() + a - 1, v.begin() + b - 1);
    printf("%d\n", (int)v.size());
    for (size_t i = 0; i < v.size(); ++i) {
        printf("%d ", v[i]);
    }
    printf("\n");
    return 0;
}