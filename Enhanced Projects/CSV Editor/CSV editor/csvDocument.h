#ifndef CSVDOCUMENT_H
#define CSVDOCUMENT_H

#include <string>
#include <vector>

// Note: This header, and NOT a .cpp file, defines the CSV object within the program.

struct csvDocument {
    std::vector<std::vector<std::string>> rows;
    std::string filename;
    bool modified = false;
};

#endif