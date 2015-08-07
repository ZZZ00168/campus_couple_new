#!/usr/bin/python
# -*- coding: utf8 -*-
"""
author: 

update_time: 2015/7/30--13:23

apis:
    /user/follow/delete
"""

import route
import re

from output import *
from database import *

@route.route('/user/follow/delete')
class UserFollowDelete: #取消关注用户
    def POST(self):
        input = web.input(access_token = None, user_id = None, followed_id = None)
        db = getDb()

        if input.access_token == None or input.user_id == None or input.followed_id == None:
            return output(110)

        try :
            input.user_id = int(input.user_id)
            input.followed_id = int(input.followed_id)
        except:
            return output(111)

        #是否存在 用户ID
        results = db.select('user' , vars={'user_id':input.followed_id} , where = "user_id=$user_id")
        if len(results) == 0:
            return output(468)

        #用户权限
        results = db.select('token' , vars = {'access_token':input.access_token , 'user_id':input.user_id} ,
                            where = "user_id=$user_id and access_token=$access_token")
        if len(results) == 0:
            return output(410)

        try:
            db.delete("follow" , vars = {'user_id':input.user_id , 'followed_id':input.followed_id } ,
                        where = "user_id=$user_id and followed_id=$followed_id")
        except:
            return output(700)

        return output(200)
