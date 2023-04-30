#!/usr/bin/env python
# -*- coding: utf-8 -*-

from starlette.responses import Response


class BaseController:
    def __init__(self, app):
        self.app = app


    def response(self, data, status):
        return Response(data, status)

