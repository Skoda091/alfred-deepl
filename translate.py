#!/usr/bin/python
# encoding: utf-8
from __future__ import division, print_function, unicode_literals, absolute_import

import sys

from workflow import Workflow, web, ICON_WEB

def main(wf):
    import argparse
    import re
    import requests
    import json    # Get args from Workflow, already in normalized Unicode

    args_wf = wf.args
    # print("#DUPA_-1")
    # print(args_wf[0])

    parser = argparse.ArgumentParser(description='Translate sentences using the DeepL API.')
    parser.add_argument('-l', '--language', default='PL', dest='lang',
                        help="The language to translate into. Defaults to English.")
    parser.add_argument('text', nargs='+', help="The text to be translated.")
    # print("#DUPA_0")
    args = parser.parse_args()
    # print(args)
    # print("#DUPA_1")
    text = " ".join(args.text)
    # print("#DUPA_2")
    # print(text)

    sp = re.compile("([^\.!\?;]+[\.!\?;]*)")
    sentences = [s for s in sp.split(text) if len(s) > 0]
    payload = {
        "jsonrpc": "2.0", "method": "LMT_handle_jobs", "id": 1,
        "params": {
            "jobs": [{"kind": "default", "raw_en_sentence": s} for s in sentences],
            "lang": {"user_preferred_langs": ["EN", "DE"],
                    "source_lang_user_selected": "auto",
                    "target_lang": args.lang},
            "priority": 1}}
    # print(payload)
    r = requests.post('https://deepl.com/jsonrpc', data=json.dumps(payload))
    translations = json.loads(r.text)['result']['translations']
    # print(translations)

    result = ""
    for translation in translations:
        # print(translation)
        beams = sorted(translation['beams'], key=lambda b: -1 * b['score'])
        for beam in beams:
            wf.add_item(title=wf.decode(beam['postprocessed_sentence']), valid=True, icon=ICON_WEB)

    # wf.add_item(
    #     'No results found',
    #     'Select to view google search',
    #     arg = 'http://www.google.com/',
    #     valid = True)


    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow(libraries=['./lib'])
    sys.exit(wf.run(main))