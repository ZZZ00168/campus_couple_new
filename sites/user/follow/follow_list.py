#!/usr/bin/python
# -*- coding: utf8 -*-
"""
author: 

update_time: 2015/7/30--13:23

apis:
    /user/follow/list
"""

import route
import re

from database import *
from output import *


@route.route('/user/follow/list')
class UserFollowList:  # 获取我关注用户列表
    def POST(self):
        input = web.input(access_token=None, user_id=None)

        if input.access_token == None or input.user_id == None:
            return output(110)

        try:
            input.user_id = int(input.user_id)
        except:
            return output(111)

        # 用户权限

        db = getDb()

        results = db.select('token', vars={'access_token': input.access_token, 'user_id': input.user_id},
                            where="user_id=$user_id and access_token=$access_token")
        if len(results) != 1:
            return output(410)

        # 获取全部的关注人
        results = db.select('follow', vars={'user_id': input.user_id}, where="user_id=$user_id")
        if len(results) == 0:
            return output(200, [])

        follow_list = []
        try:
            for i in results:
                user_id = i.followed_id
                user_name = None
                user_img_url = None
                description = ''

                userinfos = db.select('userinfo', vars={'user_id': user_id}, where="user_id=$user_id")

                for j in userinfos:
                    if j.type == 'nickname':
                        user_name = j.information
                    elif j.type == 'img_url':
                        user_img_url = j.information
                    elif j.type == 'description':
                        description = j.information

                userinfos = db.select('user', vars = {'id':user_id}, where = "user_id=$id")[0]

                if user_name == None:
                    user_name = u'用户' + userinfos.mobile[-4:]

                sex = userinfos.sex
                if sex == None:
                    sex = 'm'

                follow_list.append({"user_id": user_id, "user_name": user_name, "sex": sex,
                             "user_img_url": user_img_url, "description": description})
            return output(200, follow_list)
        except:
            return output(700)
