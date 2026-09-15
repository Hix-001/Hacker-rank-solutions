// 15/09/2026
// Easy
// For Loop
// HackerRank: Iterate through a range using a for loop and apply conditional logic.

#include <cstdio>
int main() {
    int a, b;
    scanf("%d", &a);
    scanf("%d", &b);
    const char* words[] = {"", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};
    for (int n = a; n <= b; ++n) {
        if (n >= 1 && n <= 9) {
            printf("%s\n", words[n]);
        } else {
            if (n % 2 == 0) {
                printf("even\n");
            } else {
                printf("odd\n");
            }
        }
    }
    return 0;
}