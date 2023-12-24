#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/11/21
# Tool:PyCharm

""" 追踪，增加请求id、时间等 """
__version__ = '0.0.1'
__history__ = """"""
__all__ = ['TraceMiddleware']

import time

from django.utils.deprecation import MiddlewareMixin

from shortcut_util.unique import uuid_id


class TraceMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request.META['HTTP-X-RequestID'] = request.META.get(
            'HTTP-X-RequestID', uuid_id())
        request.META['HTTP-X-RequestTS'] = int(time.time() * 1000)

    def process_response(self, request, response):
        response.headers['HTTP-X-RequestId'] = request.META['HTTP-X-RequestID']
        response.headers['HTTP-X-RequestTS'] = request.META['HTTP-X-RequestTS']
        response.headers['HTTP-X-ResponseTS'] = int(time.time() * 1000)
        response.headers['HTTP-X-TS'] = int(response.headers['HTTP-X-ResponseTS']) - \
            int(response.headers['HTTP-X-RequestTS'])
        return response
