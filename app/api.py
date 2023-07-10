""" API file """
import time

from aiohttp import web
from sqlalchemy.orm import Session

from app.models import (
    Document,
    Rubric
)


routes = web.RouteTableDef()


@routes.view('/api/document/{id}')
class DocumentId(web.View):
    """
    Document handler
    GET /api/document/{id} - return JSON document
    if {id} miss return error

    DELETE /api/document/{id} - remove document with id
    """

    async def get(self) -> web.Response:
        """ GET handler /api/document/{id} """

        request: web.Request = self.request
        app: web.Application = request.app
        engine = app['engine']
        session: Session = Session(engine)  # app['session']
        start_time = request['start_time']
        resp = {}
        status = 200

        id = request.match_info.get('id', None)

        if id is not None:
            try:
                id = int(id)
            except ValueError as err:
                print(err.with_traceback)
                resp['error'] = 'id="{id}" is not correct'
                status = 400
                return web.json_response(resp, status=status)

            document = session.query(Document).filter(
                Document.id == id).one_or_none()
            rubrics = document.rubrics if document is not None else None

            if document is None:
                resp['error'] = 'item not found'
                status = 404
                return web.json_response(resp, status=status)

            document = document.__dict__
            del document['_sa_instance_state']
            document['created_date'] = str(document['created_date'])

            document['rubrics'] = rubrics
            document['rubrics'] = [
                rubric.__dict__ for rubric in document['rubrics']]
            for rubric in document['rubrics']:
                del rubric['_sa_instance_state']

            resp['document'] = document
        else:
            status = 400
            resp['error'] = 'missing id'

        return web.json_response(resp, status=status)

    async def delete(self) -> web.Response:
        """ DELETE handler /api/document/{id} """

        request: web.Request = self.request
        app: web.Application = request.app
        engine = app['engine']
        session: Session = Session(engine)  # app['session']
        start_time = request['start_time']
        resp = {}
        status = 200

        id = request.match_info.get('id', None)

        if id is not None:
            try:
                id = int(id)
            except ValueError as err:
                print(err.with_traceback)
                resp['error'] = 'id="{id}" is not correct'
                status = 400
                return web.json_response(resp, status=status)

            session.query(Rubric).filter(Rubric.document_id == id).delete()
            session.query(Document).filter(Document.id == id).delete()
            session.commit()

            resp['status'] = 'Deletion completed successfully'
        else:
            status = 400
            resp['error'] = 'missing id'

        return web.json_response(resp, status=status)


@routes.view('/api/search')
class Search(web.View):
    """
    Search handler
    GET /api/search?text=...
    search text in documents and return top 20, order by date
    """

    async def get(self):
        """ GET handler /api/search """

        request: web.Request = self.request
        app: web.Application = request.app
        engine = app['engine']
        session: Session = app['session']
        params = request.rel_url.query
        start_time = request['start_time']
        resp = {}
        status = 200

        text = params.get('text', '')
        top = int(params.get('top', 20))

        documents = session.query(Document). \
            filter(Document.text.ilike(f'%{text}%')). \
            order_by(Document.created_date.desc()). \
            limit(top). \
            all()

        for i in range(len(documents)):
            rubrics = documents[i].rubrics
            rubrics = [rubric.__dict__ for rubric in rubrics]
            for rubric in rubrics:
                del rubric['_sa_instance_state']

            documents[i] = documents[i].__dict__
            documents[i]['created_date'] = str(documents[i]['created_date'])
            del documents[i]['_sa_instance_state']
            documents[i]['rubrics'] = rubrics

        resp['documents'] = documents

        return web.json_response(resp, status=status)
