from scraper import scrape_prereqs, tokenize, parser
import json, requests, time
from datetime import datetime

courses_dict = {}

count = 0

with open('course_list.json', 'r') as f:
    courses = json.load(f)

with requests.Session() as session:
    for course in courses:
        course_components = course.split()
        dept = course_components[0]
        code = course_components[1]
        count += 1

        current_time = datetime.now().strftime("%H:%M:%S")

        if not code.isdigit():
            print(f"[{current_time}] ({count}/2892) Skipped non-numeric code {course}")
            continue

        start_time = time.perf_counter()

        course_name, prereq_string = scrape_prereqs(dept, code, session)
        tokens = tokenize(prereq_string)
        parsed_prereqs = parser(tokens, [0])

        courses_dict[course] = {
            'name': course_name,
            'prereqs': parsed_prereqs,
            'coreqs': []
        }

        duration = time.perf_counter() - start_time
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"[{current_time}] ({count}/2892) Processed {course} in {duration:.2f}s")

with open('courses.json', 'w') as f:
    json.dump(courses_dict, f, indent=2)