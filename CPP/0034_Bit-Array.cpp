// 12/10/2026
// Hard
// Bit Array
// HackerRank: Count unique elements in a PRNG sequence using Floyd's Cycle-Finding Algorithm.

#include <cstdio>

using namespace std;

int main() {
    unsigned int n, s, p, q;
    
    if (scanf("%u %u %u %u", &n, &s, &p, &q) == 4) {
        // 0x7FFFFFFF is the bitmask equivalent of modulo 2^31
        unsigned int tortoise = s & 0x7FFFFFFF;
        unsigned int hare = s & 0x7FFFFFFF;
        unsigned int distinct = n;
        
        for (unsigned int i = 1; i < n; i++) {
            // Advance tortoise by 1 step
            tortoise = (tortoise * (unsigned long long)p + q) & 0x7FFFFFFF;
            
            // Advance hare by 2 steps
            hare = (hare * (unsigned long long)p + q) & 0x7FFFFFFF;
            hare = (hare * (unsigned long long)p + q) & 0x7FFFFFFF;
            
            // Cycle detected
            if (tortoise == hare) {
                unsigned int mu = 0;
                tortoise = s & 0x7FFFFFFF;
                
                // Find the start of the cycle
                while (tortoise != hare) {
                    tortoise = (tortoise * (unsigned long long)p + q) & 0x7FFFFFFF;
                    hare = (hare * (unsigned long long)p + q) & 0x7FFFFFFF;
                    mu++;
                }
                
                // Find the length of the cycle
                unsigned int lambda = 1;
                hare = (tortoise * (unsigned long long)p + q) & 0x7FFFFFFF;
                while (tortoise != hare) {
                    hare = (hare * (unsigned long long)p + q) & 0x7FFFFFFF;
                    lambda++;
                }
                
                // Verify the cycle exists entirely within the N constraints
                unsigned int total = mu + lambda;
                if (total < n) {
                    distinct = total;
                }
                break;
            }
        }
        
        printf("%u\n", distinct);
    }
    
    return 0;
}