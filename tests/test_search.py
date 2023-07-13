""" unit test /api/document/{id} """
import unittest

import requests


class TestSearchGet(unittest.TestCase):
    """ TEST: get document with specified id=5 """

    def test_search(self):
        """ test search """

        resp = requests.get('http://localhost:8080/api/search?text=Все говорят: Изменись,и все за тобой потянуться')
        self.assertEqual(resp.json()['documents'][0]['text'],
                         'Все говорят: Изменись,и все за тобой потянуться. '
                         'А я лучше останусь собой и посмотрю, кто со мной остаётся!')
