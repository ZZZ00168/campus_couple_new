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
class UserFollowList: #获取我关注用户列表
    def POST(self):
        input = web.input(access_token = None, user_id = None)
        db = getDb()

        if input.access_token == None or input.user_id == None:
            return output(110)

        try :
            input.user_id = int(input.user_id)
        except:
            return output(111)

        #用户权限
        results = db.select('token' , vars = {'access_token':input.access_token , 'user_id':input.user_id} ,
                            where = "user_id=$user_id and access_token=$access_token")
        if len(results) == 0:
            return output(410)

        #获取全部的关注人
        results = db.select('follow' , vars={'user_id':input.user_id} , where = "user_id=$user_id")
        if len(results) == 0:
            return output(200 ,[])# todo 没有关注列表

        list = []
        for i in results:
            followed_id = i.followed_id
            userinfo = db.select('userinfo' ,vars ={'user_id':followed_id} , where = "user_id=$user_id" )
            #在userinfo里面找不到对应的followed_id
            if len(userinfo) == 0:
                continue

            #对user_img_url做处理
            results = db.select('userinfo' ,vars = {'user_id':followed_id,'type':"img_url"} ,
                                where = "user_id=$user_id and type=$type" )

            if len(results) == 0:
                user_img_url = ""
            else :
                user_img_url = results[0].information

            #对user_name做处理
            results = db.select('userinfo' ,vars = {'user_id':followed_id} ,
                                where = "user_id=$user_id and type='nickname'" )
            if len(results) == 0:
                user_nickname = ""
            else :
                user_nickname = results[0].information

            #对description做处理
            results = db.select('userinfo' ,vars = {'user_id':followed_id} ,
                                where = "user_id=$user_id and type='description'" )
            if len(results) == 0:
                description = ""
            else :
                description = results[0].information

            #对sex做处理
            results = db.select('userinfo' ,vars = {'user_id':followed_id} ,
                                where = "user_id=$user_id and type='sex'" )
            if len(results) == 0:
                sex = ""
            else :
                sex = results[0].information

            list.append({"user_id":followed_id ,"user_name":user_nickname,"sex":sex ,
                         "user_img_url": user_img_url ,"description":description})
        #for 结束
        return output(200 , list)
