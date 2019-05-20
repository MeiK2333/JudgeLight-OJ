#include <fstream>
#include <iostream>
#include <string>
#include <cctype>

int main() {
    std::ifstream fout("output.txt");
    std::ifstream fans("data.out");

    std::string s1, s2;
    std::getline(fout, s1);
    std::getline(fans, s2);

    bool ok = true;

    if (s1.length() != s2.length()) {
        ok = false;
    } else {
        for (size_t i = 0; i < s1.length(); i++) {
            if (tolower(s1[i]) != tolower(s2[i])) {
                ok = false;
            }
        }
    }
    if (ok) {
        return 0;
    }
    return 1;
}
