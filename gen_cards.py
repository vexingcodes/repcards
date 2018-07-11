"""Generates a business card PDF containing information about the current state
representatives for all congressional districts."""

import json
import os

import weasyprint

OUTPUT_PATH = './output'
LEGISLATORS_FILE_PATH = './legislators-current.json'

assert os.path.exists(LEGISLATORS_FILE_PATH), "Output directory not found."
assert os.path.exists(OUTPUT_PATH), "Output directory not found."

def get_legislator_info(path):
    with open(path) as legislator_file:
        legislators = json.load(legislator_file)

    info = {}
    for legislator in legislators:
        legislator_info = {}
        legislator_info['name'] = legislator['name']['official_full']
        legislator_info['phone'] = legislator['terms'][-1]['phone']

        state = legislator['terms'][-1]['state']
        if state not in info:
            info[state] = {'representatives': {}, 'senators': []}

        legislator_type = legislator['terms'][-1]['type']
        if legislator_type == 'rep':
            district = str(legislator['terms'][-1]['district'])
            info[state]['representatives'][district] = legislator_info
        elif legislator_type == 'sen':
            info[state]['senators'].append(legislator_info)
    return info

card_css = weasyprint.CSS(string='@page { size: A3; margin: 1cm }')
card_html = weasyprint.HTML(string='<h1>The title</h1><p>Content goes here')
card_html.write_pdf('./output/example.pdf', stylesheets=[card_css],)

#for state, reps in get_legislator_info(LEGISLATORS_FILE_PATH).items():
#    for district, info in reps['representatives'].items():
#        pdf_path = '{}/{}-{:0>2}.pdf'.format(OUTPUT_PATH, state, district)
#        with open(pdf_path, 'w') as district_file:
#            district_file.write(info['name'])
