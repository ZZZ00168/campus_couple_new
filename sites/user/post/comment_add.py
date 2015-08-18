#!/usr/bin/python
# -*- coding: utf8 -*-
"""
author:
update_time: 2015
apis:
    /user/post/comment/add
"""

import route
import web
from output import *
from database import *

from output import *
from database import *

@route.route('/user/post/comment/add')
class UserPostCommentAdd:
    def POST(self):  # 传入 access_token,user_id,post_id,commenter_id,comment

        input = web.input(access_token = None, user_id = None, post_id = None,
                          comment_id = None, content = None)

        if(input.access_token == None or input.user_id == None or
                   input.post_id == None or input.content == None):
            return output(110)

        try:
            input.user_id = int(input.user_id)
            input.post_id = int(input.post_id)
            if input.comment_id == None:
                input.comment_id = 0
            input.comment_id = int(input.comment_id)
        except:
            return output(111)

        db = getDb()

        #再判断token 和 commenter_id 是否对应
        result = db.select('token' , vars={'access_token':input.access_token,
                                           'user_id':input.user_id},
                           where = "user_id=$user_id and access_token=$access_token")
        if len(result) == 0:
            return output(410)

        #判断是否存在该条post
        post = db.select('post' , vars={'post_id':input.post_id}, where = "post_id=$post_id")
        if len(post) == 0:
            return output(467)

        commented_id = 0

        if input.comment_id != 0:
            results = db.select('comments', vars = {'id':input.comment_id, 'post_id':input.post_id},
                                where = "comment_id=$id and post_id=$post_id")
            if len(results) == 0:
                return output(469)

            commented_id = results[0].user_id

        try:
            db.insert('comments', post_id = input.post_id, user_id = input.user_id,
                      commented_id = commented_id, content = input.content, add_time = None)
            return output(200)
        except:
            return output(700)
