import unittest
from bs4 import BeautifulSoup
from parse import get_final_list
"""This test checks if the list returned by the function parse contains at least one non-empty dictionary"""


class GetFinalList(unittest.TestCase):
    def test_final_list(self):
        page_content = BeautifulSoup('''<button class="button-link link-internal result-list-entry__map-link" data-result-id="110126101" title="Auf der Karte anzeigen">
                     <div class="font-ellipsis">
                      Winsstraße 13, Prenzlauer Berg (Prenzlauer Berg), Berlin
                     </div>
                    </button>
                   </div>
                  </div>
                  <div class="result-list-entry__criteria margin-bottom-s">
                   <div>
                    <div class="grid grid-flex gutter-horizontal-l gutter-vertical-s" data-is24-qa="attributes">
                     <dl class="grid-item result-list-entry__primary-criterion " role="presentation">
                      <dd class="font-nowrap font-line-xs">
                       745 €
                      </dd>
                      <dt class="font-s onlyLarge">
                       Kaltmiete
                      </dt>
                     </dl>
                     <dl class="grid-item result-list-entry__primary-criterion " role="presentation">
                      <dd class="font-nowrap font-line-xs">
                       55,58 m²
                      </dd>
                      <dt class="font-s onlyLarge">
                       Wohnfläche
                     </dl>''', "html.parser")
        data_ids_list = ['110126101']
        result = get_final_list(page_content, data_ids_list)
        self.assertEqual(result, [{'id': '110126101', 'address': 'Winsstraße 13, Prenzlauer Berg (Prenzlauer Berg), Berlin',
                                   'price': '745 €', 'living_space': '55,58 m²'}])


if __name__ == '__main__':
    unittest.main()
