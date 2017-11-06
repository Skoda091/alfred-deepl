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
from plistlib import readPlist, writePlist
from workflow import Workflow

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('query', default='EN', help="The language to translate into. Defaults to English.")
    return parser.parse_args(args)

def main(wf):
    args = parse_args(wf.args)
    info = readPlist('info.plist')
    info['variables']['target_lang'] = args.query
    writePlist(info, 'info.plist')
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow(libraries=['./lib'])
    sys.exit(wf.run(main))