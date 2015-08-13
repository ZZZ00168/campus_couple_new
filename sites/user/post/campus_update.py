#!/usr/bin/python
# -*- coding: utf8 -*-
"""
author: 

update_time: 2015/7/30--13:23

apis:
    /user/post/campus/update
"""
import web

import route
from output import *
from database import *


@route.route('/user/post/campus/update')
class UserPostCampusUpdate:  # 查询校区文章更新情况
    def POST(self):
        input = web.input(access_token=None, user_id=None, last_post_id=None)
        if (input.access_token == None or input.user_id == None or input.last_post_id == None):
            return output(110, False)

        try:
            input.user_id = int(input.user_id)
            input.last_post_id = int(input.last_post_id)
        except:
            return output(111, False)

        db = getDb()
        results = db.select('token', vars = {'user_id': input.user_id, 'token':input.access_token},
                               where="user_id=$user_id and access_token=$token")

        if len(results) == 0:
            return output(410, False)

        campus_id = db.select('user', vars = {'id' : input.user_id}, where = "user_id=$id",
                                what = 'campus_id')[0].campus_id
        try:
            campus_id = int(campus_id)
            if campus_id <= 0:
                return output(460, False)
        except:
            return output(460, False)


        results = db.select('post,user', vars = {'id':input.last_post_id,
                                                 'campus_id':campus_id},
                                where = "post_id>$id and user.user_id=post.user_id and user.campus_id=$campus_id",
                                what = "post.post_id as post_id",
                                limit = "0, 1")

        if len(results) > 0:
            return output(200, True)
        else:
            return output(200, False)
