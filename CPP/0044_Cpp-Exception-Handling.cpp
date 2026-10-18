// 18/10/2026
// Medium
// Debugging
// HackerRank: Intercept and process std::invalid_argument exceptions using try-catch blocks.

#include <iostream>
#include <stdexcept>

using namespace std;

int largest_proper_divisor(int n) {
    if (n == 0) {
        throw invalid_argument("largest proper divisor is not defined for n=0");
    }
    if (n == 1) {
        throw invalid_argument("largest proper divisor is not defined for n=1");
    }
    for (int i = n / 2; i >= 1; --i) {
        if (n % i == 0) {
            return i;
        }
    }
    return -1;
}

void process_input(int n) {
    try {
        int d = largest_proper_divisor(n);
        cout << "result=" << d << "\n";
    } catch (const invalid_argument& e) {
        cout << e.what() << "\n";
    }
    cout << "returning control flow to caller\n";
}

int main() {
    int n;
    if (cin >> n) {
        process_input(n);
    }
    return 0;
}
