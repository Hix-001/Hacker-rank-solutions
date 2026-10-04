// 04/10/2026
// Medium
// Accessing Inherited Functions
// HackerRank: Resolve multiple inheritance naming ambiguities using scope resolution.

#include <cstdio>
using namespace std;

class A {
public:
    A() { callA = 0; }
private:
    int callA;
    void inc() { callA++; }
protected:
    void func(int &a) {
        a = a * 2;
        inc();
    }
public:
    int getA() { return callA; }
};
class B {
public:
    B() { callB = 0; }
private:
    int callB;
    void inc() { callB++; }
protected:
    void func(int &a) {
        a = a * 3;
        inc();
    }
public:
    int getB() { return callB; }
};
class C {
public:
    C() { callC = 0; }
private:
    int callC;
    void inc() { callC++; }
protected:
    void func(int &a) {
        a = a * 5;
        inc();
    }
public:
    int getC() { return callC; }
};
class D : public A, public B, public C {
    int val;
public:
    D() { val = 1; }    
    void update_val(int new_val) {
        int temp = new_val;        
        while (temp % 2 == 0) {
            A::func(val);
            temp /= 2;
        }        
        while (temp % 3 == 0) {
            B::func(val);
            temp /= 3;
        }        
        while (temp % 5 == 0) {
            C::func(val);
            temp /= 5;
        }
    }    
    void check(int);
};
void D::check(int new_val) {
    update_val(new_val);
    printf("Value = %d\n", val);
    printf("A's func called %d times\n", getA());
    printf("B's func called %d times\n", getB());
    printf("C's func called %d times\n", getC());
}
int main() {
    D d;
    int new_val;   
    scanf("%d", &new_val);
    d.check(new_val);    
    return 0;
}
