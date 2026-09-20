// 20/09/2026
// Medium
// Inherited Code
// HackerRank: Define a custom exception class to interface with a locked validation stub.

#include <cstdio>
#include <cstring>

class BadLengthException {
    int length;
public:
    BadLengthException(int n) {
        length = n;
    }
    int what() {
        return length;
    }
};

bool checkUsername(const char* username) {
    bool isValid = true;
    int n = strlen(username);
    if(n < 5) {
        throw BadLengthException(n);
    }
    for(int i = 0; i < n - 1; i++) {
        if(username[i] == 'w' && username[i+1] == 'w') {
            isValid = false;
        }
    }
    return isValid;
}

int main() {
    int t;
    scanf("%d", &t);
    while(t--) {
        char username[200];
        scanf("%s", username);
        try {
            bool isValid = checkUsername(username);
            if(isValid) {
                printf("Valid\n");
            } else {
                printf("Invalid\n");
            }
        } catch (BadLengthException e) {
            printf("Too short: %d\n", e.what());
        }
    }
    return 0;
}