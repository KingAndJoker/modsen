""" API file """
import time

from aiohttp import web
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from app.models import Document
from app.schema import DocumentSchema

routes = web.RouteTableDef()


def get_config(
    request: web.Request,
) -> tuple[web.Application, Engine, Session, DocumentSchema]:
    """
    extracts from request and returns
    application, engine, session, document schema
    """

    app: web.Application = request.app
    engine = app["engine"]
    session: Session = Session(engine)  # app['session']
    document_schema: DocumentSchema = app["document_schema"]
    return app, engine, session, document_schema


@routes.view("/api/document/{id}")
class DocumentId(web.View):
    """
    Document handler
    GET /api/document/{id} - return JSON document
    if {id} miss return error

    DELETE /api/document/{id} - remove document with id
    """

    async def get(self) -> web.Response:
        """GET handler /api/document/{id}"""

        request: web.Request = self.request
        app, engine, session, document_schema = get_config(request)
        resp: dict = dict()
        status = 200

        id = request.match_info.get("id", None)

        if id:
            try:
                id = int(id)
            except ValueError as err:
                print(err.with_traceback)
                resp["error"] = 'id="{id}" is not correct'
                status = 400
                return web.json_response(resp, status=status)

            document = session.query(Document) \
                .filter(Document.id == id) \
                .one_or_none()

            if not document:
                resp["error"] = "item not found"
                status = 404
                return web.json_response(resp, status=status)

            resp["document"] = document_schema.dump(document)
        else:
            status = 400
            resp["error"] = "missing id"

        return web.json_response(resp, status=status)

    async def delete(self) -> web.Response:
        """DELETE handler /api/document/{id}"""

        request: web.Request = self.request
        app, engine, session, document_schema = get_config(request)
        resp: dict = dict()
        status = 200

        id = request.match_info.get("id", None)

        if id is not None:
            try:
                id = int(id)
            except ValueError as err:
                print(err.with_traceback)
                resp["error"] = 'id="{id}" is not correct'
                status = 400
                return web.json_response(resp, status=status)

            session.query(Document).filter(Document.id == id).delete()
            session.commit()

            resp["status"] = "Deletion completed successfully"
        else:
            status = 400
            resp["error"] = "missing id"

        return web.json_response(resp, status=status)


@routes.view("/api/search")
class Search(web.View):
    """
    Search handler
    GET /api/search?text=...
    search text in documents and return top 20, order by date
    """

    async def get(self):
        """GET handler /api/search"""

        request: web.Request = self.request
        app, engine, session, document_schema = get_config(request)
        params = request.rel_url.query
        resp: dict = dict()
        status = 200

        text = params.get("text", "")
        top = int(params.get("top", 20))

        documents = (
            session.query(Document)
            .filter(Document.text.ilike(f"%{text}%"))
            .order_by(Document.created_date.desc())
            .limit(top)
            .all()
        )

        documents = [document_schema.dump(document) for document in documents]

        resp["documents"] = documents

        return web.json_response(resp, status=status)
