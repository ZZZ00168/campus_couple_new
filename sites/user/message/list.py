#!/usr/bin/python
# -*- coding: utf8 -*-
"""
update_time: 2015/8/19 22:06

apis:
    /user/message/list
"""

import route
import web

from output import *
from database import *

@route.route('/user/message/list')
class UserMessageList:  # 关注用户
    def POST(self):
        input = web.input(access_token = None, user_id = None)

        if input.access_token == None or input.user_id == None:
            return output(110)

        try:
            input.user_id = int(input.user_id)
        except:
            return output(111)

        db = getDb()
        results = db.select('token', vars = {'token':input.access_token, 'id':input.user_id},
                            where = 'access_token=$token and user_id=$id')
        if len(results) == 0:
            return output(410)

        message_list = []

        results = db.select('messages', vars = {'id':input.user_id},
                            where = "receiver_id=id",
                            what = "sender_id,content,add_time")
        for message in results:
            message_list.append({'sender_id':message.sender_id,
                                 'content':message.content,
                                 'add_time':str(message.add_time)})

        try:
            db.delete('messages', vars = {'id':input.user_id}, where = "receiver_id=$id")
        except:
            return output(700)
        return output(200, message_list)
