/************************************************************
 *  CSV Editor Program 1.0
 *  Developer: Tyler Kazee
 *  Email: tkazee1226@gmail.com
 *  Date: 11/18/2025
 *
 *  Description:
 *  This program loads, edits, searches, and saves CSV files.
 *  It includes parsing support for quoted fields, escaped
 *  double-quotes, and commas inside quotes.
 ************************************************************/

#include <iostream>
#include <limits>
#include <string>
#include "csvDocument.h"
#include "csvIO.h"
#include "csvOperator.h"

void clearCin() {
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

void runCsvOperations(csvDocument& doc) {
    while (true) {
        std::cout << "----- CSV Menu -----\n"
            << "1. Display CSV\n"
            << "2. Search CSV\n"
            << "3. Add Row\n"
            << "4. Delete Row\n"
            << "5. Save CSV\n"
            << "6. Return\n"
            << "Choice: ";

        int choice;
        std::cin >> choice;
        clearCin();
        std::cout << "\n";

        switch (choice) {
        case 1:
            displayCsv(doc);
            break;

        case 2: {
            std::string key;
            std::cout << "Keyword: ";
            std::getline(std::cin, key);
            std::cout << "\n";
            searchCsv(doc, key);
            break;
        }

        case 3:
            addEntriesInteractive(doc);
            break;

        case 4:
            deleteEntryBySearch(doc);
            break;

        case 5: {
            std::string path = doc.filename;

            if (path.empty()) {
                std::cout << "Enter file name: ";
                std::getline(std::cin, path);
            }

            if (!path.empty()) {
                saveCsvToFile(doc, path);
                doc.filename = path;
                doc.modified = false;
            }
            else {
                std::cout << "Save cancelled.\n\n";
            }
            break;
        }

        case 6:
            return;

        default:
            std::cout << "Invalid choice.\n\n";
        }
    }
}

int main() {
   csvDocument doc;

    while (true) {
        std::cout << "===== CSV Manager =====\n"
            << "1. Load File\n"
            << "2. Create New CSV\n"
            << "3. Help / README\n"
            << "4. Exit\n"
            << "Choice: ";

        int choice;
        std::cin >> choice;
        clearCin();
        std::cout << "\n";

        switch (choice) {
        case 1: {
            std::cout << "Enter file path: ";
            std::string path;
            std::getline(std::cin, path);

            if (loadCsvFromFile(doc, path)) {
                runCsvOperations(doc);
            }
            break;
        }

        case 2: {
            doc = csvDocument(); // reset
            std::cout << "New CSV created.\n\n";

            addEntriesInteractive(doc);

            if (!doc.rows.empty()) {
                std::cout << "Save CSV as: ";
                std::string path;
                std::getline(std::cin, path);

                if (!path.empty()) {
                    saveCsvToFile(doc, path);
                    doc.filename = path;
                    doc.modified = false;
                }
            }

            runCsvOperations(doc);
            break;
        }

        case 3: {
            std::cout << "\n========== HELP / README ==========\n\n";

            std::cout <<
                "This program allows the user to load, view, edit, search, and save CSV files.\n"
                "Supported CSV features include:\n"
                "  Quoted fields\n"
                "  Commas inside quoted fields\n"
                "  Escaped double-quotes (\"\")\n"
                "  Adding and deleting rows\n"
                "  Searching by keyword\n\n"

                "Menu Options:\n"
                "  1. Load File        - Load an existing CSV into memory\n"
                "  2. Create New CSV   - Start a new blank CSV file\n"
                "  3. Display CSV      - Prints the CSV to the console\n"
                "  4. Search CSV       - Finds rows containing a keyword\n"
                "  5. Add Row          - Append a row to the CSV\n"
                "  6. Delete Row       - Remove a row based on a search term\n"
                "  7. Save CSV         - Write your changes to disk\n"
                "  8. Help / README    - Show this information\n"
                "  9. Exit Program\n\n"

                "Notes:\n\n"
                "  When creating and saving a CSV with this program,\n"
                "  the file will be created within the same file/directory\n"
                "  as this CSV Manager program.\n"
                "  \n"
                "  This program does NOT support Excel formulas.\n"
                "  CSV structure must remain rectangular.\n"
                "  Be sure to save your work before exiting.\n\n"
                "  About the developer -\n\n"
                "  This program was created by Tyler Kazee, a Computer Science major\n"
                "  attending Southern New Hampshire University. It is an enhanced and\n"
                "  redesigned version of a project originally titled \"CSV MENU,\" developed\n"
                "  for the course CS-300: Data Structures and Algorithms, and later used\n"
                "  as part of the CS-499 Computer Science Capstone.\n\n"
                "===================================\n\n\n";
            break;
        }

        case 4:
            std::cout << "Goodbye! Thank you for using this program!\n";
            return 0;

        default:
            std::cout << "Invalid choice.\n\n";
        }
    }
}