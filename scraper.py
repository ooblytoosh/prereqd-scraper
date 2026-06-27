from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
import requests

def scrape_prereqs(dept, course_code):
    course_url = f'https://oscar.gatech.edu/bprod/bwckctlg.p_disp_course_detail?cat_term_in=202602&subj_code_in={dept}&crse_numb_in={course_code}'
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

    prereq_string = prereq_string.replace('(', '( ')
    prereq_string = prereq_string.replace(')', ' )')
    prereq_string = ' '.join(prereq_string.split())

    return prereq_string.strip()

def tokenize(prereq_string):
    tokens = []
    keys = ['and', 'or', '(', ')']
    course_codes = {
        'ACCT',
        'AE',
        'AS',
        'APPH',
        'ASE',
        'ARBC',
        'ARCH',
        'AECT',
        'BIOS',
        'BIOL',
        'BMEJ',
        'BMED',
        'BMEM',
        'BC',
        'CETL',
        'CHBE',
        'CHEM',
        'CHIN',
        'CP',
        'CEE',
        'COE',
        'CLL',
        'COS',
        'CX',
        'CSE',
        'CS',
        'COOP',
        'UCGA',
        'EAS',
        'ECON',
        'ECEP',
        'ECE',
        'ENGL',
        'FS',
        'FREE',
        'FREN',
        'GT',
        'GTL',
        'GRMN',
        'GMC',
        'HS',
        'HEBW',
        'HIN',
        'HIST',
        'HTS',
        'HUM',
        'ID',
        'ISYE',
        'INTA',
        'IL',
        'INTN',
        'IMBA',
        'IAC',
        'JAPN',
        'KOR',
        'LATN',
        'LS',
        'LING',
        'LMC',
        'MGT',
        'MOT',
        'MLDR',
        'MSE',
        'MATH',
        'ME',
        'MP',
        'MSL',
        'ML',
        'MUSI',
        'NS',
        'NEUR',
        'NRE',
        'PERS',
        'PHIL',
        'PHYS',
        'POL',
        'PTFE',
        'PORT',
        'PSYC',
        'PUBJ',
        'PUBP',
        'RUSS',
        'SCI',
        'SLS',
        'SS',
        'SOC',
        'SPAN',
        'SWAH',
        'VIP',
        'WOLOF'

    }
    i = 0

    token_list = prereq_string.split()
    

    while i < len(token_list):
        token = token_list[i]
        if token in keys:
            tokens.append(token)
        elif token in course_codes and token_list[i+1][0].isnumeric():
            tokens.append(f'{token} {token_list[i+1]}')
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

    return {operator: items}

print(parser(tokenize(scrape_prereqs('MATH', '2552')), [0]))