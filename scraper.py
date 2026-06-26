from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
import requests

course_url = 'https://oscar.gatech.edu/bprod/bwckctlg.p_disp_course_detail?cat_term_in=202602&subj_code_in=MATH&crse_numb_in=2551'
course = requests.get(course_url).text
soup = BeautifulSoup(course, 'html.parser')

prereq_string = ""

prereq_block = soup.find('span', class_='fieldlabeltext', string='Prerequisites: ')

if prereq_block is not None:
    for item in prereq_block.next_siblings:
        if isinstance(item, NavigableString):
            prereq_string += item.strip()
        elif isinstance(item, Tag):
            if (item.string is not None):
                prereq_string += item.string
        prereq_string += " "


print(prereq_string.strip())