#ifndef CSVOPERATOR_H
#define CSVOPERATOR_H

#include "csvDocument.h"
#include <vector>
#include <string>

void displayCsv(const csvDocument& doc);
std::vector<size_t> searchCsv(const csvDocument& doc, const std::string& keyword);
void addEntriesInteractive(csvDocument& doc);
void deleteEntryBySearch(csvDocument& doc);

#endif
