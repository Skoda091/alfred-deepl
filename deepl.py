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

from __future__ import division, print_function, unicode_literals, \
    absolute_import
from plistlib import readPlist
import sys

import json

from workflow import Workflow, web

UPDATE_SETTINGS = {'github_slug': 'Skoda091/alfred-deepl'}
ICON_UPDATE = 'update-available.png'

# Shown in error logs. Users can find help here
HELP_URL = 'https://github.com/Skoda091/alfred-deepl'

# API endpoint for DeepL translation API
API_URL = 'https://deepl.com/jsonrpc'

# How long to cache results for
CACHE_MAX_AGE = 20  # seconds


def parse_args(args):
    """Parse provided arguments to script"""
    from argparse import ArgumentParser

    parser = ArgumentParser(
        description='Translate sentences using the DeepL API.')
    parser.add_argument(
        '--set-target-language',
        default='EN',
        dest='target_lang',
        help="The language to translate into. Defaults to English.")
    parser.add_argument(
        'text',
        default='text',
        nargs='+',
        help="The text to be translated.")
    return parser.parse_args(args)


def get_target_lang():
    """Retrieve target language translation from settings variables"""
    return readPlist('info.plist')['variables']['target_lang']


def create_payload(text, target_lang):
    """Create payload for DeepL API call"""
    return {
        "jsonrpc": "2.0", "method": "LMT_handle_jobs", "id": 1,
        "params": {
            "jobs": [{"kind": "default", "raw_en_sentence": s} for s in text],
            "lang": {"user_preferred_langs": ["EN", "PL"],
                     "source_lang_user_selected": "auto",
                     "target_lang": target_lang},
            "priority": 1}}


def call_deepl_api(payload):
    """Return results from API"""
    return web.post(API_URL, data=json.dumps(payload))


def main(wf):
    # Import packages
    import deepl_available_langs as langs

    # Update available?
    if wf.update_available:
        wf.add_item('A newer version is available',
                    '↩ to install update',
                    autocomplete='workflow:update',
                    icon=ICON_UPDATE)

    args = parse_args(wf.args)

    # Fallback if target language not set
    if args.target_lang:
        target_lang = args.target_lang
    else:
        target_lang = get_target_lang()

    # Translate
    payload = create_payload(args.text, target_lang)
    response = call_deepl_api(payload)

    translations = json.loads(response.text)['result']['translations']
    target_lang = json.loads(response.text)['result']['target_lang'] or \
        target_lang
    source_lang = json.loads(response.text)['result']['source_lang']

    for translation in translations:
        beams = sorted(translation['beams'], key=lambda b: -1 * b['score'])
        for beam in beams:
            item = wf.decode(beam['postprocessed_sentence'])

            subtitle = 'Translated from ' + \
                langs.AVAILABLE_LANGS[source_lang]['name']
            icon = langs.AVAILABLE_LANGS[target_lang]['icon']

            wf.add_item(title=item, subtitle=subtitle, valid=True, icon=icon,
                        arg=item)

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow(libraries=['./lib'],
                  help_url=HELP_URL,
                  update_settings=UPDATE_SETTINGS)
    log = wf.logger
    sys.exit(wf.run(main))