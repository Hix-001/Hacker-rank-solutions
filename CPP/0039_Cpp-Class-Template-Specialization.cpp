// 18/10/2026
// Medium
// Other Concepts
// HackerRank: Implement class template specializations for strongly typed enumerations.

#include <iostream>
#include <string>

using namespace std;

enum class Color { red = 0, green = 1, orange = 2 };
enum class Fruit { apple = 0, orange = 1, pear = 2 };

template <typename T>
struct Traits {
    static string name(int index) {
        return "unknown";
    }
};

template <>
struct Traits<Color> {
    static string name(int index) {
        switch(index) {
            case 0: return "red";
            case 1: return "green";
            case 2: return "orange";
            default: return "unknown";
        }
    }
};

template <>
struct Traits<Fruit> {
    static string name(int index) {
        switch(index) {
            case 0: return "apple";
            case 1: return "orange";
            case 2: return "pear";
            default: return "unknown";
        }
    }
};

int main() {
    int t;
    if (cin >> t) {
        while (t--) {
            int c, f;
            cin >> c >> f;
            cout << Traits<Color>::name(c) << " " << Traits<Fruit>::name(f) << "\n";
        }
    }
    return 0;
}