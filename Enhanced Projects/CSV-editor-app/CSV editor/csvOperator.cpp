#include "csvOperator.h"
#include "csvUtility.h"
#include "csvIO.h"
#include <iostream>
#include <limits>

static void clearCinLine() {
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

void displayCsv(const csvDocument& doc) {
    //Parses and displays entire CSV file into printed and readable format
    if (doc.rows.empty()) {
        std::cout << "[Document is empty]\n\n";
        return;
    }

    std::cout << "----- CSV CONTENTS -----\n";
    for (size_t i = 0; i < doc.rows.size(); ++i) {
        std::cout << i << ": " << joinRow(doc.rows[i], " | ") << "\n";
    }
    std::cout << "------------------------\n\n";
}

std::vector<size_t> searchCsv(const csvDocument& doc, const std::string& keyword) {
    // Searches the currently load CSV file for a input keyword. If keyword exsists in multiple entries,
    // numbered list of matches will be displayed.
    
    std::vector<size_t> matches;
    if (keyword.empty()) {
        std::cout << "Keyword empty.\n\n";
        return matches;
    }

    std::string k = toLower(keyword);

    for (size_t r = 0; r < doc.rows.size(); ++r) {
        for (const auto& cell : doc.rows[r]) {
            if (toLower(cell).find(k) != std::string::npos) {
                matches.push_back(r);
                break;
            }
        }
    }

    if (matches.empty()) {
        std::cout << "No matches found.\n\n";
    }
    else {
        std::cout << "Matches:\n";
        for (size_t i = 0; i < matches.size(); ++i) {
            size_t r = matches[i];
            std::cout << "  " << (i + 1) << ". [row " << r << "] "
                << joinRow(doc.rows[r], " | ") << "\n";
        }
        std::cout << "\n";
    }

    return matches;
}

void addEntriesInteractive(csvDocument& doc) {
    // This method allows the user to create there own CSV file within this program.
    // pressing enter with an entry will move to a new column, entering with no input will switch
    // to new row. entering the word ESCAPE will exit and save CSV to disk

    std::cout << "Entering CSV data:\n"
        << " - Type a value and press Enter for a column\n"
        << " - Blank line = new row\n"
        << " - Type ESCAPE to stop entering rows\n\n";

    std::vector<std::string> row;
    std::string input;

    while (true) {
        std::cout << "Column " << (row.size() + 1) << ": ";
        std::getline(std::cin, input);
        input = trim(input);

        if (toLower(input) == "escape") {
            if (!row.empty()) {
                doc.rows.push_back(row);
            }
            break;
        }

        if (input.empty()) {
            if (!row.empty()) {
                doc.rows.push_back(row);
                row.clear();
                std::cout << "-- New row started --\n";
            }
            continue;
        }

        row.push_back(input);
    }

    doc.modified = true;
    std::cout << "Row entry complete.\n\n";
}

void deleteEntryBySearch(csvDocument& doc) {
    // Method will search for entry by keyword, then give user option to delete entry

    std::cout << "Keyword to delete: ";
    std::string keyword;
    std::getline(std::cin, keyword);

    auto matches = searchCsv(doc, keyword);
    if (matches.empty()) return;

    std::cout << "Choose entry to delete (0 to cancel): ";
    int choice;
    std::cin >> choice;
    clearCinLine();

    if (choice <= 0 || (size_t)choice > matches.size()) {
        std::cout << "Cancel.\n\n";
        return;
    }

    size_t rowIndex = matches[choice - 1];
    doc.rows.erase(doc.rows.begin() + rowIndex);
    doc.modified = true;

    std::cout << "Deleted row " << rowIndex << ".\n\n";
}