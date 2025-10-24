#
# Copyright (C) 2025 pdnguyen of HCMC University of Technology VNU-HCM.
# All rights reserved.
# This file is part of the CO3093/CO3094 course.
#
# WeApRous release
#
# The authors hereby grant to Licensee personal permission to use
# and modify the Licensed Source Code for the sole purpose of studying
# while attending the course
#

"""
daemon.request
~~~~~~~~~~~~~~~~~

This module provides a Request object to manage and persist 
request settings (cookies, auth, proxies).
"""
from .dictionary import CaseInsensitiveDict

import json as json_module
from urllib.parse import urlencode
import base64

class Request():
    """The fully mutable "class" `Request <Request>` object,
    containing the exact bytes that will be sent to the server.

    Instances are generated from a "class" `Request <Request>` object, and
    should not be instantiated manually; doing so may produce undesirable
    effects.

    Usage::

      >>> import deamon.request
      >>> req = request.Request()
      ## Incoming message obtain aka. incoming_msg
      >>> r = req.prepare(incoming_msg)
      >>> r
      <Request>
    """
    __attrs__ = [
        "method",
        "url",
        "headers",
        "body",
        "reason",
        "cookies",
        "routes",
        "hook",
    ]

    def __init__(self):
        #: HTTP verb to send to the server.
        self.method = None
        #: HTTP URL to send the request to.
        self.url = None
        #: dictionary of HTTP headers.
        self.headers = None
        #: HTTP path
        self.path = None        
        # The cookies set used to create Cookie header
        self.cookies = None
        #: request body to send to the server.
        self.body = None
        
        #: Routes
        # e.g:
        # {
        #     ('GET', '/home'): home_handler,
        #     ('POST', '/login'): login_handler
        # }
        self.routes = {}



        #: Hook point for routed mapped-path
        self.hook = None  # lưu handler tương ứng với routes đc tìm thấy

    def extract_request_line(self, request):
        # GET /home.html HTTP/1.1  (dòng đầu của 1 request http(s))
        # hàm tách ra : method: get, path:/home.html, version: HTTP/1.1
        try:
            lines = request.splitlines()
            first_line = lines[0]
            method, path, version = first_line.split()

            if path == '/':
                path = '/index.html'
        except Exception:
            return None, None

        return method, path, version
             
    def prepare_headers(self, request):
        """Prepares the given HTTP headers."""
        # e.g
        #GET / HTTP/1.1 (ko xử lí ở đây)

        # xử lí phần này 
        # Host: www.example.com
        # User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
        # Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
        # Accept-Language: en-US,en;q=0.5
        # Connection: keep-alive
        # Cookie: session_id=abc12345; user_settings=dark_mode
        # If-Modified-Since: Tue, 01 Sep 2025 10:00:00 GMT

        lines = request.split('\r\n')
        headers = {}
        for line in lines[1:]: # bỏ dòng header đầu
            if ': ' in line:
                key, val = line.split(': ', 1)
                headers[key.lower()] = val
        return headers



    def prepare(self, request, routes=None):
        """Prepares the entire request with the given parameters."""

        # Prepare the request line from the request header
        self.method, self.path, self.version = self.extract_request_line(request)
        print("[Request] {} path {} version {}".format(self.method, self.path, self.version))

        #
        # @bksysnet Preapring the webapp hook with WeApRous instance
        # The default behaviour with HTTP server is empty routed
        #
        # TODO manage the webapp hook in this mounting point 
        #

        # KHÔNG XỬ LÝ HOOK Ở ĐÂY XỬ LÝ Ở BACKEND
        
        # if not routes == {}:
        #     self.routes = routes
        #     self.hook = routes.get((self.method, self.path))
        #     #
        #     # self.hook manipulation goes here
        #     # ...
        #     #

        self.headers = self.prepare_headers(request)
        cookies = self.headers.get('cookie', '')

        # e.g: cookie: session_id=abc12345; user_settings=dark_mode
        # parse cookies
        self.cookies = self._parse_cookies(cookies)
        self.body = self._extract_body(request)
        
            #
            #  TODO: implement the cookie function here
            #        by parsing the header            #

        return


        
    def _parse_cookies(self, cookie_header):

        cookies = {}
        if not cookie_header:
            return cookies
            
        for cookie in cookie_header.split(';'):
            cookie = cookie.strip()
            if '=' in cookie:
                key, value = cookie.split('=', 1)
                cookies[key] = value
        return cookies
       


    def prepare_body(self, data=None, files=None, json=None):
        # self.prepare_content_length(self.body)
        # self.body = body
        self.body = None

        #
        # TODO prepare the request authentication
        #
	# self.auth = ...
    

        self.body = None
        if json is not None:
            self.body = json_module.dumps(json).encode('utf-8')
            self.headers['content-type'] = 'application/json'

        elif data is not None:
            if isinstance(data, dict):
                self.body = urlencode(data).encode('utf-8')
                self.headers['content-type'] = 'application/x-www-form-urlencoded'

            elif isinstance(data, str):
                self.body = data.encode('utf-8')

            elif isinstance(data, (bytes, bytearray)):
                self.body = data

        # Note: file uploads not handled here
        self.prepare_content_length(self.body)
        return


    def prepare_content_length(self, body):
        self.headers["Content-Length"] = "0"
        #
        # TODO prepare the request authentication
        #
	# self.auth = ...
        length = len(body) if body else 0
        self.headers['Content-Length'] = str(length)
        
        return


    def prepare_auth(self, auth, url=""):
        #
        # TODO prepare the request authentication
        #
	# self.auth = ...

        if auth is None:
            return 
        
        if isinstance(auth, tuple) and len(auth) == 2:
            # Basic Auth
            
            username, password = auth

            credentials = f"{username}:{password}"
            encoded = base64.b64encode(credentials.encode()).decode('ascii')

            self.headers['Authorization'] = f'Basic {encoded}'
        
        elif isinstance(auth, str):
            # Bearer token
            self.headers['Authorization'] = f'Bearer {auth}'
        
        return



    def prepare_cookies(self, cookies):
            self.headers["Cookie"] = cookies
