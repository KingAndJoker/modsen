""" unit test /api/document/{id} """
import sys

sys.path.insert(1, "../")

from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase
from environs import Env

from seeding import seeding_from_csv, seeding_from_txt
from setup import setup


class TestSearchGet(AioHTTPTestCase):
    """TEST: get document with specified id=5"""

    async def get_application(self):
        """
        Override the get_app method to return your application.
        """

        env = Env()
        env.read_env()
        app = web.Application()
        setup(app, env=env)
        seeding_from_csv(app["engine"], path_to_csv="./../posts.csv")
        seeding_from_txt(app["engine"], path="./../documents.txt")
        
        return app

    async def test_search(self):
        """test search"""

        async with self.client.request(
            "GET", "/api/search?text=Все говорят: Изменись,и все за тобой потянуться"
        ) as resp:
            resp_json = await resp.json()
            self.assertEqual(
                resp_json["documents"][0]["text"],
                "Все говорят: Изменись,и все за тобой потянуться. "
                "А я лучше останусь собой и посмотрю, кто со мной остаётся!",
            )
