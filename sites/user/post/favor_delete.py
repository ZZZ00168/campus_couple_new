#!/usr/bin/python
# -*- coding: utf8 -*-
"""
author:
update_time: 2015
apis:
    /user/post/favor/delete
"""

import route
import web
from output import *
from database import *


@route.route('/user/post/favor/delete')
class UserPostFavorAdd:
    def POST(self):  # 传入 access_token,user_id,post_id
        input = web.input(access_token='', post_id='', user_id='');
        if (input.access_token == '' or input.post_id == '' or input.user_id == ''):
            return output(110);
        db = getDb()
        user_id = db.select('token', vars={'access_token': input.access_token}, where="access_token=$access_token",
                            what='user_id')
        if len(user_id) == 0:
            return output(412)
        if_have = db.select('post', vars={'user_id': input.user_id, 'post_id': input.post_id})
        # todo 未点赞，用户想要删除点赞,则返回啥？
        if len(if_have) == 0:
            return output(233)
        try:
            db.delete('favor', vars={'post_id': input.post_id, 'user_id': input.user_id},
                      where="post_id=$post_id and user_id=$user_id")
        except:
            return output(700)
        return output(200)
