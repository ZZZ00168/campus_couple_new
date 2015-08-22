#!/usr/bin/python
# -*- coding: utf8 -*-


"""
    author:nango

test_time: 2015/7/29 10:35    OK
update_time: 2015/7/21 22:05
apis:
    /campus/login
    /campus/logout
"""

import route
import web
import random
import time
from database import *
from output import *
from encrypt import *

@route.route('/campus/login')
class CampusLogin:
    def POST(self):  # ，传入loginname，password，返回登陆正确的随机单一token值
        input = web.input(login_name=None, password=None)

        # 是否缺少必要参数
        if input.login_name == None or input.password == None:
            return output(110)

        # TODO:
        # 用户名是否合法
        # 密码是否合法
        if len(input.login_name) > 20 or len(input.password) > 33:
            return output(112)

        # 用户名是否唯一存在
        db = getDb()
        results = db.select('campus', vars={'login_name': input.login_name},
                            where="login_name=$login_name",
                            what="campus_id,passwd")
        if len(results) != 1:
            return output(460)

        # 密码是否正确
        results = results[0]
        if results.passwd != encrypt(input.password):
            return output(430)

        # 记下campus_id
        campus_id = results.campus_id

        # 密码正确，增权限access_token
        token = db.select('campus_token', vars={'id': campus_id},
                          where="campus_id=$id")

        if len(token) > 0:  # 如果存在token，那就更新token的时间
            token = token[0]
            try:
                db.update('campus_token', vars={'id': token.campus_id},
                          where="campus_id=$id", activate_time=None)
                return output(200, {'access_token':token.access_token})
            except:
                return output(700)

        else:
            try:
                while True:  # 防止不同用户的token相同
                    token = encrypt(str(random.randint(100000, 1000000)) +
                                    str(time.time()) + input.login_name)
                    results = db.select('campus_token', vars={'token': token},
                                        where="access_token=$token")
                    if len(results) == 0:
                        break

                db.insert('campus_token', access_token=token, campus_id=campus_id,
                          activate_time=None)
                return output(200, {"access_token": token, 'campus_id':campus_id})
            except:
                return output(700)


@route.route('/campus/logout')
class CampusLogout:
    def POST(self):  # 传入access_token如果正确，那就删掉该token，如果错误，则返回权限不足
        input = web.input(access_token=None)
        # 参数不足
        if input.access_token == None:
            return output(110)
        db = getDb()
        results = db.select('campus_token', vars={'token': input.access_token},
                            where='access_token=$token')
        if len(results) > 0:
            try:
                db.delete('campus_token', vars={'token': input.access_token},
                          where="access_token=$token")
                return output(200)
            except:
                return output(700)
        else:
            return output(410)
