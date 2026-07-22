# prereqd-scraper

A scraper for Georgia Tech's course catalog and prerequisite data, built
to feed [prereqd](https://github.com/your-username/prereqd) — Georgia
Tech doesn't publish a course/prerequisite API, so this pulls structured
data out of the public OSCAR catalog pages instead.

**⚠️ Unofficial.** Scrapes public catalog pages (OSCAR), not any
sanctioned API. Not affiliated with Georgia Tech. Catalog page structure
can change at any time and break this without warning — see [Known
issues](#known-issues) below.

## What it produces

Two scripts, two outputs. **`courses.json` and `majors.json` are
gitignored** — they're generated locally by running the scripts below,
not committed to this repo.

### `courses.json`

Built by `build_courses_json.py`, using `courses_scraper.py`. Scrapes
every course in `COURSE_LIST` (defined in `constants.py`) from its OSCAR
catalog detail page, pulling out:

- **Course name**
- **Credit hours**
- **Prerequisites**, parsed from raw catalog text (e.g. `"MATH 1552 and
  (PHYS 2211 or PHYS 2231)"`) into a nested AND/OR tree:

```json
{
  "MATH 2552": {
    "name": "Differential Equations",
    "prereqs": {
      "and": [
        "MATH 1552",
        { "or": ["PHYS 2211", "PHYS 2231"] }
      ]
    },
   "hours": 4,
  }
}
```

This is the exact schema [prereqd](https://github.com/ooblytoosh/prereqd)
expects for `courses.json`.

### `majors.json`

Built by `build_majors_json.py`, using `majors_scraper.py`. Scrapes each
major's public requirements page (`MAJORS_LINKS` in `constants.py`) and
pulls the raw list of course codes referenced on that page.

**Note:** this output is just a flat list of course codes per major —
it does **not** produce the `single` / `choose` / `pool` requirement
structure prereqd's `majors.json` actually uses. That structure (which
requirement is a straight single course vs. a "choose N" group vs. a
credit-hour pool, footnote-driven exceptions, thread/concentration
data, etc.) currently has to be built by hand from the flat scraped
list — the scraper gets you the raw ingredients, not the finished
data file. See prereqd's README for more on that schema.

## How prerequisite parsing works

1. **`scrape_prereqs`** (in `courses_scraper.py`) fetches a course's
   OSCAR detail page and pulls the raw prerequisite text out of the
   page's `Prerequisites:` field, along with the course name and
   credit hours.
2. **`tokenize`** splits that raw text into a flat list of tokens —
   course codes, `and`/`or`, and parentheses — filtering out anything
   that isn't a real recognized course code (checked against
   `COURSE_CODES`).
3. **`parser`** recursively walks the token list and builds a nested
   `{and: [...]}` / `{or: [...]}` tree, handling parenthesized
   sub-groups by recursing into them.

## Setup

```bash
pip install beautifulsoup4 lxml requests
```

`constants.py` is included in this repo — it defines:
- `COURSE_LIST` — every course code to scrape for `courses.json`
- `COURSE_CODES` — the set of valid department prefixes, used by the
  tokenizer to distinguish real course codes from other text
- `MAJORS_LINKS` — a dict of `{major name: catalog URL}` for
  `majors.json`

No additional configuration needed — clone and run.

## Running

```bash
python build_courses_json.py   # → courses.json
python build_majors_json.py    # → majors.json
```

Scraping the full course list takes a while — it's a synchronous loop
over ~2,600 individual page requests, printing progress
(`(count/total)`) and per-request timing as it goes.

## Known issues

- **No rate limiting.** Requests fire back-to-back with no delay
  between them. This is easy on a small `COURSE_LIST` but worth adding
  a `time.sleep()` between requests if you're scraping the full
  catalog, both to be a reasonable citizen toward OSCAR and to reduce
  the chance of getting throttled or blocked mid-run.
- **Fragile to page structure changes.** Course names, prereqs, and
  credit hours are all pulled via specific CSS classes
  (`fieldlabeltext`, `nttitle`, `ntdefault`) that OSCAR could change at
  any time without notice — if scraping suddenly returns `None` for
  everything, this is the first place to check.
- **Prereq tokenizer assumes clean spacing/structure.** Catalog prose
  is hand-written per course and not perfectly consistent; some
  courses' prerequisite text may not tokenize/parse cleanly and are
  worth spot-checking against the live catalog page rather than
  trusted blindly.
- **`majors.json` output needs manual follow-up work** (see above) —
  it's a starting point for building prereqd's actual major/thread
  data, not a drop-in replacement for it.
- **Hardcoded term code** (`cat_term_in=202602`) — scrapes whichever
  catalog term is hardcoded into the URL; update this if you need a
  different term's course data.
- **Outdated course info** - OSCAR is out of date for some courses,
  so there are some edge cases where newer courses aren't in OSCAR
  yet or there are still legacy/decomissioned classes still in the
  database.

## Related

- [prereqd](https://github.com/ooblytoosh/prereqd) — the app this
  data feeds into
