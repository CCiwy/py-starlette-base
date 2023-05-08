#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Import Built-Ins
from typing import Protocol, Type, Any
from json.decoder import JSONDecodeError


import json

class Controller(Protocol):
    def make_routes(self):
        ...


# Import Third-Party
from starlette.responses import Response

from marshmallow.schema import Schema, EXCLUDE
from marshmallow.exceptions import ValidationError


from src.errors import DeserializeError


def serialize(data, schema: Type[Schema], many: bool =False) -> Type[Schema]:
    return schema(many=many).dumps(data, indent=4)


def deserialize(data: Any, schema: Type[Schema]) -> Type[Schema]:
    try:
        return schema(unknown=EXCLUDE).loads(data.decode())

    except ValidationError as e:
        raise e
    
    except JSONDecodeError as e:
        raise e


class BaseController:
    def __init__(self, app):
        self.app = app


    def response(self, data, status):
        return Response(data, status)


    def json_response(self, data, status, schema=None, many=False):
        content = (
            serialize(data, schema, many=many)
            if schema 
            else json.dumps(data)
            )

        return Response(content=content, status_code=status, media_type="application/json")


    def bad_request(self, msg):
        return self.response(msg, 400)


    def unauthorized(self, msg):
        return self.response(msg, 403)


    def internal_error(self, msg):
        return self.response(msg, 500)


    async def deserialize_request(self, request, schema):
        body = await request.body()

        try:
            data = deserialize(body, schema)
        except (ValidationError, JSONDecodeError) as e:
            raise DeserializeError.init_from(e)

        return data
