//22/07/26
//30 DAY OF CODE IN PYTHON [DAY 21]
//GENERICS
// HackerRank: Implement a generic printArray function using C++ Templates.

#include <iostream>
#include <vector>
#include <string>

using namespace std;

template <typename T>
void printArray(vector<T> arr) {
    for (int i = 0; i < arr.size(); i++) {
        cout << arr[i] << endl;
    }
}
int main() {
	int n;
	
	cin >> n;
	vector<int> int_vector(n);
	for (int i = 0; i < n; i++) {
		int value;
		cin >> value;
		int_vector[i] = value;
	}
	
	cin >> n;
	vector<string> string_vector(n);
	for (int i = 0; i < n; i++) {
		string value;
		cin >> value;
		string_vector[i] = value;
	}

	printArray<int>(int_vector);
	printArray<string>(string_vector);

	return 0;
}