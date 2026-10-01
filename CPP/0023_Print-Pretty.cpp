// 01/10/2026
// Medium
// Print Pretty
// HackerRank: Format floating-point numbers natively using strict C-style string buffers.

#include <cstdio>
using namespace std;

int main() {
    int t;
    scanf("%d", &t);    
    while (t--) {
        double a, b, c;
        scanf("%lf %lf %lf", &a, &b, &c);        
        printf("0x%llx\n", (long long)a);        
        char buf[64];
        int len = snprintf(buf, sizeof(buf), "%+.2f", b);
        for (int i = 0; i < 15 - len; ++i) {
            printf("_");
        }
        printf("%s\n", buf);        
        printf("%.9E\n", c);
    }    
    return 0;
}