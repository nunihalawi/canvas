import requests
import string
import json


with open('settings.json') as json_file:
    settings = json.load(json_file)

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