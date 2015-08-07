#!/usr/bin/python
# -*- coding: utf8 -*-
urls = []

def getURLs():
    return tuple(urls)

def route(route_path):
    def _route(aClass):
        urls.append(route_path)
        urls.append(aClass)
        return aClass
    return _route

