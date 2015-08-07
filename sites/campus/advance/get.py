#!/usr/bin/python
# -*- coding: utf8 -*-

import route
import web

from database import *
from output import *



@route.route('/campus/advance/time/get')
class CampusAdvanceTimeGet:
    def POST(self):
        input = web.input(access_token = None)

        if input.access_token == None:
            return output(110)
        db = getDb()
        campus_id = db.select('campus_token',vars = {'access_token' : input.access_token},
                              where = 'access_token=$access_token')

        if len(campus_id) == 0:
            return output(410)

        campus_id = campus_id[0].campus_id

        getAdvanceTime = db.select('campus',vars = {'campus_id' : campus_id},
                                   where= 'campus_id=$campus_id',
                                   what='advance_time')[0].advance_time

        return output(200, getAdvanceTime)

