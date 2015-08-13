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


        try:
            where = 'post.post_id>$id and post.user_id=follow.followed_id '
            where += 'and follow.user_id=$user_id'
            results = db.select('post,follow', vars = {'id':input.last_post_id,
                                                       'user_id':input.user_id},
                                    where = where,
                                    what = "post.post_id as post_id",
                                    limit = "0,1")
            if len(results) > 0:
                return output(200, True)
            else:
                return output(200, False)
        except:
            return output(700, False)

