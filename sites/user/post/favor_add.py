#!/usr/bin/python
# -*- coding: utf8 -*-
"""
author:
update_time: 2015
apis:
    /user/post/favor/add
"""

import web

import route
from output import *
from database import *


@route.route('/user/post/favor/add')
class UserPostFavorAdd:
    def POST(self):  # 传入 access_token,user_id,post_id
        input = web.input(access_token=None, post_id=None, user_id=None)
        if (input.access_token == None or input.post_id == None or input.user_id == None):
            return output(110)
         # 判断参数类型
        try:
            input.user_id = int(input.user_id)
            input.post_id = int(input.post_id)
        except:
            return output(111)
        db = getDb()
        owner_id = db.select('token', vars={'access_token': input.access_token,'user_id':input.user_id},
                             where="access_token=$access_token and user_id=$user_id",
                             what='user_id')
        if len(owner_id) == 0:
            return output(410)

        if len(db.select('post', vars = {'id':input.post_id}, where = "post_id=$id")) == 0:
            return output(467)

        if len(db.select('favor', vars = {'post_id':input.post_id, 'user_id':input.user_id},
                         where = "post_id=$post_id and user_id=$user_id")) > 0:
            return output(200)

        try:
            db.insert('favor', post_id=input.post_id, user_id=input.user_id)
        except:
            return output(700)
        return output(200)
