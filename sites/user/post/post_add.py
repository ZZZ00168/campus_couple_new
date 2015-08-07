#!/usr/bin/python
# -*- coding: utf8 -*-
"""
author:
update_time: 2015
apis:
    /user/post/add
"""

import route
import web


from output import *
from database import *

@route.route('/user/post/add')
class UserPostAdd:
    def POST(self):  # 传入 access_token,user_id,post_id,content
        input = web.input(access_token = None , user_id = None , content = None )
        db = getDb()

        if input.access_token == None or input.user_id == None or input.content==None:
            return output(110)

        #验证用户的token 和 user_id 是否对应
                #强制转化类型
        try :
            input.user_id = int(input.user_id)
        except:
            return output(111)#todo 类型错误

        #再判断token 和 user_id 是否对应
        result = db.select('token' , vars={'access_token':input.access_token , 'user_id':input.user_id} ,
                           where = "user_id=$user_id and access_token=$access_token")
        if len(result) == 0:
            return output(410)# todo 权限不足
	post_id = db.insert('post' , user_id = input.user_id , content = input.content)
        return output(200,post_id)

