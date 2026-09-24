// 24/09/2026
// Easy
// Classes and Objects
// HackerRank: Define a class with private data and public methods to calculate scores.

#include <cstdio>
class Student {
private:
    int scores[5];
public:
    void input() {
        for (int i = 0; i < 5; ++i) {
            scanf("%d", &scores[i]);
        }
    }
    int calculateTotalScore() {
        int sum = 0;
        for (int i = 0; i < 5; ++i) {
            sum += scores[i];
        }
        return sum;
    }
};
int main() {
    int n;
    scanf("%d", &n);
    Student *s = new Student[n];
    for (int i = 0; i < n; i++) {
        s[i].input();
    }
    int kristen_score = s[0].calculateTotalScore();
    int count = 0;
    for (int i = 1; i < n; i++) {
        int total = s[i].calculateTotalScore();
        if (total > kristen_score) {
            count++;
        }
    }
    printf("%d\n", count);
    delete[] s;
    return 0;
}