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
        input = web.input(access_token='', post_id='', user_id='');
        if (input.access_token == '' or input.post_id == '' or input.user_id == ''):
            return output(110);
        db = getDb()
        owner_id = db.select('token', vars={'access_token': input.access_token}, where="access_token=$access_token",
                             what='user_id')
        if len(owner_id)==0:
            return output(412)
        if_have=db.select('post',vars={'user_id':input.user_id,'post_id':input.post_id})
        #todo 已点赞，再次点赞则返回啥？
        if len(if_have)!=0:
            return output(233)

        try:
            db.insert('favor',post_id=input.post_id,user_id=input.user_id)
        except:
            return output(700)
        return output(200)
