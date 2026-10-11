// 11/10/2026
// Easy
// Maps-STL
// HackerRank: Utilize std::map to insert, erase, and query key-value pairs efficiently.

#include <iostream>
#include <string>
#include <map>

using namespace std;

int main() {
    // Optimize standard I/O operations for performance
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    int q;
    if (cin >> q) {
        map<string, int> marks;
        
        while (q--) {
            int type;
            cin >> type;
            
            if (type == 1) {
                string x;
                int y;
                cin >> x >> y;
                // Add to existing marks or implicitly initialize to 0 then add
                marks[x] += y;
            } 
            else if (type == 2) {
                string x;
                cin >> x;
                marks.erase(x);
            } 
            else if (type == 3) {
                string x;
                cin >> x;
                
                auto it = marks.find(x);
                if (it != marks.end()) {
                    cout << it->second << '\n';
                } else {
                    cout << 0 << '\n';
                }
            }
        }
    }
    
    return 0;
}