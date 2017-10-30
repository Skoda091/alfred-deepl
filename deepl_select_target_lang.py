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
from workflow import Workflow

AVAILABLE_LANGS = {
    'German': {'iso_code': 'DE', 'icon': 'lang_icons/de.png'},
    'English': {'iso_code': 'EN', 'icon': 'lang_icons/en.png'},
    'French': {'iso_code': 'FR', 'icon': 'lang_icons/fr.png'},
    'Spanish': {'iso_code': 'ES', 'icon': 'lang_icons/es.png'},
    'Italian': {'iso_code': 'IT', 'icon': 'lang_icons/it.png'},
    'Dutch': {'iso_code': 'NL', 'icon': 'lang_icons/nl.png'},
    'Polish': {'iso_code': 'PL', 'icon': 'lang_icons/pl.png'}
}

def main(wf):
    for key, value in AVAILABLE_LANGS.iteritems():
        wf.add_item(title=key, valid=True, icon=value['icon'], arg=value['iso_code'])

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow(libraries=['./lib'])
    sys.exit(wf.run(main))