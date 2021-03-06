#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script to add OSTI ID to HEP records with a corresponding DOI
"""

import re
from invenio.search_engine import perform_request_search, get_record
from invenio.bibrecord import print_rec, record_add_field
from invenio.bibformat_engine import BibFormatObject


def create_xml(recid=None, osti_id=None, doi=None):
    osti_exists = False
    doi_exists = False
    osti_mismatch = False
    mismatches = []
    osti_subfields = [('9', 'OSTI'), ('a', osti_id)]
    record = get_record(recid)
    record_link = '<a href="http://inspirehep.net/record/%s">%s</a>' % (str(recid),str(recid))
    append_record = {}
    additions = False
    errors = None
    for item in BibFormatObject(recid).fields('035__'):
        if item.has_key('9') and item.has_key('a'):
            if item['9'] == 'OSTI' and item['a'] == osti_id:
                osti_exists = True
            elif item['9'] == 'OSTI' and item['a'] != osti_id:
                osti_mismatch = True
                mismatches.append(item['a'])
    for item in BibFormatObject(recid).fields('0247_'):
        if item.has_key('2') and item.has_key('a'):
            if item['2'] == 'DOI' and item['a'] == doi:
                doi_exists = True
    if osti_exists is False and osti_mismatch is True:
        print str(recid), "already has a different OSTI ID"
        errors = "doi %s in record %s should match OSTI ID %s, but the record already contains OSTI ID(s) %s<br />" % (doi, record_link, osti_id, ','.join(mismatches))
        return errors
    if doi_exists is False and osti_exists is True:
        print str(recid), "contains an OSTI ID but no doi"
        no_doi = "%s contains OSTI ID %s but not doi %s<br />"  % (record_link, osti_id, doi)
        return no_doi
    if osti_exists is False and osti_mismatch is False:
        record_add_field(append_record, '001', controlfield_value=str(recid))
        record_add_field(append_record, '035', '', '', subfields=osti_subfields)
        print "%s: added 035__a:%s" % (str(recid), osti_id)
        return print_rec(append_record)


def main():
   # input = open('osti-ids-dois.txt', 'r')
#    output = open('tmp_osti_ids_dois_append.out', 'w')
#    errors = open('tmp_osti_ids_dois_errors.html', 'w')
#    done = open('checked-osti-ids.out', 'r+')
#    output.write("<collection>")
#    paper_list = []
    paper_dict = {}
    skip_dict = {}
    done_list = []
    errors_list = []
    recid_counter = 0
    update_counter = 0
    error_counter = 0
    with open('checked-osti-ids.out', 'r') as skip:
        for line in skip.readlines():
            matchObj = re.search(r'(\d+)\t(10.*?)', line)
            if matchObj:
                skip_dict[str(matchObj.group(1))] = matchObj.group(2)
#        skip_list = [line for line in skip.readlines()]
    """Creates a list of tuples of OSTI provided matches of OSTI IDs and DOIs, skipping OSTI IDs that have previously been uploaded"""
    with open('osti-ids-dois.txt', 'r') as input:
        for line in input.readlines():
            matchObj = re.search(r'(\d+)\t(10.*?)\s|$', line)
            if matchObj:
                if not matchObj.group(1) in skip_dict:
#                    paper_list.append((str(matchObj.group(1)), (matchObj.group(2))))
                    paper_dict[str(matchObj.group(1))] = matchObj.group(2)
    print "%s papers to search" % len(paper_dict)
    with open('tmp_osti_ids_dois_append.out', 'w') as output:
        output.write("<collection>")
#        for paper in paper_list:
        for key, value in paper_dict.iteritems():
            if update_counter < 1000:
                search = "0247_a:%s or (035__a:%s 035__9:OSTI)" % (value, key)
                html_search = '<a href="https://inspirehep.net/search?p=%s">%s</a>' % (search, search)
                html_search = re.sub(' ', '+', html_search)
                results = perform_request_search(p=search, cc='HEP')
                if len(results) > 1:
                    """records instances where INSPIRE has separate records for a matched DOI and OSTI ID"""
                    mismatch = ['<a href="https://inspirehep.net/record/%s">%s</a>' % (str(r), str(r)) for r in results]
                    error_counter += 1
                    errors_list.append("Mismatch: %s => %s<br />" % (html_search, ' '.join(mismatch)))
                if len(results) == 1:
                    for r in results:
                        recid_counter += 1
                        update = create_xml(recid=r, osti_id=key, doi=value)
                        if update:
                            error_phrases = ("record already contains", "but not doi")
                            if "<record>" in update:
                                """If DOI found in INSPIRE without associated OSTI ID, writes MARCXML to append ID"""
                                update_counter += 1
                                output.write(update)
                                """Includes OSTI ID in list to be skipped the next time the script is run"""
                                with open('checked-osti-ids.out', 'r+') as done:
                                    done.write("%s\t%s\n" % (key, value))
                            if any(x in update for x in error_phrases):
                                """records INSPIRE records to be checked for errors/missing DOIs"""
                                error_counter += 1
                                errors_list.append(update)
        output.write("</collection>")
    print "%i of %i records updated" % (update_counter, recid_counter)
    print "%i errors" % error_counter
#    output.write("</collection>")
#    output.close()
    with open('tmp_osti_ids_dois_errors.html', 'w') as errors:
        errors.write(''.join(errors_list))
#    errors.close()
    #input.close()
    #done.close()
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print 'Exiting'
