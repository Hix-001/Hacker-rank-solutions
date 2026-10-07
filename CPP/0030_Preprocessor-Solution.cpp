// 08/10/2026
// Medium
// Preprocessor Solution
// HackerRank: Utilize preprocessor directives (#define, stringification) to alter code compilation.

#include <iostream>
#include <vector>
using namespace std;
// --- PREPROCESSOR MACROS ---
#define toStr(x) #x
#define io(v) cin >> v
#define FUNCTION(name, op) void name(int &a, int b) { if (b op a) a = b; }
#define INF 1000000000
#define foreach(v, i) for (int i = 0; i < v.size(); ++i)
// ---------------------------

// The macros above generate these two functions automatically:
FUNCTION(minimum, <)
FUNCTION(maximum, >)
int main() {
    // Standard fast I/O
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n; 
    cin >> n;
    vector<int> v(n);
    foreach(v, i) {
        io(v)[i];
    }
    int mn = INF;
    int mx = -INF;
    foreach(v, i) {
        minimum(mn, v[i]);
        maximum(mx, v[i]);
    }
    int ans = mx - mn;
    cout << toStr(Result =) << ' ' << ans << '\n';
    return 0;
}