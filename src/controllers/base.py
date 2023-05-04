#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Import Built-Ins
from typing import Protocol, Type, Any
from json.decoder import JSONDecodeError


class Controller(Protocol):
    def make_routes(self):
        ...


# Import Third-Party
from starlette.responses import Response

from marshmallow.schema import Schema, EXCLUDE
from marshmallow.exceptions import ValidationError


class DeserializeError(RuntimeError):
    pass

def serialize(data, schema: Type[Schema], many: bool =False) -> Type[Schema]:
    return schema(many=many).dumps(data, indent=4)


def deserialize(data: Any, schema: Type[Schema]) -> Type[Schema]:
    try:
        return schema(unknow=EXCLUDE).loads(data.decode())

    except [ValidationError, JSONDecodeError] as e:
        raise DeserializeError()

class BaseController:
    def __init__(self, app):
        self.app = app


    def response(self, data, status):
        return Response(data, status)


    async def deserialize_request(self, request, schema):
        body = await request.body()

        try:
            data = deserialize(body, schema)
        except DeserializeError as e:
            raise e

        return data
