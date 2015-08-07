#!/usr/bin/python
# -*- coding: utf8 -*-
#test
import web

def getDb():
    return web.database(dbn='mysql', db='campus_couple', user='root', pw='123456')
