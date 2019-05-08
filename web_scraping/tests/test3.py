import unittest
import sqlite3
from web_scraping.parse import write_to_database
"""This test checks if the function write_to_database creates expected entries in the database"""

class TestDatabaseInsert(unittest.TestCase):
    def test_database_insert(self):
        test_data = [{'id': '110925072', 'address': 'Heinrich-Roller-Straße 9, Prenzlauer Berg', 'price': '790,40 €', 'living_space': '49,4 m²'}, {'id': '110925073', 'address': 'Heinrich-Heine-Straße 9, Prenzlauer Berg',
                                   'price': '890,40 €', 'living_space': '30,4 m²'}]
        write_to_database(test_data)
        conn = sqlite3.connect('rent_offers.db')
        c = conn.cursor()
        c.execute("select id from rent_offers where address = 'Heinrich-Roller-Straße 9, Prenzlauer Berg'")
        result = c.fetchall()
        conn.close()
        self.assertEqual(result[0][0], '110925072')

if __name__ == '__main__':
    unittest.main()
