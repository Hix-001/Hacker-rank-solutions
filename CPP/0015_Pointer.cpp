// 24/09/2026
// Easy
// Pointer
// HackerRank: Modify variables in place by passing memory addresses to a function.

#include <iostream>
#include <algorithm>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int a, b;
    if (!(std::cin >> a >> b))
        return 1;

    std::cout << a + b << '\n'
              << std::abs(a - b) << '\n';
}
