// 24/09/2026
// Easy
// Pointer
// HackerRank: Modify variables in place by passing memory addresses to a function.
#include <cstdio>
#include <cmath>
void update(int *a, int *b) {
    int sum = *a + *b;
    int diff = std::abs(*a - *b);
    *a = sum;
    *b = diff;
}
int main() {
    int a, b;
    scanf("%d %d", &a, &b);
    update(&a, &b);
    printf("%d\n%d\n", a, b);
    return 0;
}