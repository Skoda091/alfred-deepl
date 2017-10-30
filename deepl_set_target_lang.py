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
Translate DeepL API - set target language
"""

from __future__ import division, print_function, unicode_literals, absolute_import
import sys
import argparse
from workflow import Workflow3

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('query', default='EN', help="The language to translate into. Defaults to English.")
    return parser.parse_args(args)

def main(wf):
    args = parse_args(wf.args)
    log.debug('Target language: ' + format(args.query))
    wf.setvar('target_lang', args.query)
    # for key, value in AVAILABLE_LANGS.iteritems():
    #     wf.add_item(title=key, valid=True, icon=value['icon'], arg=value['iso_code'])

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow3(libraries=['./lib'])
    log = wf.logger
    sys.exit(wf.run(main))