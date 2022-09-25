import requests
import string
import json


with open('settings.json') as json_file:
    settings = json.load(json_file)

with open('grades.json') as json_file:
    grades = json.load(json_file)

class Canvas:
    def __init__(self):
        self.access_tokens = settings["access_tokens"] # define access token, can create through canvas settings
    
    def get_courses(self):
        courses = {}

        for token in self.access_tokens:
            self.headers = {"Authorization": "Bearer " + token}
            url = "https://canvas.instructure.com/api/v1/courses?include[]=favorites"
            r = requests.get(url, headers=self.headers).json() # get all courses for specific acccess token
            for item in r: courses[(str(item["id"])[-5:])] = item["name"] # add to dictionary

        # returns courses in dictionary formatted courseID : courseName

        return courses
    
    def get_grades(self):

        gradeList = {}

        for token in self.access_tokens:
            self.headers = {"Authorization": "Bearer " + token}
            url = "https://canvas.instructure.com/api/v1/users/self/favorites/courses?include[]=total_scores&include[]=favorites"
            grades = requests.get(url, headers=self.headers).json()

            for item in grades:
                if item['enrollments'][0]['computed_current_score'] != None: # checks to make sure that you have a current grade in that course: 
                    gradeList[item["name"]] = item['enrollments'][0]['computed_current_score']
        
        # returns Grades with formatt courseName: currentGrade

        return gradeList
    
    def dump_to_grades_json(self, grades):
        with open('grades.json', 'w') as outfile:
            json.dump(grades, outfile, indent=4)

    def poll_for_updates(self): # essentially checking if a grade has changed by poling and cross-referencing with our last result
        while True:
            gradeList = self.get_grades() # get the current grades
            for course in gradeList: # access the "old" grades that we got before that are stored in grades.json
                if course in grades: # if the course is in the json file
                    if gradeList[course] != grades[course]: # if their is a discrepancy between the old and new grades; change the grade in the json file and print the change
                        print(f"Grade for {course} has changed from {grades[course]} % to {gradeList[course]} %")
                        grades[course] = gradeList[course]
                        self.dump_to_grades_json(grades)
                elif course not in grades: # if the course is not in the json file altogether, add it to the json file and print the change
                    print(f"New course added: {course} | Grade: {gradeList[course]}")
                    grades[course] = gradeList[course]
                    self.dump_to_grades_json(grades)
    
    # WORK IN PROGRESS (braindead API)
    # def toDoList(self, courses):
    #     toDoList = {}
    #     token = self.access_tokens[1]
    #     self.headers = {"Authorization": "Bearer " + token}
    #     for courseID in courses.keys():
    #         url = f"https://canvas.instructure.com//api/v1/courses/{courseID}/todo"
    #         toDo = requests.get(url, headers=self.headers).json()
    #         print(toDo)
        

    # WORK IN PROGRESS (braindead)
    # def list_assignements(self, courses):
    #     courseList = courses.keys()
    #     for courseID in courseList:
    #         url = f"https://canvas.instructure.com/api/v1/courses/{courseID}/assignments?include[]"
    #         assignments = requests.get(url, headers=self.headers).json()
    #         print(assignments)
        

Canvas = Canvas()
courses = Canvas.get_courses() # returns dictionary of courseID : courseName
grades = Canvas.get_grades() # returns a dictionary of courseName: currentGrade
poll = Canvas.poll_for_updates() # polls for changes in grades and prints them out 