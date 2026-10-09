// 09/10/2026
// Easy
// Inheritance Introduction
// HackerRank: Introduce OOP single inheritance by accessing a base class function from a derived class object.

#include <iostream>
using namespace std;

class Triangle {
public:
    void triangle() {
        cout << "I am a triangle\n";
    }
};
class Isosceles : public Triangle {
public:
    void isosceles() {
        cout << "I am an isosceles triangle\n";
    }    
    void description() {
        cout << "In an isosceles triangle two sides are equal\n";
    }
};
int main() {
    Isosceles isc;    
    isc.isosceles();
    isc.description();
    isc.triangle();
    return 0;
}