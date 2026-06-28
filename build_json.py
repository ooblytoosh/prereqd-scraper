from scraper import scrape_prereqs, tokenize, parser
import json

courses_dict = {}

with open('course_list.json', 'r') as f:
    courses = json.load(f)

with open('new_courses.json', 'w') as f:
    for course in courses[:160]:
        course_components = course.split()
        dept = course_components[0]
        code = course_components[1]

        if int(code[0]) > 4:
            continue

        course_name, prereq_string = scrape_prereqs(dept, code)
        tokens = tokenize(prereq_string)
        parsed_prereqs = parser(tokens, [0])

        courses_dict[course] = {
            'name': course_name,
            'prereqs': parsed_prereqs,
            'coreqs': []
        }
    json.dump(courses_dict, f, indent=2)
