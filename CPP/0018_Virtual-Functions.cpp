// 26/09/2026
// Medium
// Virtual Functions
// HackerRank: Implement runtime polymorphism using abstract base classes and virtual functions.

#include <cstdio>
#include <string>

using namespace std;

class Person {
protected:
    string name;
    int age;
public:
    virtual void getdata() = 0;
    virtual void putdata() = 0;
    virtual ~Person() {}
};

class Professor : public Person {
private:
    int publications;
    int cur_id;
    static int id_counter;
public:
    Professor() {
        cur_id = ++id_counter;
    }
    void getdata() override {
        char name_buf[105];
        scanf("%s %d %d", name_buf, &age, &publications);
        name = name_buf;
    }
    void putdata() override {
        printf("%s %d %d %d\n", name.c_str(), age, publications, cur_id);
    }
};
int Professor::id_counter = 0;

class Student : public Person {
private:
    int marks[6];
    int cur_id;
    static int id_counter;
public:
    Student() {
        cur_id = ++id_counter;
    }
    void getdata() override {
        char name_buf[105];
        scanf("%s %d", name_buf, &age);
        name = name_buf;
        for(int i = 0; i < 6; i++) {
            scanf("%d", &marks[i]);
        }
    }
    void putdata() override {
        int sum = 0;
        for(int i = 0; i < 6; i++) {
            sum += marks[i];
        }
        printf("%s %d %d %d\n", name.c_str(), age, sum, cur_id);
    }
};
int Student::id_counter = 0;

int main() {
    int n, val;
    scanf("%d", &n);
    
    Person **per = new Person*[n];

    for(int i = 0; i < n; i++) {
        scanf("%d", &val);
        if(val == 1) {
            per[i] = new Professor;
        } else {
            per[i] = new Student;
        }
        per[i]->getdata();
    }

    for(int i = 0; i < n; i++) {
        per[i]->putdata();
    }
    
    for(int i = 0; i < n; i++) {
        delete per[i];
    }
    delete[] per;
    
    return 0;
}