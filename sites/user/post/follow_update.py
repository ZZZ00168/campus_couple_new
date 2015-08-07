#!/usr/bin/python
# -*- coding: utf8 -*-
"""
author: nango
update_time: 2015/7/30--11:23

apis:
    /user/post/follow/update
"""

import route
import re
import web
from database import *
from output import *
from encrypt import *
from verify import *


@route.route('/user/post/follow/update')
class UserPostFollowUpdate:  # 查询关注用户的文章更新情况
    def POST(self):  # 传入access_token,user_id,last_post_id
        input = web.input(access_token=None, user_id=None, last_post_id=None)

        # 缺少必填参数
        if input.access_token == None or input.user_id == None or input.post_id == None:
            return output(110, False)
        try:
            input.user_id = int(input.user_id)
            input.last_post_id = int(input.post_id)
        except:
            return output(111, False)
        try:
            db = getDb()
            results = db.select('token', vars={'user_id': input.user_id, 'access_token': input.access_token},
                                where="user_id=$user_id and access_token=$access_token")
            # access_token权限不足
            if len(results) != 1:
                return output(410, False)
            # 查询是否存在post_id
            post_ids = db.select('post', vars={'post_id': input.last_post_id},
                                 where='post_id=$post_id', what='post_id')
            if len(post_ids) != 1:
                return output(467, False)  # post_id不存在
            # 查找user_id的所关注人的post_id

            results = db.select('follow', vars={'user_id': input.user_id},
                                where="user_id=$user_id")
            for i in results:
                followed_post_list = db.select('post', vars={'user_id': i.followed_id},
                                               where="user_id=$user_id", what='post_id')
                for j in followed_post_list:
                    if int(input.last_post_id) < int(j.post_id):
                        return output(200, True)
        except:
            return output(700, False)

