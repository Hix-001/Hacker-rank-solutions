// 03/10/2026
// Easy
// Inheritance
// HackerRank: Implement basic class inheritance and utilize protected access modifiers.

#include <cstdio>

using namespace std;

class Rectangle {
protected:
    int width;
    int height;
public:
    void display() {
        printf("%d %d\n", width, height);
    }
};

class RectangleArea : public Rectangle {
public:
    void read_input() {
        scanf("%d %d", &width, &height);
    }
    
    void display() {
        printf("%d\n", width * height);
    }
};

int main() {
    RectangleArea r_area;
    
    r_area.read_input();
    
    r_area.Rectangle::display();
    
    r_area.display();
    
    return 0;
}