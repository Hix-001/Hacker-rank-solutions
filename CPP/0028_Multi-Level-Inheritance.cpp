// 06/10/2026
// Easy
// Inheritance
// HackerRank: Implement multi-level inheritance to chain methods across three class generations.

#include <cstdio>
using namespace std;

class Triangle {
public:
    void triangle() {
        printf("I am a triangle\n");
    }
};
class Isosceles : public Triangle {
public:
    void isosceles() {
        printf("I am an isosceles triangle\n");
    }
};
class Equilateral : public Isosceles {
public:
    void equilateral() {
        printf("I am an equilateral triangle\n");
    }
};
int main() {
    Equilateral eqr;    
    eqr.equilateral();
    eqr.isosceles();
    eqr.triangle();    
    return 0;
}