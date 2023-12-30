import sys
import difflib
import re

from datetime import datetime

def parse_date(date_string):
    date_formats = [
        "%d-%b-%Y",
        "%d-%m-%Y",
        "%Y-%b-%d",
        "%Y-%m-%d",
        "%m/%d/%y %I:%M %p"
        # Add more date formats as needed
    ]

    for date_format in date_formats:
        try:
            parsed_date = datetime.strptime(date_string, date_format)
            return parsed_date  # Return the parsed date if successful
        except ValueError:
            continue  # Continue to the next format if ValueError is raised

    # If none of the formats match
    raise ValueError("Unrecognized date format: {}".format(date_string))

def fixdate(dt):
    monmap = {
        'january': 'jan',
        'february': 'feb',
        'march': 'mar',
        'april': 'apr',
        'may': 'may',
        'june': 'jun',
        'july': 'jul',
        'august': 'aug',
        'september': 'sep',
        'october': 'oct',
        'november': 'nov',
        'december': 'dec',
        'januari': 'jan',
        'februari': 'feb',
        'mac': 'mar',
        'ogos': 'aug',
        'september': 'sep',
        'oktober': 'oct',
        'november': 'nov',
        'disember': 'dec',
        'jan': 'jan',
        'feb': 'feb',
        'mar': 'mar',
        'apr': 'apr',
        'may': 'may',
        'jun': 'jun',
        'jul': 'jul',
        'aug': 'aug',
        'sep': 'sep',
        'oct': 'oct',
        'nov': 'nov',
        'dec': 'dec'
    }

    try:
        # split 20-APR-2020 to d = 20, m = APR, y = 2020, applicable to all separators
        d, m, y = re.split(r"[ :\-/\s]+", dt.strip())
    except(ValueError):
        # split 20APR2020 to d = 20, m = APR, y = 2020
        cleaned_text = re.sub(r'[^a-zA-Z0-9]', '', dt)
        regex_pattern = re.compile(r'[a-zA-Z]+')
        matches = regex_pattern.findall(cleaned_text)
        idx = dt.index(matches[0])
        d = dt[:idx]
        m = matches[0]
        y = dt[idx+len(m):]

    months = set(monmap.keys())
    close_match = difflib.get_close_matches(m.lower(), months, 1)

    try:
        m = monmap.get(close_match[0])
    except(IndexError):
        pass

    dt = f'{d}-{m}-{y}'.upper()
    try:
        dt = parse_date(dt).strftime('%Y-%b-%d').upper()
    except(ValueError):
        return None
    return dt

def main():
    if __name__ == 'fixdates.main':
        if len(sys.argv) > 1:
            print(fixdate(sys.argv[1]))
        else:
            print('Usage: fixdates <date>')