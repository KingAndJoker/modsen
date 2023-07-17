""" unit test /api/document/{id} """
import sys

sys.path.insert(1, "../")

from environs import Env

from setup import setup
from seeding import seeding
from aiohttp.test_utils import AioHTTPTestCase
from aiohttp import web


class TestDocumentGet(AioHTTPTestCase):
    """TEST: get document with specified id=5"""

    async def get_application(self):
        """
        Override the get_app method to return your application.
        """

        env = Env()
        env.read_env()
        app = web.Application()
        setup(app, env=env)
        seeding(app["engine"], path_to_csv="./../posts.csv")

        return app

    async def test_get_document(self):
        """test get document"""

        async with self.client.request("GET", "/api/document/417") as resp:
            resp_json = await resp.json()
            self.assertEqual(
                resp_json["document"]["text"],
                (
                    "Все говорят: Изменись,и все за тобой потянуться. А я лучше "
                    "останусь собой и посмотрю, кто со мной остаётся!"
                ),
            )

    async def test_error_400(self):
        """test status code=400"""

        async with self.client.request("GET", "/api/document/zxc") as resp:
            self.assertEqual(resp.status, 400)

    async def test_error_404(self):
        """test status code=404"""

        async with self.client.request("GET", "/api/document/123123") as resp:
            self.assertEqual(resp.status, 404)
