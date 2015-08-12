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

        if comment[0].user_id != input.user_id:
            return output(410)

        #顺便得出这条评论评论的 说说
        post_id = comment[0].post_id

        # 判断是 说说的主人 ， 还是评论的主人
        identity = ""

        result = db.select('post' , vars={'post_id':post_id} , where = "post_id=$post_id")
        if len(result) == 0:
            return output(11111)#todo 说说 不存在

        result = db.select('comments' , vars={'comment_id':input.comment_id} , where = "comment_id=$comment_id")
        if len(result) == 0:
            return output(11111)#todo 评论 不存在

        # 现在的result 是 评论 查询结果
        if result[0].commenter_id == input.user_id:
            identity = "comment_author"
        else:
            result = db.select('post' , vars = {'post_id':post_id} , where = "post_id=$post_id")
            if result[0].user_id == input.user_id:
                identity = "post_author"

        if identity == "":
            return output(420)#todo 用户权限不足无法删除
        else:
            db.delete("comments" , vars={'comment_id':input.comment_id} , where = "comment_id=$comment_id")
        return output(200)
