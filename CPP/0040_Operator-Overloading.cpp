// 18/10/2026
// Medium
// Other Concepts
// HackerRank: Overload the + operator to perform 2D matrix addition.

#include <iostream>
#include <vector>

using namespace std;

class Matrix {
public:
    vector<vector<int>> a;
    
    Matrix operator+(const Matrix& y) {
        Matrix result;
        for (size_t i = 0; i < this->a.size(); i++) {
            vector<int> row_result;
            for (size_t j = 0; j < this->a[0].size(); j++) {
                row_result.push_back(this->a[i][j] + y.a[i][j]);
            }
            result.a.push_back(row_result);
        }
        return result;
    }
};

int main() {
    int cases, k;
    if (cin >> cases) {
        for (k = 0; k < cases; k++) {
            Matrix x;
            Matrix y;
            Matrix result;
            int n, m, i, j;
            cin >> n >> m;
            
            for (i = 0; i < n; i++) {
                vector<int> b;
                int num;
                for (j = 0; j < m; j++) {
                    cin >> num;
                    b.push_back(num);
                }
                x.a.push_back(b);
            }
            
            for (i = 0; i < n; i++) {
                vector<int> b;
                int num;
                for (j = 0; j < m; j++) {
                    cin >> num;
                    b.push_back(num);
                }
                y.a.push_back(b);
            }
            
            result = x + y;
            
            for (i = 0; i < n; i++) {
                for (j = 0; j < m; j++) {
                    cout << result.a[i][j] << " ";
                }
                cout << "\n";
            }
        }
    }
    return 0;
}