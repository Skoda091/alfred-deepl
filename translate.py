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
            "lang": {"user_preferred_langs": ["EN", "DE"],
                    "source_lang_user_selected": "auto",
                    "target_lang": args.lang},
            "priority": 1}}
    r = requests.post('https://deepl.com/jsonrpc', data=json.dumps(payload))
    translations = json.loads(r.text)['result']['translations']
    result = ""
    for translation in translations:
        # print(translation)
        beams = sorted(translation['beams'], key=lambda b: -1 * b['score'])
        for beam in beams:
            wf.add_item(title=wf.decode(beam['postprocessed_sentence']), valid=True, icon=ICON_WEB)

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow(libraries=['./lib'])
    sys.exit(wf.run(main))