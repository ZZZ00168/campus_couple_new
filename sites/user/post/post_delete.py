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
import os
import os.path

from database import *
from output import *
from encrypt import *
from verify import *


@route.route('/user/post/delete')
class UserPostDelete:
    def POST(self):  # 传入 access_token,user_id,post_id
        input = web.input(access_token=None, user_id=None, post_id=None)
        # 判断参数是否齐全：
        if input.access_token == None or input.user_id == None or input.post_id == None:
            return output(110)  # 缺少必填参数
        # 判断参数类型
        try:
            input.user_id = int(input.user_id)
            input.post_id = int(input.post_id)
        except:
            return output(111)

        # 查看access_token 是否对应user_id
        db = getDb()
        user = db.select('token', vars={"access_token": input.access_token, "user_id": input.user_id},
                         where="user_id=$user_id and access_token=$access_token",what='user_id')
        if len(user) != 1:
            return output(410)  # 权限不足

        results = db.select('post', vars = {'id':input.post_id}, where = 'post_id=$id')
        if len(results) == 0:
            return output(467)
        results = results[0]

        if results.user_id != input.user_id:
            return output(410)

        original_filename = results.img_url
        thumbnail_filename = results.thumbnail_img_url
        if original_filename == None:
            original_filename = ''
        else:
            original_filename = ('/var/campus_couple_img/static/' +
                                original_filename[original_filename.rfind('/') + 1:])
        if thumbnail_filename == None:
            thumbnail_filename = ''
        else:
            thumbnail_filename = ('/var/campus_couple_img/static/' +
                                thumbnail_filename[thumbnail_filename.rfind('/') + 1:])

        t = db.transaction()
        try:
            # 删掉全部favor
            db.delete('favor', vars={'post_id': input.post_id}, where="post_id=$post_id")
            # 删掉全部评论 comments
            db.delete('comments', vars={'post_id': input.post_id}, where="post_id=$post_id")
            # 删掉该post
            db.delete('post', vars={'post_id': input.post_id}, where="post_id=$post_id")

            if os.path.exists(original_filename) == True:
                os.remove(original_filename)
            if os.path.exists(thumbnail_filename) == True:
                os.remove(thumbnail_filename)
        except:
            t.rollback()
            return output(700)
        else:
            t.commit()
            return output(200)
