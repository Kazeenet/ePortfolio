#include "csvIO.h"
#include <fstream>
#include <iostream>



bool loadCsvFromFile(csvDocument& doc, const std::string& path) {
    // Method takes a CSV file address in the form of a string, and loads it into memory
    
    // Validate filepath input
    if (path.empty()) {
        std::cout << "Error: No file path entered.\n\n";
        return false;
    }

    // Enforce .csv extension
    if (path.size() < 4 || path.substr(path.size() - 4) != ".csv") {
        std::cout << "Warning: File does not end with .csv extension.\n";
    }

    // Opens file
    std::ifstream file(path);
    if (!file.is_open()) {
        std::cout << "Error: Could not open file \"" << path << "\"\n";
        std::cout << "Make sure the file exists and the path is correct.\n\n";
        return false;
    }

    doc.rows.clear();
    std::string line;
    bool fileHadContent = false;

    // Read line-by-line with validation
    while (std::getline(file, line)) {

        fileHadContent = true;

        // Ignore completely empty lines
        if (line.empty()) {
            continue;
        }

        std::vector<std::string> row;
        std::string cell;
        bool inQuotes = false;

        for (size_t i = 0; i < line.size(); ++i) {
            char ch = line[i];

            // Handle escaped double quotes ("")
            if (ch == '\"' && inQuotes && i + 1 < line.size() && line[i + 1] == '\"') {
                cell.push_back('\"');  // add literal "
                i++;                  // skip next "
                continue;
            }

            if (ch == '\"') {
                inQuotes = !inQuotes;
                continue;
            }

            if (ch == ',' && !inQuotes) {
                row.push_back(cell);
                cell.clear();
            }
            else {
                cell.push_back(ch);
            }
        }

        row.push_back(cell);

        // Validate column count consistency
        if (!doc.rows.empty() && row.size() != doc.rows[0].size()) {
            std::cout << "Warning: Row has a different number of columns than header.\n";
        }

        doc.rows.push_back(row);
    }

    // Reject empty file
    if (!fileHadContent) {
        std::cout << "Warning: File was empty or unreadable.\n\n";
        return false;
    }

    // Successfully loaded
    doc.filename = path;
    doc.modified = false;

    std::cout << "CSV file successfully loaded!\n";
    std::cout << "Rows loaded: " << doc.rows.size() << "\n\n";

    return true;
}
bool saveCsvToFile(const csvDocument& doc, const std::string& path) {
    //Method to save CSV file to disk
    std::ofstream out(path);
    if (!out.is_open()) {
        std::cout << "Error: could not open file for writing.\n\n";
        return false;
    }

    for (size_t r = 0; r < doc.rows.size(); ++r) {
        const auto& row = doc.rows[r];

        for (size_t c = 0; c < row.size(); ++c) {
            out << row[c];
            if (c + 1 < row.size()) out << ",";
        }
        if (r + 1 < doc.rows.size()) out << "\n";
    }

    std::cout << "File saved to: " << path << "\n\n";
    return true;
}