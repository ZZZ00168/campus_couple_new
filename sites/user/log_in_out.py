#!/usr/bin/python
# -*- coding: utf8 -*-
"""
update_time: 2015/7/19--13:23
apis:
    /user/login
    /user/logout
"""

import route
import web
import random
import time

from database import *
from output import *
from encrypt import *
from mytoken import *

@route.route('/user/login')
class UserLogin:
    def POST(self):
        input = web .input(mobile = None, password = None)

        if input.mobile == None or input.password == None:
            return output(110)
        db = getDb()
        user = db.select('user', vars = {'mobile' : input.mobile},
                         where = "mobile=$mobile and verified='yes'",
                         what = "user_id,passwd")
        if len(user) != 1:
            return output(421)

        user = user[0]
        if user.passwd != encrypt(input.password):
            return output(430)

        token = db.select('token', vars = {'id' : user.user_id},
                          where = "user_id=$id")
        if len(token) > 0:
            token = token[0]
            try:
                db.update('token', vars = {'id' : user.user_id},
                          where = "user_id=$id", activate_time = None)
                return output(200, {'access_token' : token.access_token, 'user_id' : user.user_id})
            except:
                return output(700)

        else:
            try:
                while True:
                    token = encrypt(str(random.randint(100000, 1000000)) +
                                str(time.time()) + input.mobile)
                    results = db.select('token', vars = {'token' : token},
                              where = "access_token=$token")
                    if len(results) == 0:
                        break

                db.insert('token', access_token = token, user_id = user.user_id,
                          activate_time = None)
                return output(200, {'access_token' : token, 'user_id' : user.user_id})
            except:
                return output(700)

@route.route('/user/logout')
class UserLogout:
    def POST(self):
        input = web.input(access_token = None, user_id = None)
        if input.access_token == None or input.user_id == None:
            return output(110)

        try:
            input.user_id = int(input.user_id)
        except:
            return output(111)

        db = getDb()

        results = db.select('token', vars = {'token' : input.access_token, 'id' : input.user_id},
                            where = "access_token=$token and user_id=$id")
        if len(results) > 0:
            try:
                db.delete('token', vars = {'token' : input.access_token},
                            where = "access_token=$token")
                return output(200)
            except:
                return output(700)
        else:
            return output(410)

