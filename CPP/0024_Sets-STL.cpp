// 02/10/2026
// Easy
// Sets-STL
// HackerRank: Utilize std::set to efficiently insert, delete, and query unique elements.

#include <cstdio>
#include <set>
using namespace std;

int main() {
    int q;
    scanf("%d", &q);    
    set<int> s;    
    while (q--) {
        int y, x;
        scanf("%d %d", &y, &x);        
        if (y == 1) {
            s.insert(x);
        } else if (y == 2) {
            s.erase(x);
        } else if (y == 3) {
            set<int>::iterator it = s.find(x);
            if (it != s.end()) {
                printf("Yes\n");
            } else {
                printf("No\n");
            }
        }
    }
    return 0;
}