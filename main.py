#!/usr/bin/env python
# -*- coding: utf8 -*-
import web
import route
import cgi
import sites

if __name__ == "__main__":
    cgi.maxlen = 10 * 1024 * 1024
    app = web.application(route.getURLs(), globals())
    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run()
