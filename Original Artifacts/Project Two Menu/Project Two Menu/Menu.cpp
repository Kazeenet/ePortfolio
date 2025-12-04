/*
*Developer: Morgan Kazee
*Class:  CS-300
*Date: 12-10-2024
* 
* The following is the creation of an interface that sorts and manipulates
* provided course data in a csv file.
*/


#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
//including class packages to use vectors, sorting algorthim, string, and file input

using namespace std;

//Declaring structure of course be placed into a vector of multiple course objects
struct Course {
	string courseNum;
	string courseTitle;
	vector <string> coursePrereq;
	//Prerequsites variable will exist as a vector inside a vector, since
	//they are the only attribute in course that may inlcude multiple values per course
};
vector <Course> loadData(string filename) {
	//loadData method will return a vector course object when called
	//it will load the input csv file into the course vector structure.

	string line;//Initializing line variable to use as a line placeholder
	vector<Course> courseList;//creating course list object as a vector of course objects
	ifstream file(filename);//initializing filestream for csv file

	if (!file.is_open()) {//if the file cannot be opened
		cout << "Cannot open file, please try again." << endl;//print message
		return courseList;//return
	}
	
	while (getline(file, line)) {//while there exists a next line in the file,

		Course course;//create new course object
		int index = line.find(",");//index will mark the area in the line that divides with comma
		course.courseNum = line.substr(0, index);//create course number value in course equal to the substring from begining to index
		line.erase(0, index + 1);//erases everything on the line just recorded into courseNum
		index = line.find(",");//finds the next comma
		course.courseTitle = line.substr(0, index);//repeats the same action as with courseNum, but this time with CourseTitle as it
		//will assumingly be the next in the line
		line.erase(0, index + 1);//erases everything on the line just recorded into courseTitle.

		while (!line.empty()) {//While the line is no empty after everything recorded has been deleted, meaning, while
			//prerequisites exist in the entry on the csv file,
			index = line.find(",");//the index will be set at next comma
			string tempPrereq = line.substr(0, index);//a temp variable will be made to hold the next substring from begining to the comma
			course.coursePrereq.push_back(tempPrereq);//prequisites in temp will be pushed back to the end of the CoursePrereq vector that exists
			//within the course object
			if (index == string::npos) break;//if the index has no position in the string,
			line.erase(0, index + 1);//erase what was just recorded
		}
		courseList.push_back(course);//add the course top the end of the courselist vector
	}
	file.close();//close file when finshed

	return courseList;

}

void printCourse(Course course){
	//This simple method will print the course number and course title of a course object when called.
	//After this, it also calls the prerequistes if they exist, but by using a for loop since they may or may not exist as
	//multiples in a vector

	cout << "Course Number : " << course.courseNum << endl;
	cout << "Course Title : " << course.courseTitle << endl;
	cout << "Course Prerequisites : ";
	for (string i : course.coursePrereq) {
		cout << i << ", ";
	}
	cout << endl;
}


void printCourseList(vector<Course>& courselist) {
	//this method will first use sort function from the C++ algorithm library to alphanumerically organize the courselist.
	//Then, it will iterate through the sorted list printing each course's course number and course title.

	sort(courselist.begin(), courselist.end(), [](const Course& a, const Course& b) {//returns a sorted list from the begining and end
		return a.courseNum < b.courseNum;});

	for (const Course& course : courselist) {//for each course object in course list,

		cout << course.courseNum << ", " << course.courseTitle << endl;// print courseNum and Coursetitle

	}

}
//Initiating main method
int main() {

	vector <Course> courseList;//creating empty courseList vector
	string fileName = "CS 300 ABCU_Advising_Program_Input.csv";//entering CSV filename and extension after including it in folder

	//Initalizng switch case statement for main menu 
	int choice = 0;
	while (choice != 9) {

		cout << "Welcome to course planner.\n" << endl;
		cout << "  1. Load Data Structure" << endl;
		cout << "  2. Print Course List" << endl;
		cout << "  3. Print Course." << endl;
		cout << "  9. Exit\n" << endl;
		cout << "Enter choice: ";
		cin >> choice;

		switch (choice) {

		case 1:
			courseList = loadData(fileName);//calling load data method with CSV file as parameter

			cout << "Course Data Loaded." << endl;
			break;

		case 2:

			if (courseList.empty()) {
				cout << "Course Data Empty. Please load Course Data" << endl;//message prints if user hits case 2 without
				//loading data yet
			}
			else {
				cout << "Here is a sample schedule:\n" << endl;
				cout << endl;

				printCourseList(courseList);//calls  PrintCourseList with the current courselist as parameter
			}
			break;

		case 3:

			if (courseList.empty()) {
				cout << "No course data loaded!" << endl;//message prints if user has not yet loaded the CSV file

			}
			else {

				string searchkey;//initializing searchkey variable
				
				cout << "What course do you want to know about?";
				cin >> searchkey;//searchkey variable will be equal to user input
				transform(searchkey.begin(), searchkey.end(), searchkey.begin(), toupper);
				//transform function uses toupper to captialize each letter in the searchkey course number.
				//this provides input validation. If the user enters csci400 instead of CSCI400, it will still work.
				for (Course course : courseList) {//for each course object in course list,
					if (course.courseNum == searchkey) {//if the current course objecs course number is equal to the searchkey,
						printCourse(course);//call the printcourse method with the current course as the parameter
						cout << endl;
						break;
					}
					//if course is not found, the system will print nothing.
				}

			}

			break;

		case 9:

			cout << "Thank you for using the course planner!" << endl;//exit program if choice is case 9
			break;

		default:

			cout << choice << " is not a valid option." << endl;//input validation. Message prints if user chooses other input//
			//not shown as menu option.

		}

	}
	 



	return 0;

}