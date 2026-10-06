// 05/10/2026
// Easy
// Debugging / Overloading Ostream Operator
// HackerRank: Overload the insertion operator to format and print class objects natively.

#include <iostream>
#include <cstdio>
#include <string>
using namespace std;
class Person {
public:
    Person(const string& first_name, const string& last_name) {
        first_name_ = first_name;
        last_name_ = last_name;
    }
    const string& get_first_name() const {
        return first_name_;
    }
    const string& get_last_name() const {
        return last_name_;
    }
private:
    string first_name_;
    string last_name_;
};
ostream& operator<<(ostream& os, const Person& p) {
    os << "first_name=" << p.get_first_name() << ",last_name=" << p.get_last_name();
    return os;
}
int main() {
    char fn[20], ln[20], ev[20];
    if (scanf("%s %s %s", fn, ln, ev) == 3) {
        string first_name(fn);
        string last_name(ln);
        string event(ev);        
        Person p(first_name, last_name);        
        cout << p << " " << event << endl;
    }    
    return 0;
}