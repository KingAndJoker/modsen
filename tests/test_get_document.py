""" unit test /api/document/{id} """
import unittest

import requests


class TestDocumentGet(unittest.TestCase):
    """ TEST: get document with specified id=5 """

    def test_get_document(self):
        """ test get document """

        resp = requests.get('http://localhost:8080/api/document/417')
        self.assertEqual(resp.json()['document']['text'],
                         'Все говорят: Изменись,и все за тобой потянуться. '
                         'А я лучше останусь собой и посмотрю, кто со мной остаётся!')

    def test_error_400(self):
        """ test status code=400 """

        resp = requests.get('http://localhost:8080/api/document/zxc')
        self.assertEqual(resp.status_code, 400)

    def test_error_404(self):
        """ test status code=404 """

        resp = requests.get('http://localhost:8080/api/document/12341234')
        self.assertEqual(resp.status_code, 404)
