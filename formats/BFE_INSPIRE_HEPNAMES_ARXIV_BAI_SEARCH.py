﻿# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2017 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
"""BibFormat element - Prints arXiv BAI hotlink directly under name if available, otherwise prints arXiv search

"""

def format_element(bfo):
    """
    Provides HepNames detailed BFT with an arXiv author ID url
    using 035__a if 035__9 is arxiv.
    """

    # base URL for arXiv author pages
    ARXIVAU = 'http://arxiv.org/a/'

    bai = bfo.fields('035__')
    no_arxiv = True

    for item in bai:
        if item.get('9') and item['9'].lower() == 'arxiv' and item.get('a'):
            no_arxiv = False
            return "%s%s" % (ARXIVAU,item['a'])


    if no_arxiv:
        return 'http://arxiv.org/find/all/1/au:<BFE_INSPIRE_HEPNAMES_ARXIV />/0/1/0/all/0/1?per_page=100'

# pylint: disable=W0613
def escape_values(bfo):
    """
    Called by BibFormat in order to check if output of this element
    should be escaped.
    """

    return 0
# pylint: enable=W0613
