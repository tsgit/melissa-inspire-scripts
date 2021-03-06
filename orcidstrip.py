# -*- coding: utf-8 -*-
##
## This file is part of INSPIRE.
## Copyright (C) 2017 CERN.
##
## INSPIRE is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## INSPIRE is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with INSPIRE; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.


"""To strip leading and trailing characters from ORCID Ids"""
testrecord = 1611776
import re

fields = ['100__j', '700__j']
orcid = re.compile("(?i)ORCID:\w{4}-\w{4}-\w{4}-\w{4}")

def check_record(record, fields):
    for pos,val in record.iterfields(fields):
        if val:
            orcidsearch = orcid.search(val)
            if orcidsearch:
                if orcidsearch.group(0) != val:
#                    record_modify_subfield(pos[0][0:3], pos[0][5], orcidsearch.group(0), pos[2], field_position_global=pos[1])
#                    record.set_amended("%s: %s:%s changed to %s:%s" % (record.record_id, pos[0], val, pos[0], orcidsearch.group(1)))
                    print "%s: %s:%s changed to %s:%s" % (record.record_id, pos[0], val, pos[0], orcidsearch.group(0))
