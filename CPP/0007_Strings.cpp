// 16/09/2026
// Easy
// Strings
// HackerRank: Manipulate C++ std::string objects while interfacing with C-style I/O.

#include <cstdio>
#include <string>
using namespace std;
int main() {
    char a_buf[20000];
    char b_buf[20000];
    scanf("%s", a_buf);
    scanf("%s", b_buf);
    string a = a_buf;
    string b = b_buf;
    printf("%d %d\n", (int)a.size(), (int)b.size());
    string c = a + b;
    printf("%s\n", c.c_str());
    char temp = a[0];
    a[0] = b[0];
    b[0] = temp;
    printf("%s %s\n", a.c_str(), b.c_str());
    return 0;
}