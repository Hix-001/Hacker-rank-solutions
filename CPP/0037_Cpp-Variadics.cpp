// 17/10/2026
// Hard
// C++ Variadics
// HackerRank: Utilize variadic templates and fold expressions to convert reverse binary parameter packs to integers.

#include <iostream>
#include <string>

using namespace std;

// Template function
template <bool... digits>
int reversed_binary_value()
{
    int value = 0;
    int position = 0;

    // First template argument = least significant bit
    ((value += (digits ? (1 << position) : 0), ++position), ...);

    return value;
}

int main()
{
    int t;
    cin >> t;

    while (t--)
    {
        int x, y;
        cin >> x >> y;

        string result;

        // Range: 64*y to 64*y + 63
        for (int i = 0; i < 64; ++i)
        {
            int value = 64 * y + i;

            if (value == x)
                result += '1';
            else
                result += '0';
        }

        cout << result << '\n';
    }

    return 0;
}