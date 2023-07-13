""" unit test /api/document/{id} """
import sys
sys.path.insert(1, '../')

from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase

from setup import setup
from seeding import seeding


class TestSearchGet(AioHTTPTestCase):
    """ TEST: get document with specified id=5 """

    async def get_application(self):
        """
        Override the get_app method to return your application.
        """

        app = web.Application()
        setup(app, url_database='sqlite://')
        seeding(app['engine'], path_to_csv='./../posts.csv')
        return app

    async def test_search(self):
        """ test search """

        async with self.client.request("GET", "/api/search?text=Все говорят: Изменись,и все за тобой потянуться") as resp:
            resp_json = await resp.json()
            self.assertEqual(resp_json['documents'][0]['text'],
                             'Все говорят: Изменись,и все за тобой потянуться. '
                             'А я лучше останусь собой и посмотрю, кто со мной остаётся!')
