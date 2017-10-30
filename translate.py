#!/usr/bin/python
# encoding: utf-8
#
# Copyright © 2017 Adam Skołuda
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2017-10-02
#

"""
Translate DeepL API
"""

from __future__ import division, print_function, unicode_literals, absolute_import

import sys

from workflow import Workflow, web, ICON_WEB

UPDATE_SETTINGS = {'github_slug': 'Skoda091/alfred-deepl'}

ICON_PL = ''
ICON_EN = ''

# Shown in error logs. Users can find help here
HELP_URL = 'https://github.com/Skoda091/alfred-deepl'

# API endpoint for DeepL translation API
API_URL = 'https://deepl.com/jsonrpc'

# How long to cache results for
CACHE_MAX_AGE = 20  # seconds

def main(wf):
    import argparse
    import re
    import requests
    import json    # Get args from Workflow, already in normalized Unicode

    parser = argparse.ArgumentParser(description='Translate sentences using the DeepL API.')
    parser.add_argument('-l', '--language', default='PL', dest='lang',
                        help="The language to translate into. Defaults to English.")
    parser.add_argument('text', nargs='+', help="The text to be translated.")
    args = parser.parse_args()
    text = " ".join(wf.args)

    sp = re.compile("([^\.!\?;]+[\.!\?;]*)")
    sentences = [s for s in sp.split(text) if len(s) > 0]
    payload = {
        "jsonrpc": "2.0", "method": "LMT_handle_jobs", "id": 1,
        "params": {
            "jobs": [{"kind": "default", "raw_en_sentence": s} for s in sentences],
            "lang": {"user_preferred_langs": ["EN", "PL"],
                    "source_lang_user_selected": "auto",
                    "target_lang": args.lang},
            "priority": 1}}
    r = requests.post(API_URL, data=json.dumps(payload))
    translations = json.loads(r.text)['result']['translations']
    result = ""
    for translation in translations:
        beams = sorted(translation['beams'], key=lambda b: -1 * b['score'])
        for beam in beams:
            item = wf.decode(beam['postprocessed_sentence'])
            wf.add_item(title=item, valid=True, icon=ICON_WEB, arg=item)

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow(libraries=['./lib'])
    sys.exit(wf.run(main))