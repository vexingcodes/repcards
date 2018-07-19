"""Generates a business card PDF containing information about the current state
representatives for all congressional districts."""

import json
import os

import jinja2
import weasyprint

ABBREV_TO_NAME = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming'
}
assert len(ABBREV_TO_NAME) == 50, "ABBREV_TO_NAME dictionary has wrong number of entries."

OUTPUT_PATH = './output'
assert os.path.exists(OUTPUT_PATH), "Output directory not found."

LEGISLATORS_FILE_PATH = './legislators-current.json'
assert os.path.exists(LEGISLATORS_FILE_PATH), "Output directory not found."

CSS_FILE_PATH = './card.css'
assert os.path.exists(CSS_FILE_PATH), "CSS file not found."

TEMPLATE_FILE_PATH = './card.html.jinja2'
assert os.path.exists(TEMPLATE_FILE_PATH), "HTML Template file not found."

def ordinal(num):
    """ Takes a number, returns a string with that number followed by its correct suffix, e.g. 1st,
    32nd, 99th, etc.  Ripped straight from
    https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement"""
    return "%d%s" % (num, "tsnrhtdd"[(num//10%10 != 1)*(num%10 < 4)*num%10::4])

def get_legislator_info(path):
    """ Transform the flat legislators-current.json into something more hierarchical"""

    with open(path) as legislator_file:
        legislators = json.load(legislator_file)

    info = {}
    for legislator in legislators:
        state = legislator['terms'][-1]['state']
        if state not in ABBREV_TO_NAME:
            continue
        if state not in info:
            info[state] = {'representatives': {}, 'senators': []}

        legislator_info = {}
        if 'official_full' in legislator['name']:
            legislator_info['name'] = legislator['name']['official_full']
        else:
            legislator_info['name'] = '{} {}'.format(
                legislator['name']['first'], legislator['name']['last'])
        legislator_info['phone'] = legislator['terms'][-1]['phone']
        legislator_info['party'] = legislator['terms'][-1]['party']

        legislator_type = legislator['terms'][-1]['type']
        if legislator_type == 'rep':
            district = str(legislator['terms'][-1]['district'])
            assert district not in info[state]['representatives'], "District has two reps."
            info[state]['representatives'][district] = legislator_info
        elif legislator_type == 'sen':
            info[state]['senators'].append(legislator_info)

    assert len(info) == 50, 'Info does not cover all states.'
    return info

def main():
    """ Generate all cards. """

    with open(CSS_FILE_PATH) as css_file:
        card_css = weasyprint.CSS(string=css_file.read())
    with open(TEMPLATE_FILE_PATH) as template_file:
        html_template = jinja2.Template(template_file.read())

    for state, reps in get_legislator_info(LEGISLATORS_FILE_PATH).items():
        for district, info in reps['representatives'].items():
            district_name = ABBREV_TO_NAME[state]
            if district != "0":
                district_name = '{} {} District '.format(district_name, ordinal(int(district)))
            html = html_template.render(district_name=district_name,
                                        sen_1_name=reps['senators'][0]['name'],
                                        sen_1_phone=reps['senators'][0]['phone'],
                                        sen_1_party=reps['senators'][0]['party'],
                                        sen_2_name=reps['senators'][1]['name'],
                                        sen_2_phone=reps['senators'][1]['phone'],
                                        sen_2_party=reps['senators'][1]['party'],
                                        rep_name=info['name'],
                                        rep_phone=info['phone'],
                                        rep_party=info['party'])
            card_html = weasyprint.HTML(string=html)
            pdf_path = '{}/{}-{:0>2}.pdf'.format(OUTPUT_PATH, state, district)
            card_html.write_pdf(pdf_path, stylesheets=[card_css])

if __name__ == '__main__':
    main()
