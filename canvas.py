import requests
import string
import json

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}
class Canvas:
    def __init__(self):
        self.access_token = "3165~ClzFgg1KPHRtpGdPo9X5BZcM2uF204q6oNOo0ProkSvlGke7sJ5Q6cfMksQ8Onv9"
    
    def get_courses(self):
        url = "https://canvas.instructure.com/api/v1/courses"
        headers = {"Authorization": "Bearer " + self.access_token}
        r = requests.get(url, headers=headers)
        return r.json()
    
    def get_grades(self):
        url = "https://canvas.instructure.com/api/v1/users/self/favorites/courses?include[]=total_scores&include[]=favorites"
        headers = {"Authorization": "Bearer " + self.access_token}
        r = requests.get(url, headers=headers)
        return r.json()

# print events
print(json.dumps(Canvas().get_grades(), indent=4))