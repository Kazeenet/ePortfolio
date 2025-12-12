#include "csvUtility.h"
#include <algorithm>
#include <cctype>
#include <string>

// This class defines parsing methods for simplier manipulation within the CSV file.

std::string toLower(const std::string& s) {
    std::string out = s;
    std::transform(out.begin(), out.end(), out.begin(),
        [](unsigned char c) { return std::tolower(c); });
    return out;
}

std::string trim(const std::string& s) {
    size_t start = s.find_first_not_of(" \t\r\n");
    if (start == std::string::npos) return "";

    size_t end = s.find_last_not_of(" \t\r\n");
    return s.substr(start, end - start + 1);
}

std::string joinRow(const std::vector<std::string>& row, const std::string& sep) {
    std::string out;
    for (size_t i = 0; i < row.size(); ++i) {
        out += row[i];
        if (i + 1 < row.size()) out += sep;
    }
    return out;
}