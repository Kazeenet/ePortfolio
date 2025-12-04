#ifndef CSVIO_H
#define CSVIO_H

#include <string>
#include "CsvDocument.h"

bool loadCsvFromFile(csvDocument& doc, const std::string& path);
bool saveCsvToFile(const csvDocument& doc, const std::string& path);

#endif
