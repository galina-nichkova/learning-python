import unittest
from bs4 import BeautifulSoup
from web_scraping.parse import get_final_list
"""This test checks if parsing the BS object returns expected results"""


class GetFinalList(unittest.TestCase):
    def test_final_list(self):
        with open("test2_input.html", "r", encoding="utf-8") as f:
            contents = f.read()
        page_content = BeautifulSoup(contents, "html.parser")
        data_ids_list = ['110925072']
        result = get_final_list(data_ids_list, page_content)
        self.assertEqual(result, [{'id': '110925072', 'address': 'Heinrich-Roller-Straße 9, Prenzlauer Berg',
                                   'price': '790,40 €', 'living_space': '49,4 m²'}])


if __name__ == '__main__':
    unittest.main()
