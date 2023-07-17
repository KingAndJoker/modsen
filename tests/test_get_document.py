""" unit test /api/document/{id} """
import sys

sys.path.insert(1, '../')

from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase

from seeding import seeding
from setup import setup


class TestDocumentGet(AioHTTPTestCase):
    """ TEST: get document with specified id=5 """

    async def get_application(self):
        """
        Override the get_app method to return your application.
        """

        app = web.Application()
        setup(app, url_database='sqlite://')
        seeding(app['engine'], path_to_csv='./../posts.csv')

        return app

    async def test_get_document(self):
        """ test get document """

        # resp = requests.get('http://localhost:8080/api/document/417')
        # self.assertEqual(resp.json()['document']['text'],
        #                  'Все говорят: Изменись,и все за тобой потянуться. '
        #                  'А я лучше останусь собой и посмотрю, кто со мной остаётся!')
        async with self.client.request("GET", "/api/document/417") as resp:
            resp_json = await resp.json()
            self.assertEqual(resp_json['document']['text'], 'Все говорят: Изменись,и все за тобой потянуться. А я лучше останусь собой и посмотрю, кто со мной остаётся!')

    async def test_error_400(self):
        """ test status code=400 """

        async with self.client.request("GET", "/api/document/zxc") as resp:
            self.assertEqual(resp.status, 400)

    async def test_error_404(self):
        """ test status code=404 """

        async with self.client.request("GET", "/api/document/123123123112") as resp:
            self.assertEqual(resp.status, 404)
