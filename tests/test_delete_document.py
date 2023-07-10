""" unit test /api/document/{id} """
import unittest

import requests


class TestDocumentDelete(unittest.TestCase):
    """ TEST: delete document with specified id=5 """

    def test_document(self):
        """ test """

        resp = requests.delete('http://localhost:8080/api/document/415')
        self.assertEqual(resp.status_code, 200)
        resp = requests.get('http://localhost:8080/api/document/415')
        self.assertEqual(resp.status_code, 404)

    def test_error_400(self):
        """ test """

        resp = requests.delete('http://localhost:8080/api/document/zxc')
        self.assertEqual(resp.status_code, 400)
