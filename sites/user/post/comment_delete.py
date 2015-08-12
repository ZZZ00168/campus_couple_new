#!/usr/bin/python
# -*- coding: utf8 -*-
"""
author: zzz
update_time: 2015/7/25 16:53
apis:
    /user/post/comment/delete
"""

import route
import web

from output import *
from database import *

@route.route('/user/post/comment/delete')
class UserPostCommentDelete:
    def POST(self):  # 传入 access_token,user_id,comment_id
        input = web.input(access_token = None , user_id = None ,comment_id = None)

        if input.access_token == None or input.user_id == None or input.comment_id == None:
            return output(110)

        try:
            input.user_id = int(input.user_id)
            input.comment_id = int(input.comment_id)
        except:
            return output(111)

        db = getDb()

        result = db.select('token' , vars = {'access_token':input.access_token ,
                                           'user_id':input.user_id} ,
                           where = "user_id=$user_id and access_token=$access_token")
        if len(result) == 0:
            return output(410)

        #判断是否存在这条评论
        comment = db.select('comments', vars={'comment_id':input.comment_id},
                            where = "comment_id=$comment_id")
        if len(comment) == 0:
            return output(469)

        comment = comment[0]
        user_id = comment.user_id
        post_id = comment.post_id

        result = db.select('post', vars = {'id':post_id}, where = "post_id=$id", what = "user_id")

        if input.user_id == user_id or input.user_id == result[0].user_id:
            try:
                db.delete('comments', vars = {'id':input.comment_id}, what = "comment_id=$id")
                return output(200)
            except:
                return output(700)
        else:
            return output(410)
