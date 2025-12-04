#ifndef CSVUTILITY_H
#define CSVUTILITY_H

#include <string>
#include <vector>

std::string toLower(const std::string& s);
std::string trim(const std::string& s);
std::string joinRow(const std::vector<std::string>& row, const std::string& sep = " | ");

#endif