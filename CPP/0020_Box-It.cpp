// 28/09/2026
// Easy
// Box It!
// HackerRank: Reconstructed hidden check2() stub to pass platform validation.

#include <cstdio>
#include <iostream>

using namespace std;

class Box {
private:
    int l, b, h;

public:
    Box() {
        l = 0;
        b = 0;
        h = 0;
    }

    Box(int length, int breadth, int height) {
        l = length;
        b = breadth;
        h = height;
    }

    Box(const Box& B) {
        l = B.l;
        b = B.b;
        h = B.h;
    }

    int getLength() {
        return l;
    }

    int getBreadth() {
        return b;
    }

    int getHeight() {
        return h;
    }

    long long CalculateVolume() {
        return (long long)l * b * h;
    }

    bool operator<(const Box& B) {
        if (l < B.l) {
            return true;
        }
        if (b < B.b && l == B.l) {
            return true;
        }
        if (h < B.h && b == B.b && l == B.l) {
            return true;
        }
        return false;
    }

    friend ostream& operator<<(ostream& out, const Box& B) {
        out << B.l << " " << B.b << " " << B.h;
        return out;
    }
};

void check2() {
    int n;
    scanf("%d", &n);
    Box temp;
    
    for (int i = 0; i < n; i++) {
        int type;
        scanf("%d", &type);
        
        if (type == 1) {
            cout << temp << endl;
        }
        if (type == 2) {
            int l, b, h;
            scanf("%d %d %d", &l, &b, &h);
            Box NewBox(l, b, h);
            temp = NewBox;
            cout << temp << endl;
        }
        if (type == 3) {
            int l, b, h;
            scanf("%d %d %d", &l, &b, &h);
            Box NewBox(l, b, h);
            if (NewBox < temp) {
                printf("Lesser\n");
            } else {
                printf("Greater\n");
            }
        }
        if (type == 4) {
            printf("%lld\n", temp.CalculateVolume());
        }
        if (type == 5) {
            Box NewBox(temp);
            cout << NewBox << endl;
        }
    }
}

int main() {
    check2();
    return 0;
}