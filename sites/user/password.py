#!/usr/bin/python
# -*- coding: utf8 -*-
"""
    author:nango

update_time: 2015/7/21--14:43

apis:
    /user/password/change
    /user/password/forget
    /user/password/verify
"""

import route
import re
from database import *
from output import *
from encrypt import *
from verify import *



@route.route('/user/password/change')
class PasswordChange:
    def POST(self):
        # 访问方式：POST请求参数：mobile、old_password、new_password
        input = web.input(mobile=None, old_password=None, new_password=None)

        if input.mobile == None or input.old_password == None or input.new_password == None:
            return output(110)

        ##判断mobile 是否存在、新密码长度、新密码类型、旧密码是否正确
        # 先解决不用查表

        # 判断密码长度、类型。符合则status_code["status_code"]=200
        status_code = Judge.verifyPasswordIsleague(input.new_password)
        if (status_code["status_code"] != 200):
            return output(status_code["status_code"])

        # 查表获取用户信息
        db = getDb()
        myvar = {'mobile': input.mobile}
        user = db.select('user', vars=myvar,
                         where="mobile=$mobile and verified='yes'",
                         what='user_id,passwd')
        # 用户是否存在
        if len(user) != 1:
            return output(421)
        user = user[0]
        print user.passwd
        print input.old_password,encrypt(input.old_password)
        # 旧密码是否正确
        if user.passwd != encrypt(input.old_password):
            return output(430)

        # 更新用户密码
        try:
            db.update('user', vars={'user_id': user.user_id},
                      where="user_id=$user_id",
                      passwd=encrypt(input.new_password))
            return output(200)
        except:
            return output(700)


@route.route('/user/password/forget')
class PasswordForget:
    # 访问方式：POST    请求参数：mobile
    def POST(self):
        # 返回类型:json 、 json[“data”]: null  、 json[“status”]:状态码
        input = web.input(mobile=None)

        if input.mobile == None:
            return output(110)

        # status_code["satus_code"]=200 表示用户手机号单独唯一存在。
        status_code = Judge.verifyUsernameIsExistAndIsleague(input.mobile)
        if (status_code["status_code"] != 200):
            return output(status_code["status_code"])  # 否则返回错误

        try:
            status_code_message = sendVerifyCode(input.mobile)
            return output(status_code_message)  # 处理正确与否，返回。
        except:
            return output(700)  # 发送短信失败


@route.route('/user/password/verify')
class PasswordVerify:
    def POST(self):  # 请求参数：mobile、verify_code、new_password
        input = web.input(mobile=None, verify_code=None, new_password=None)

        if input.mobile == None or input.verify_code == None or input.new_password == None:
            return output(110)

        try:
            input.verify_code = int(input.verify_code)
        except:
            return output(111)

        # 验证新密码格式
        status_code = Judge.verifyPasswordIsleague(input.new_password)
        if status_code["status_code"] != 200:
            return output(status_code["status_code"])

        # 验证用户名是否存在
        status_code_mobile = Judge.verifyUsernameIsExistAndIsleague(input.mobile)
        if status_code_mobile["status_code"] != 200:
            return output(status_code_mobile["status_code"])

        # 验证验证码
        user_id = status_code_mobile["user_id"]
        # 查表获取用户信息
        db = getDb()
        myvar = {'user_id': user_id}
        user = db.select('user_verify', vars=myvar,
                         where="user_id=$user_id", what = "verify_code")
        if len(user) != 1:
            return output(431)
        user = user[0]

        if input.verify_code != user.verify_code:
            # 删掉验证码
            try:
                db.delete('user_verify', vars=myvar, where="user_id=$user_id")
                return output(431)
            except:
                return output(431)
        # 删掉改验证码
        t = db.transaction()
        try:
            db.delete('user_verify', vars=myvar, where="user_id=$user_id")
            db.update('user', vars=myvar, where="user_id=$user_id",
                      passwd=encrypt(input.new_password))
            t.commit()
            return output(200)
        except:
            t.rollback()
            return output(700)


# 工具类，判断mobile、password是否合法，mobile是否存在
class Judge:
    # 判断mobile类型、长度是否合法
    # 返回类型 {"status_code":integer}
    @staticmethod
    def verifyUsernameIsleague(mobile):

        if len(mobile) != 11 or (not re.compile(r'^[1-9][0-9]+$').match(mobile)):
            return {"status_code": 120}
        else:
            return {"status_code": 200}

    # 判断用户输入的密码 长度、类型是否合法
    # 返回类型 {"status_code":integer}
    @staticmethod
    def verifyPasswordIsleague(input_password):
        if (input_password == None):
            return {"status_code": 130}
        length = len(input_password)
        if length < 6:
            return {"status_code": 130}
        if length > 18:
            return {"status_code": 131}
        if not re.compile(r'^[0-9A-Za-z]+$').match(input_password):
            return {"status_code": 132}
        return {"status_code": 200}

    # 判断mobile是否合法，且是否单独存在数据库中
    # 返回类型 {"status_code":integer}
    @staticmethod
    def verifyUsernameIsExistAndIsleague(mobile):
        # 判断mobile长度、类型。符合则status_code["status_code"]=200
        status_code = Judge.verifyUsernameIsleague(mobile)
        if (status_code["status_code"] != 200):
            return status_code

        # 查表获取用户信息
        db = getDb()
        myvar = {'mobile': mobile}
        user = db.select('user', vars=myvar,
                         where="mobile=$mobile and verified='yes'",
                         what='user_id,passwd')
        # 判断用户手机号码是否存在
        if len(user) != 1:
            return {"status_code": 421}
        user = user[0]

        # 验证时候使用到user_id来查表
        result1 = {"status_code": 200, "user_id": user.user_id}
        return result1
