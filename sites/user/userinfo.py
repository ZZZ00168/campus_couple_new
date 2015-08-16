#!/usr/bin/python
# -*- coding: utf8 -*-
"""
author:zzz
update_time: 2015/7/19--13:23
apis:
    /userinfo/get
    /userinfo/set
"""

import route
import web
import re

from database import *
from output import *
from mytoken import *


@route.route('/userinfo/get')
class GetUserInfo:
    # 这里的schoolname还没有实现。因为可能shool_id 有改动#
    def POST(self):
        input = web.input(access_token=None, user_id=None)

        if input.access_token == None or input.user_id == None:
            return output(110)

        try:
            input.user_id = int(input.user_id)
        except:
            return output(111)

        db = getDb()

        result = db.select('token', vars={'token': input.access_token, 'user_id': input.user_id},
                           where="access_token=$token and user_id=$user_id ")

        if len(result) != 1:
            return output(410)
        user_id = input.user_id

        info = {}
        user = db.select('user', vars={'id': user_id}, where="user_id=$id")[0]

        info['mobile'] = user.mobile
        info['sex'] = user.sex
        if user.default_address_id == None:
            info['default_address_id'] = 0
        else:
            info['default_address_id'] = user.default_address_id
        if user.campus_id != None:
            results = db.select('campus', vars={'id': user.campus_id},
                                where="campus_id=$id")[0]
            info['campus_name'] = results.campus_name
            info['school_name'] = db.select('school', vars={'id': results.school_id},
                                            where="school_id=$id",
                                            what='school_name')[0].school_name
        else:
            info['campus_name'] = None
            info['school_name'] = None

        info['img_url'] = None
        info['birthday'] = None
        info['nickname'] = None
        info['description'] = None
        info['location'] = None
        info['province_id'] = None
        info['province_name'] = None
        info['profession'] = None

        userinfo = db.select('userinfo', vars={'user_id': user_id}, where="user_id=$user_id")

        for i in userinfo:
            if i.type == 'province_id':
                info['province_id'] = int(i.information)
            else:
                info[i.type] = i.information

        if info['province_id'] != None:
            info['province_name'] = db.select('province', vars={'id': info['province_id']},
                                              where="province_id=$id")[0].province_name

        del info['province_id']

        return output(200, info)


@route.route('/userinfo/set')
class SetUserInfo:
    def POST(self):

        input = web.input(access_token=None, nickname=None, user_id=None, birthday=None,
                          description=None, province_id=None, location=None,
                          sex=None, profession=None)

        if input.access_token == None or input.user_id == None:
            return output(110)

        try:
            input.user_id = int(input.user_id)
            if input.province_id != None:
                input.province_id = int(input.province_id)
        except:
            return output(111)

        if input.sex != None:
            if input.sex != 'm' and input.sex != 'f':
                return output(112)

        if (input.birthday != None and
                (not re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}').match(input.birthday))):
            return output(113)

	if input.nickname != None:
		if 1>=len(input.nickname) or len(input.nickname)>=8:
			return output(114)

        db = getDb()

        if len(db.select('token', vars={'token': input.access_token, 'id': input.user_id},
                         where="access_token=$token and user_id=$id")) == 0:
            return output(410)

        try:
            if input.province_id != None:
                if len(db.select('province', vars = {'id' : input.province_id},
                                 where = "province_id=$id")) == 0:
                    return output(461)
                vars = {'id': input.user_id, 'type': 'province_id'}
                where = 'user_id=$id and type=$type'
                if len(db.select('userinfo', vars=vars, where=where)) != 0:
                    db.update('userinfo', vars = vars, where = where,
                              information = str(input.province_id))
                else:
                    db.insert('userinfo', user_id = input.user_id, type = 'province_id',
                              information = str(input.province_id))

            if input.nickname != None:
                vars = {'id': input.user_id, 'type': 'nickname'}
                where = 'user_id=$id and type=$type'
                if len(db.select('userinfo', vars=vars, where = where)) != 0:
                    db.update('userinfo', vars = vars, where = where, information = input.nickname)
                else:
                    db.insert('userinfo', user_id = input.user_id, type = 'nickname',
                              information = input.nickname)

            if input.birthday != None:
                vars = {'id': input.user_id, 'type': 'birthday'}
                where = 'user_id=$id and type=$type'
                if len(db.select('userinfo', vars=vars, where=where)) != 0:
                    db.update('userinfo', vars = vars, where = where, information = input.birthday)
                else:
                    db.insert('userinfo', user_id = input.user_id, type = 'birthday',
                              information = input.birthday)

            if input.description != None:
                vars = {'id': input.user_id, 'type': 'description'}
                where = 'user_id=$id and type=$type'
                if len(db.select('userinfo', vars=vars, where=where)) != 0:
                    db.update('userinfo', vars = vars, where = where, information = input.description)
                else:
                    db.insert('userinfo', user_id = input.user_id, type = 'description',
                              information = input.description)

            if input.location != None:
                vars = {'id': input.user_id, 'type': 'location'}
                where = 'user_id=$id and type=$type'
                if len(db.select('userinfo', vars=vars, where=where)) != 0:
                    db.update('userinfo', vars = vars, where = where, information = input.location)
                else:
                    db.insert('userinfo', user_id = input.user_id, type = 'location',
                              information = input.location)

            if input.sex != None:
                db.update('user', vars = {'id' : input.user_id}, where = "user_id=$id",
                          sex = input.sex)

            if input.profession != None:
                vars = {'id': input.user_id, 'type': 'profession'}
                where = 'user_id=$id and type=$type'
                if len(db.select('userinfo', vars=vars, where=where)) != 0:
                    db.update('userinfo', vars = vars, where = where, information = input.profession)
                else:
                    db.insert('userinfo', user_id = input.user_id, type = 'profession',
                              information = input.profession)

        except:
            return output(700)

        return output(200)
