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
        input = web.input(access_token=None, user_id=None, Last_post_id=None)
        if (input.access_token == None or input.user_id == None or input.Last_post_id == None):
            return output(110)
        db = getDb()
        try:
            result = db.select('token', vars={'user_id': input.user_id}, where="user_id=$user_id", what="access_token")
        except:
            return output(700)
        if len(result) != 1:
            return output(700)
        for i in result:
            if i.access_token != input.access_token:
                return output(410)
        try:
            # result=db.select('post,user',vars={'user_id':input.user_id},where="post.user_id=user.user_id and user.")
            campus = db.select('user', vars={'user_id': input.user_id}, where="user_id=$user_id", what="campus_id")
        except:
            return output(700)
        if len(campus) != 1:
            return output(700)
        for i in campus:
            campus_id = i.campus_id
        try:
            post_list= db.select('user,post', vars={'campus_id': campus_id},
                                  where="user.user_id=post.user_id and user.campus_id=$campus_id", what="post.post_id")
        except:
            return output(700)
        if len(post_list)==0:
            return output(467)
        maxId=0
        for i in post_list:
            maxId=max(i.post_id,maxId)
        if int(maxId)<=int(input.Last_post_id):
             return output(200,False)
        else:
             return output(200,True)

