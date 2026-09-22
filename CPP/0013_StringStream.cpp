// 22/09/2026
// Easy
// StringStream
// HackerRank: Parse a comma-separated string of integers into a vector using stringstream.

#include <cstdio>
#include <vector>
#include <string>
#include <sstream>
using namespace std;
vector<int> parseInts(string str) {
    stringstream ss(str);
    vector<int> result;
    int num;
    char ch;
    while (ss >> num) {
        result.push_back(num);
        ss >> ch;
    }    
    return result;
}
int main() {
    char buffer[800005];
    scanf("%s", buffer);
    vector<int> integers = parseInts(buffer);
    for (size_t i = 0; i < integers.size(); i++) {
        printf("%d\n", integers[i]);
    }
    return 0;
}