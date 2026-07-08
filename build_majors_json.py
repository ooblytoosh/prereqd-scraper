from majors_scraper import scrape_majors
import json
from constants import MAJORS_LINKS

majors = {}
for major, link in MAJORS_LINKS.items():
    majors[major] = {
        "courses": scrape_majors(link)
    }

with open('majors.json', 'w') as f:
    json.dump(majors, f, indent=2)