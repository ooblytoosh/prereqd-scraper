from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
import requests

def scrape_majors(major_link):
    major_html = requests.get(major_link).text
    soup = BeautifulSoup(major_html, 'html.parser')

    courses_list = []
    course_table = soup.find('tbody')

    if course_table is not None:
        courses = course_table.find_all('a', class_='code')
        if courses is not None:
            for course in courses:
                course_text = course.get_text()
                cleaned_course = course_text.replace('\xa0', ' ')
                courses_list.append(cleaned_course)
    return courses_list