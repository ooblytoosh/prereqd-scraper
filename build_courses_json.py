from courses_scraper import scrape_prereqs, tokenize, parser
import json, requests, time
from datetime import datetime
from constants import COURSE_LIST

count = 0
courses = {}

with requests.Session() as session:
    for course in COURSE_LIST:
        course_components = course.split()
        dept = course_components[0]
        code = course_components[1]
        count += 1
        current_time = datetime.now().strftime("%H:%M:%S")
        start_time = time.perf_counter()

        course_name, prereq_string, credit_hours = scrape_prereqs(dept, code, session)
        tokens = tokenize(prereq_string)
        parsed_prereqs = parser(tokens, [0])

        courses[course] = {
            'name': course_name,
            'prereqs': parsed_prereqs,
            'hours': credit_hours
        }

        duration = time.perf_counter() - start_time
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"[{current_time}] ({count}/2636) Processed {course} in {duration:.2f}s")

with open('courses.json', 'w') as f:
    json.dump(courses, f, indent=2)