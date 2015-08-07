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
        db = getDb()
        input = web.input(access_token = None ,user_id = None , post_id = None , commenter_id = None , comment = None)
        try:
            input.post_id = int(input.post_id)
            input.commenter_id = int(input.commenter_id)
        except:
            return output(117)#todo 参数错误

        #x先看是不空值
        if input.access_token == None or input.commenter_id == None or input.post_id == None or input.comment == None:
            return output(110)# todo 缺少必填参数

        #再判断token 和 commenter_id 是否对应
        result = db.select('token' , vars={'access_token':input.access_token , 'user_id':input.commenter_id} ,
                           where = "user_id=$user_id and access_token=$access_token")
        if len(result) == 0:
            return output(420)# todo 权限不足

        #判断是否存在该条post
        post = db.select('post' , vars={'post_id':input.post_id} , where = "post_id=$post_id")
        if len(post) == 0:
            return output(1111111111)# todo 不存在被评论的post

        # 插入
        db.insert('comments' , post_id= input.post_id , user_id=input.user_id , comment_id=input.commenter_id ,content = input.comment )
        return output(200)

