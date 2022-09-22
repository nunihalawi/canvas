import requests
import string
import json

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}


class Canvas:
    def __init__(self):
        self.access_token = "3165~ClzFgg1KPHRtpGdPo9X5BZcM2uF204q6oNOo0ProkSvlGke7sJ5Q6cfMksQ8Onv9" # define access token, can get through canvas settings
        self.headers = {"Authorization": "Bearer " + self.access_token} # authorization header
    
    def get_courses(self):
        url = "https://canvas.instructure.com/api/v1/courses"
        r = requests.get(url, headers=self.headers).json()
        # returns courses in dictionary formatted courseID : courseName
        return {str(item["id"])[-5:] : item["name"] for item in r}

    
    def get_grades(self):
        url = "https://canvas.instructure.com/api/v1/users/self/favorites/courses?include[]=total_scores&include[]=favorites"
        grades = requests.get(url, headers=self.headers).json()
        # returns Grades with formatt courseName: currentGrade
        return {item["name"]: item['enrollments'][0]['computed_current_score'] for item in grades if item['enrollments'][0]['computed_current_score'] != None}, 
    
    # WORK IN PROGRESS
    # def list_assignements(self, courses):
    #     courseList = courses.keys()
    #     for courseID in courseList:
    #         url = f"https://canvas.instructure.com/api/v1/courses/{courseID}/assignments?include[]"
    #         assignments = requests.get(url, headers=self.headers).json()
    #         print(assignments)
        

Canvas = Canvas()
courses = Canvas.get_courses() # returns dictionary of courseID : courseName
grades = Canvas.get_grades() # returns a dictionary of courseName: currentGrade

