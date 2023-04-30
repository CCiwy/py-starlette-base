#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Import Built-Ins
from typing import Protocol

class Controller(Protocol):
    def make_routes(self):
        ...


# Import Third-Party
from starlette.responses import Response


class BaseController:
    def __init__(self, app):
        self.app = app


    def response(self, data, status):
        return Response(data, status)

