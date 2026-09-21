// 21/09/2026
// Medium
// Exceptional Server
// HackerRank: Handle polymorphic C++ exception hierarchies using try-catch blocks.

#include <cstdio>
#include <vector>
#include <stdexcept>
#include <exception>
#include <new>

using namespace std;

class Server {
private:
    static int load;
public:
    static int compute(long long A, long long B) {
        load += 1;
        if(A < 0) {
            throw std::invalid_argument("A is negative");
        }
        vector<int> v(A, 0);
        int real = -1, cmplx = -1;
        if(B == 0) throw 0;
        real = (A/B)*real;
        int ans = v.at(B);
        return real + A - B*ans;
    }
    static int getLoad() {
        return load;
    }
};

int Server::load = 0;

int main() {
    int t;
    scanf("%d", &t);
    
    while (t--) {
        long long a, b;
        scanf("%lld %lld", &a, &b);
        
        try {
            int result = Server::compute(a, b);
            printf("%d\n", result);
        } catch (const std::bad_alloc& e) {
            printf("Not enough memory\n");
        } catch (const std::exception& e) {
            printf("Exception: %s\n", e.what());
        } catch (...) {
            printf("Other Exception\n");
        }
    }
    
    printf("%d\n", Server::getLoad());
    
    return 0;
}