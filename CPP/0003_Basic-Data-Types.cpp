// 12/09/2026
// Easy
// Basic Data Types
// HackerRank: Read and print various basic data types using scanf/printf and format specifiers.

#include <cstdio>
int main() {
    int i;
    long l;
    char c;
    float f;
    double d;
    scanf("%d %ld %c %f %lf", &i, &l, &c, &f, &d);
    printf("%d\n", i);
    printf("%ld\n", l);
    printf("%c\n", c);
    printf("%.3f\n", f);
    printf("%.9lf\n", d);
    return 0;
}