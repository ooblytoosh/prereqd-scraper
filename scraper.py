from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
from constants import COURSE_CODES
import requests


def scrape_prereqs(dept, course_code, session):
    course_url = f'https://oscar.gatech.edu/bprod/bwckctlg.p_disp_course_detail?cat_term_in=202602&subj_code_in={dept}&crse_numb_in={course_code}'
    course = session.get(course_url).text
    soup = BeautifulSoup(course, 'lxml')

    prereq_string = ""
    prereq_block = soup.find('span', class_='fieldlabeltext', string='Prerequisites: ')

    if prereq_block is not None:
        for item in prereq_block.next_siblings:
            if isinstance(item, NavigableString):
                prereq_string += item.strip()
            elif isinstance(item, Tag):
                if item.string is not None:
                    prereq_string += item.string
            prereq_string += " "

    prereq_string = prereq_string.replace('(', '( ')
    prereq_string = prereq_string.replace(')', ' )')
    prereq_string = ' '.join(prereq_string.split())

    course_name = soup.find(class_='nttitle')
    if course_name is not None:
        course_name = course_name.string
        if course_name is not None:
            course_name = course_name.replace(f"{dept} {course_code} - ", '')

    return (course_name, prereq_string.strip())


def tokenize(prereq_string):
    tokens = []
    keys = ['and', 'or', '(', ')']
    i = 0
    token_list = prereq_string.split()

    while i < len(token_list):
        token = token_list[i]
        if token in keys:
            tokens.append(token)
        elif token in COURSE_CODES and token_list[i + 1][0].isnumeric() and 'X' not in token_list[i + 1]:
            tokens.append(f'{token} {token_list[i + 1]}')
        i += 1

    cleaned_tokens = []
    for token in tokens:
        if (token == 'or' or token == 'and') and cleaned_tokens and cleaned_tokens[-1] == token:
            continue
        else:
            cleaned_tokens.append(token)

    return cleaned_tokens


def parser(tokens, position):
    items = []
    operator = None

    if len(tokens) == 0:
        return {}

    while position[0] < len(tokens):
        token = tokens[position[0]]
        position[0] += 1

        if token == '(':
            items.append(parser(tokens, position))
        elif token == 'and':
            operator = 'and'
        elif token == 'or':
            operator = 'or'
        elif token == ')':
            break
        else:
            items.append(token)

    if len(items) == 1 and operator is None:
        return {'and': items}

    return {operator: items}