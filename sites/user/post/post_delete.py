#!/usr/bin/python
# -*- coding: utf8 -*-
"""
author: nango
update_time: 2015/7/25--17:23
apis:
    /user/post/delete
"""

import route
import re
from database import *
from output import *
from encrypt import *
from verify import *


@route.route('/user/post/delete')
class UserPostDelete:
    def POST(self):  # 传入 access_token,user_id,post_id
        input = web.input(access_token='', user_id=0, post_id=0)
        # 判断参数是否齐全：
        if input.access_token == '' or input.user_id == 0 or input.post_id == 0:
            return output(110)  # 缺少必填参数
        # 判断参数类型
        try:
            input.user_id = int(input.user_id)
            input.post_id = int(input.post_id)
        except:
            return output(117)

        # 查看access_token 是否对应user_id
        db = getDb()
        user = db.select('token', vars={"access_token": input.access_token, "user_id": input.user_id},
                         where="user_id=$user_id and access_token=$access_token",what='user_id')
        if len(user) != 1:
            output(420)  # 权限不足
        t = db.transaction()
        try:
            # 删掉全部favor
            db.delete('favor', vars={'post_id': input.post_id}, where="post_id=$post_id")
            # 删掉全部评论 comments
            db.delete('comments', vars={'post_id': input.post_id}, where="post_id=$post_id")
            # 删掉该post
            db.delete('post', vars={'post_id': input.post_id}, where="post_id=$post_id")
        except:
            t.rollback()
            return output(700)
        else:
            t.commit()
            return output(200)
