""" API file """
import time

from aiohttp import web
from sqlalchemy.orm import Session

from app.models import Document


routes = web.RouteTableDef()


@routes.view('/api/document/{id}')
class Document_Id(web.View):
    """
    Document handler
    GET /api/document/{id} - return JSON document
    if {id} miss return error

    """

    async def get(self) -> web.Response:
        """ GET handler /api/document/{id} """

        request: web.Request = self.request
        app: web.Application = request.app
        engine = app['engine']
        session: Session = Session(engine) # app['session']
        start_time = request['start_time']
        resp = {}
        status = 200

        id = request.match_info.get('id', None)

        if id is not None:
            try:
                id = int(id)
            except TypeError as err:
                print(err.with_traceback)
                resp['error'] = 'id="{id}" is not correct'
                status = 400
                resp['time'] = time.time() - start_time
                return web.json_response(resp, status=status)

            document = session.query(Document).filter(Document.id == id).one()
            rubrics = document.rubrics

            document = document.__dict__
            del document['_sa_instance_state']
            document['created_date'] = str(document['created_date'])

            document['rubrics'] = rubrics
            document['rubrics'] = [rubric.__dict__ for rubric in document['rubrics']]
            for rubric in document['rubrics']:
                del rubric['_sa_instance_state']

            resp['document'] = document
        else:
            status = 400
            resp['error'] = 'missing id'

        resp['time'] = time.time() - start_time
        return web.json_response(resp, status=status)
