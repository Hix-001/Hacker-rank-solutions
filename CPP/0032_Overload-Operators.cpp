// 10/10/2026
// Medium
// Overload Operators
// HackerRank: Overload the addition and stream insertion operators for a custom Complex number class.

#include <iostream>
#include <cstdio>

using namespace std;

class Complex {
public:
    int a, b;
};
// Overload the + operator
Complex operator+(const Complex& X, const Complex& Y) {
    Complex Z;
    Z.a = X.a + Y.a;
    Z.b = X.b + Y.b;
    return Z;
}
// Overload the << operator
ostream& operator<<(ostream& os, const Complex& C) {
    os << C.a << "+i" << C.b;
    return os;
}
int main() {
    Complex x, y;
    int a1, b1, a2, b2;   
    if (scanf("%d+i%d", &a1, &b1) == 2) {
        x.a = a1;
        x.b = b1;
    }    
    if (scanf("%d+i%d", &a2, &b2) == 2) {
        y.a = a2;
        y.b = b2;
    }
    
    Complex z = x + y;
    cout << z << endl;
    
    return 0;
}