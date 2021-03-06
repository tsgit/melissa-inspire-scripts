#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from invenio.testutils import make_test_suite, \
    run_test_suite
from invenio.bibformat_engine import BibFormatObject
from invenio.bibformat_elements import bfe_INSPIRE_Hepnames_Arxiv_BAI_SEARCH

TESTREC1 = """<collection><record><controlfield tag="001">981878
              </controlfield><datafield tag="035" ind1=" " ind2=" ">
              <subfield code="a">zwirner_f_1</subfield><subfield 
              code="9">arXiv</subfield></datafield>
	      <datafield tag="100" ind1=" " ind2=" ">
	      <subfield code="a">Zwirner, Fabio</subfield></datafield>
	      </record></collection>
           """

TESTREC2 = """<collection><record><controlfield tag="001">982445
              </controlfield><datafield tag="035" ind1=" " ind2=" ">
              <subfield code="9">ARXIV</subfield>
              <subfield code="a">ARXIV-ZACHOS-C-1</subfield>
              </datafield><datafield tag="100" ind1=" " ind2=" ">
              <subfield code="a">Zachos, Cosmas K.</subfield></datafield>
              </record></collection>
           """

TESTREC3 = """<collection><record><controlfield tag="001">1017924
              </controlfield><datafield tag="100" ind1=" " ind2=" ">
              <subfield code="a">Atkinson, Robert L.</subfield>
              </datafield></record></collection>
           """

TESTREC4 = """<collection><record><controlfield tag="001">982447
              </controlfield><datafield tag="035" ind1=" " ind2=" ">
              <subfield code="9">ARXIV</subfield>
              <subfield code="a"></subfield></datafield>
              <datafield tag="100" ind1=" " ind2=" ">
              <subfield code="a">Zachariasen, Fred</subfield>
              </datafield></record></collection>
           """
TESTREC5 = """<collection><record><controlfield tag="001">1018662
              </controlfield><datafield tag="100" ind1=" " ind2=" ">
              <subfield code="a">de Alfaro, Vittorio</subfield>
              </datafield></record></collection>
           """

TESTREC6 = """<collection><record><controlfield tag="001">1016805
              </controlfield><datafield tag="100" ind1=" " ind2=" ">
              <subfield code="a">Ben-David, Ram Jacob</subfield>
              </datafield></record></collection>
           """

ARXIV_BAI_SEARCH_TEST = {
    TESTREC1: '<a href="http://arxiv.org/a/zwirner_f_1">[arXiv]</a>',
    TESTREC2: '<a href="http://arxiv.org/a/ARXIV-ZACHOS-C-1">[arXiv]</a>',
    TESTREC3: '<a href="https://arxiv.org/find/all/1/au:Zachariasen_F/0/1/0/all/0/1?per_page=100">[arXiv]</a>',
    TESTREC4: '<a href="https://arxiv.org/find/all/1/au:Atkinson_R/0/1/0/all/0/1?per_page=100">[arXiv]</a>',
    TESTREC5: '<a href="https://arxiv.org/find/all/1/au:Alfaro_V/0/1/0/all/0/1?per_page=100">[arXiv]</a>',
    TESTREC6: '<a href="https://arxiv.org/find/all/1/au:Ben_David_R/0/1/0/all/0/1?per_page=100">[arXiv]</a>'
}

class HepNames_arxiv_BAI_SEARCH_format_test(unittest.TestCase):
    def test4BAI_link(self):
        for key in ARXIV_BAI_SEARCH_TEST:
            bfo = BibFormatObject(None, xml_record=key)
            out = bfe_INSPIRE_Hepnames_Arxiv_BAI_SEARCH.format_element(bfo)
            self.assertEqual(ARXIV_BAI_SEARCH_TEST[key], out)

TEST_SUITE = make_test_suite(HepNames_arxiv_BAI_SEARCH_format_test)

if __name__ == "__main__":
    run_test_suite(TEST_SUITE)
