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
Translate DeepL API - select target language
"""

from __future__ import division, print_function, unicode_literals, absolute_import
import sys
import deepl_available_langs
from workflow import Workflow

def main(wf):
    for key, value in deepl_available_langs.AVAILABLE_LANGS.iteritems():
        wf.add_item(title=value['name'], valid=True, icon=value['icon'], arg=key)

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow(libraries=['./lib'])
    sys.exit(wf.run(main))