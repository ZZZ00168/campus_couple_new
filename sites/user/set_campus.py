#!/usr/bin/python
# -*- coding: utf8 -*-

import web
import route

from output import output
from database import *

@route.route('/user/campus/set')
class UserCampusSet:
    def POST(self):
        input = web.input(access_token = None, user_id = None, campus_id = None)

        if (input.access_token == None or input.user_id == None or
            input.campus_id == None):
            return output(110)

        try:
            input.user_id = int(input.user_id)
            input.campus_id = int(input.campus_id)
        except:
            return output(111)

        db = getDb()

        results = db.select('campus', vars = {'id' : input.campus_id}, where = "campus_id=$id")
        if len(results) == 0:
            return output(460)

        results = db.select('token', vars = {'token' : input.access_token, 'id' : input.user_id},
                            where = "access_token=$token and user_id=$id")
        if len(results) == 0:
            return output(410)

        try:
            db.update('user', vars = {'id' : input.user_id}, where = "user_id=$id",
                      campus_id = input.campus_id)
            return output(200)
        except:
            return output(700)
