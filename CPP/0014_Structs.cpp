// 23/09/2026
// Easy
// Structs
// HackerRank: Create a custom composite data type to store and print student details.

#include <cstdio>
#include <string>
using namespace std;

struct Student {
    int age;
    string first_name;
    string last_name;
    int standard;
};
int main() {
    Student st;
    char first_name_buf[55];
    char last_name_buf[55];
    scanf("%d", &st.age);
    scanf("%s", first_name_buf);
    scanf("%s", last_name_buf);
    scanf("%d", &st.standard);
    st.first_name = first_name_buf;
    st.last_name = last_name_buf;
    printf("%d %s %s %d\n", st.age, st.first_name.c_str(), st.last_name.c_str(), st.standard);
    return 0;
}