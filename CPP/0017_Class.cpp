// 25/09/2026
// Easy
// Class
// HackerRank: Implement encapsulation using private data members and public getters/setters.

#include <cstdio>
#include <string>
#include <sstream>
using namespace std;

class Student {
private:
    int age;
    string first_name;
    string last_name;
    int standard;
public:
    void set_age(int a) {
        age = a;
    }
    int get_age() {
        return age;
    }
    void set_first_name(string fn) {
        first_name = fn;
    }
    string get_first_name() {
        return first_name;
    } 
    void set_last_name(string ln) {
        last_name = ln;
    }
    string get_last_name() {
        return last_name;
    }
    void set_standard(int s) {
        standard = s;
    } 
    int get_standard() {
        return standard;
    } 
    string to_string() {
        stringstream ss;
        ss << age << "," << first_name << "," << last_name << "," << standard;
        return ss.str();
    }
};
int main() {
    int age, standard;
    char first_name_buf[55], last_name_buf[55];
    scanf("%d", &age);
    scanf("%s", first_name_buf);
    scanf("%s", last_name_buf);
    scanf("%d", &standard);   
    Student st;
    st.set_age(age);
    st.set_standard(standard);
    st.set_first_name(first_name_buf);
    st.set_last_name(last_name_buf);   
    printf("%d\n", st.get_age());
    printf("%s, %s\n", st.get_last_name().c_str(), st.get_first_name().c_str());
    printf("%d\n", st.get_standard());
    printf("\n");
    printf("%s\n", st.to_string().c_str());  
    return 0;
}