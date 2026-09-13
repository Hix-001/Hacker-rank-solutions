// 13/09/2026
// Medium
// Attribute Parser
// HackerRank: Parse custom HTML-like tags, track nesting scope, and answer queries.

#include <iostream>
#include <vector>
#include <map>
#include <string>
#include <sstream>
#include <cstdio>

using namespace std;
int main() {
    int n, q;
    scanf("%d %d", &n, &q);
    // Consume the trailing newline after reading integers
    string temp;
    getline(cin, temp); 
    map<string, string> db;
    vector<string> tag_stack;
    for (int i = 0; i < n; ++i) {
        string line;
        getline(cin, line);
        // Clean the string: remove '"' and '>' for easier parsing
        string clean_line = "";
        for (char c : line) {
            if (c != '"' && c != '>') {
                clean_line += c;
            }
        }
        if (clean_line.substr(0, 2) == "</") {
            // Closing tag: step back out of current scope
            tag_stack.pop_back();
        } else {
            // Opening tag: enter new scope
            clean_line.erase(0, 1); // Remove the leading '<'
            stringstream ss(clean_line);        
            string tag_name;
            ss>> tag_name;
            tag_stack.push_back(tag_name);
            // Construct the current hierarchical scope path
            string scope = "";
            for (size_t j = 0; j < tag_stack.size(); ++j) {
                scope += tag_stack[j];
                if (j != tag_stack.size() - 1) scope += ".";
            }
            // Extract remaining attributes (Format: name = value)
            string attr_name, eq, attr_val;
            while (ss >> attr_name >> eq >> attr_val) {
                db[scope + "~" + attr_name] = attr_val;
            }
        }
    }
    // Process Queries
    for (int i = 0; i < q; ++i) {
        string query;
        getline(cin, query);    
        if (db.count(query)) {
            // .c_str() is required to format std::string with printf %s
            printf("%s\n", db[query].c_str()); 
        } else {
            printf("Not Found!\n");
        }
    }
    return 0;
}