// 18/10/2026
// Medium
// Other Concepts
// HackerRank: Resolve 'undefined reference to main' linker error by providing the full executable architecture.

#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

struct Workshop {
    int start_time;
    int duration;
    int end_time;
};

struct Available_Workshops {
    int n;
    Workshop* array;
};

Available_Workshops* initialize(int start_time[], int duration[], int n) {
    Available_Workshops* aw = new Available_Workshops;
    aw->n = n;
    aw->array = new Workshop[n];
    
    for (int i = 0; i < n; i++) {
        aw->array[i].start_time = start_time[i];
        aw->array[i].duration = duration[i];
        aw->array[i].end_time = start_time[i] + duration[i];
    }
    
    return aw;
}

int CalculateMaxWorkshops(Available_Workshops* ptr) {
    sort(ptr->array, ptr->array + ptr->n, [](const Workshop& a, const Workshop& b) {
        return a.end_time < b.end_time;
    });
    
    int count = 0;
    int current_end = 0;
    
    for (int i = 0; i < ptr->n; i++) {
        if (ptr->array[i].start_time >= current_end) {
            count++;
            current_end = ptr->array[i].end_time;
        }
    }
    
    return count;
}

int main() {
    int n;
    if (cin >> n) {
        int* start_time = new int[n];
        int* duration = new int[n];
        
        for (int i = 0; i < n; i++) {
            cin >> start_time[i];
        }
        for (int i = 0; i < n; i++) {
            cin >> duration[i];
        }
        
        Available_Workshops* ptr = initialize(start_time, duration, n);
        cout << CalculateMaxWorkshops(ptr) << "\n";
        
        // Memory Cleanup
        delete[] start_time;
        delete[] duration;
        delete[] ptr->array;
        delete ptr;
    }
    
    return 0;
}