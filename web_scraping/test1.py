from bs4 import BeautifulSoup
import unittest
from parse import get_data_ids
"""This test checks if the function parse returns a non-empty list"""

class GetDataIds(unittest.TestCase):

    def test_returns_data_ids(self):
        test_object = BeautifulSoup('''<li class="result-list__listing " data-id="110126101">
<li class="result-list__listing " data-id="110126102">
<li class="result-list__listing " data-id="110126103">
<li class="result-list__listing " data-id="110126104">
<li class="result-list__listing " data-id="110126105">''', "html.parser")
        result = get_data_ids(test_object)
        self.assertEqual(result, ['110126101', '110126102', '110126103', '110126104', '110126105'])

if __name__ == '__main__':
    unittest.main()
