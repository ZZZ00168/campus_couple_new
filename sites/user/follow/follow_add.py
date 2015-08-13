#!/usr/bin/python
# -*- coding: utf8 -*-
"""
update_time: 2015/7/30--13:23

apis:
    /user/followed/add
"""

import route
import web
import re

from output import *
from database import *


@route.route('/user/follow/add')
class UserfollowedAdd:  # 关注用户
    def POST(self):
        input = web.input(access_token=None, user_id=None, followed_id=None)
        if input.access_token == None or input.user_id == None or input.followed_id == None:
            return output(110)

        try:
            input.user_id = int(input.user_id)
            input.followed_id = int(input.followed_id)
        except:
            return output(111)

        db = getDb()
        # 是否存在 用户ID
        results = db.select('user', vars={'user_id': input.followed_id}, where="user_id=$user_id")
        if len(results) != 1:
            return output(468)

        # 用户权限
        results = db.select('token', vars={'access_token': input.access_token, 'user_id': input.user_id},
                            where="user_id=$user_id and access_token=$access_token")
        if len(results) != 1:
            return output(410)

        if len(db.select('follow', vars = {'user_id':input.user_id, 'followed_id':input.followed_id},
                         where = "user_id=$user_id and followed_id=$followed_id")) > 0:
            return output(200)

        try:
            db.insert('follow', user_id=input.user_id, followed_id=input.followed_id)
        except:
            return output(700)
        return output(200)
