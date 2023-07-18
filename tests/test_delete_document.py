""" unit test /api/document/{id} """
import sys

sys.path.insert(1, "./../")

from environs import Env
from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase

from seeding import seeding_from_csv, seeding_from_txt
from setup import setup


class TestDocumentDelete(AioHTTPTestCase):
    """TEST: delete document with specified id=5"""

    async def get_application(self):
        """
        Override the get_app method to return your application.
        """
        
        env = Env()
        env.read_env()
        app = web.Application()
        setup(app, env=env)
        # seeding_from_csv(app["engine"], path_to_csv="./../posts.csv")
        seeding_from_txt(app["engine"], path="./../documents.txt")

        return app

    async def test_delete_document(self):
        """test delete document"""

        async with self.client.request("DELETE", "/api/document/415") as resp:
            self.assertEqual(resp.status, 200)
        async with self.client.request("GET", "/api/document/415") as resp:
            self.assertEqual(resp.status, 404)

    async def test_error_400(self):
        """test status code=400"""

        async with self.client.request("DELETE", "/api/document/zxc") as resp:
            self.assertEqual(resp.status, 400)
