""" unit test /api/document/{id} """
import sys

sys.path.insert(1, './../')

from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase

from seeding import seeding
from setup import setup


class TestDocumentDelete(AioHTTPTestCase):
    """ TEST: delete document with specified id=5 """

    async def get_application(self):
        """
        Override the get_app method to return your application.
        """

        app = web.Application()
        setup(app, url_database='sqlite://')
        seeding(app['engine'], path_to_csv='./../posts.csv')

        return app

    async def test_delete_document(self):
        """ test delete document """

        async with self.client.request("DELETE", "/api/document/415") as resp:
            self.assertEqual(resp.status, 200)
        async with self.client.request("GET", "/api/document/415") as resp:
            self.assertEqual(resp.status, 404)

    async def test_error_400(self):
        """ test status code=400 """

        async with self.client.request("DELETE", "/api/document/zxc") as resp:
            self.assertEqual(resp.status, 400)
