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
import argparse
import re
import json
from plistlib import readPlist
from workflow import Workflow, web, ICON_WEB

UPDATE_SETTINGS = {'github_slug': 'Skoda091/alfred-deepl'}
ICON_UPDATE = 'update-available.png'

# Shown in error logs. Users can find help here
HELP_URL = 'https://github.com/Skoda091/alfred-deepl'

# API endpoint for DeepL translation API
API_URL = 'https://deepl.com/jsonrpc'

# How long to cache results for
CACHE_MAX_AGE = 20  # seconds

def parse_args(args):
    parser = argparse.ArgumentParser(description='Translate sentences using the DeepL API.')
    parser.add_argument('--set-target-language', default='EN', dest='target_lang',
                        help="The language to translate into. Defaults to English.")
    parser.add_argument('text', nargs='+', help="The text to be translated.", default='text')
    return parser.parse_args(args)

def main(wf):
    args = parse_args(wf.args)
    target_lang = readPlist('info.plist')['variables']['target_lang']

    # Update available?
    if wf.update_available:
        wf.add_item('A newer version is available',
                    '↩ to install update',
                    autocomplete='workflow:update',
                    icon=ICON_UPDATE)
    # TODO: change from wf.args to args
    text = " ".join(wf.args)

    sp = re.compile("([^\.!\?;]+[\.!\?;]*)")
    sentences = [s for s in sp.split(text) if len(s) > 0]
    payload = {
        "jsonrpc": "2.0", "method": "LMT_handle_jobs", "id": 1,
        "params": {
            "jobs": [{"kind": "default", "raw_en_sentence": s} for s in sentences],
            "lang": {"user_preferred_langs": ["EN", "PL"],
                    "source_lang_user_selected": "auto",
                    "target_lang": target_lang},
            "priority": 1}}
    r = web.post(API_URL, data=json.dumps(payload))
    translations = json.loads(r.text)['result']['translations']
    result = ""
    for translation in translations:
        beams = sorted(translation['beams'], key=lambda b: -1 * b['score'])
        for beam in beams:
            item = wf.decode(beam['postprocessed_sentence'])
            wf.add_item(title=item, valid=True, icon=ICON_WEB, arg=item)

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow(libraries=['./lib'],
                  help_url=HELP_URL,
                  update_settings=UPDATE_SETTINGS)
    log = wf.logger
    sys.exit(wf.run(main))