#!/usr/bin/python
# -*- coding: utf8 -*-
"""
update_time: 2015/8/19 22:06

apis:
    /user/message/send
"""

import route
import web

from output import *
from database import *

@route.route('/user/message/send')
class UserMessageSend:  # 关注用户
    def POST(self):
        input = web.input(access_token = None, user_id = None, receiver_id = None, content = None)

        if(input.access_token == None or input.user_id == None or input.content == None or
           input.receiver_id == None):
            return output(110)

        try:
            input.user_id = int(input.user_id)
            input.receiver_id = int(input.receiver_id)
        except:
            return output(111)

        db = getDb()
        results = db.select('token', vars = {'token':input.access_token, 'id':input.user_id},
                            where = 'access_token=$token and user_id=$id')
        if len(results) == 0:
            return output(410)

        results = db.select('user', vars = {'id':input.receiver_id}, where = "user_id=$id")
        if len(results) == 0:
            return output(468)

        try:
            db.insert('messages', sender_i = input.user_id, receiver_id = input.receiver_id,
                      content = input.content, add_time = None)
        except:
            return output(700)

        return output(200)
