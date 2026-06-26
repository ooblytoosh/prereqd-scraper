from bs4 import BeautifulSoup
import requests

course = requests.get('https://oscar.gatech.edu/bprod/bwckctlg.p_disp_course_detail?cat_term_in=202602&subj_code_in=AE&crse_numb_in=1601').text
soup = BeautifulSoup(course, 'html.parser')

prereq_string = ""

prereq_block = soup.find('span', string='Prerequisites: ')

print(prereq_block)