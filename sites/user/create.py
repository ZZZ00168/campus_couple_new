#!/usr/bin/python
# -*- coding: utf8 -*-
"""
author: farseer810
update_time: 2015/7/19--13:23
apis:
    /user/register
    /user/verify
"""


import route
import web
import random
import re


from database import *
from output import *
from encrypt import *
from verify import *


@route.route('/user/verify/send')
class SendVerification:
    def POST(self):
        input = web.input(mobile = None)

        #是否缺少必要参数
        if input.mobile == None:
            return output(110)

        #判断mobile的长度与类型是否正确
        if len(input.mobile) != 11 or (not re.compile(r'^[1-9][0-9]+$').match(input.mobile)):
            return output(120)

        db = getDb()
        #查看该手机号是否已存在
        results = db.select('user', vars = {'mobile' : input.mobile}, where = "mobile=$mobile",
                            what = "verified")

        if len(results) == 0:
            t = db.transaction()
            try:
                db.insert('user', mobile = input.mobile, verified = 'no', add_time = None)
                status_code = sendVerifyCode(input.mobile, db)

                if status_code != 200:
                    t.rollback()
                    return output(status_code)

                t.commit()
            except:
                t.rollback()
                return output(700)
        #该手机号已存在
        else:
            user = results[0]

            #该手机号已存在并完成验证
            if user.verified == 'yes':
                return output(420)

            status_code = sendVerifyCode(input.mobile, db)
            if status_code != 200:
                return output(status_code)

        return output(200)


@route.route('/user/register')
class UserRegister:
    def POST(self):
        input = web.input(mobile = None, password = None, verify_code = None)

        if input.mobile == None or input.password == None or input.verify_code == None:
            return output(110)

        try:
            input.verify_code = int(input.verify_code)
        except:
            return output(111)

        length = len(input.password)
        if length < 6:
            return output(130)
        if length > 18:
            return output(131)

        if not re.compile(r'^[0-9A-Za-z]+$').match(input.password):
            return output(132)

        db = getDb()
        results = db.select('user', vars = {'mobile' : input.mobile},
                            where = "mobile=$mobile")
        if len(results) != 1:
            return output(421)

        user = results[0]

        if user.verified == 'yes':
            return output(420)

        myvar = {'id' : user.user_id}
        results = db.select('user_verify', vars = myvar, where = "user_id=$id")
        if len(results) == 0:
            return output(431)

        if results[0].verify_code != input.verify_code:
            return output(431)
        t = db.transaction()
        try:
            db.update('user', vars = myvar, where = "user_id=$id",
                      verified = 'yes', passwd = encrypt(input.password))
            db.delete('user_verify', vars = myvar, where = "user_id=$id")
            t.commit()
        except:
            t.rollback()
            return output(700)

        return output(200)

@route.route('/user/verify/check')
class UserVerifyCheck:
    def POST(self):
        input = web.input(mobile = None, verify_code = None)

        if input.mobile == None or input.verify_code == None:
            return output(110, False)

        try:
            input.verify_code = int(input.verify_code)
        except:
            return output(111, False)

        db = getDb()
        results = db.select('user', vars = {'mobile' : input.mobile}, where = "mobile=$mobile")

        if len(results) != 1:
            return output(421, False)

        user_id = results[0].user_id

        user_verify_code = db.select('user_verify' , vars = {'user_id' : user_id},
                                     where = "user_id=$user_id")


        if len(user_verify_code) != 1:
            return output(431, False)

        user_verify_code = user_verify_code[0]
        user_fail_count = user_verify_code.fail_count

        if user_verify_code.verify_code == input.verify_code:
            return output(200, True)
        else:
            if user_fail_count >= 4:
                try:
                    db.delete('user_verify', vars = {'id' : user_id}, where = "user_id=$id")
                except:
                    return output(700, False)
            else :
                user_fail_count += 1
                db.update('user_verify' , vars = {'user_id' : user_id } , where = "user_id=$user_id",
                          fail_count = user_fail_count)

            return output(431, False)

