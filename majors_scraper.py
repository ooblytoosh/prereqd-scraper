from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
import requests

def scrape_majors(major_link):
    major_html = requests.get(major_link).text
    soup = BeautifulSoup(major_html, 'html.parser')

    courses_list = []
    course_tables = soup.find_all(class_='sc_courselist')

    if course_tables is not None:
        for table in course_tables:
            table_body = table.find('tbody')
            if table_body is not None:
                courses = table_body.find_all('a', class_='code')
                if courses is not None:
                    for course in courses:
                        course_text = course.get_text()
                        cleaned_course = course_text.replace('\xa0', ' ')
                        courses_list.append(cleaned_course)
    return courses_list