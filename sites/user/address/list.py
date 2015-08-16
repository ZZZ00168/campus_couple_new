#!/usr/bin/python
# -*- coding: utf8 -*-

"""
    author:nango

update_time: 2015/7/22--12:05

apis:
    /user/address/list
"""

import route
import web
import random
import time
from database import *
from output import *
from encrypt import *


@route.route('/user/address/list')
class UserAddressList:
    def POST(self):
        input = web.input(access_token = None, user_id = None, address_id = None)

        if input.access_token == None or input.user_id == None:
            return output(110)

        try:
            input.user_id = int(input.user_id)
            if input.address_id != None:
                input.address_id = int(input.address_id)
        except:
            return output(111)

        db = getDb()

        # 查询address_token是否存在
        results = db.select('token', vars = {'token': input.access_token, 'id' : input.user_id},
                                 where = 'access_token=$token and user_id=$id')

        if len(results) != 1:
            return output(410)

        if input.address_id == None:
            results = db.select('address', vars = {'id' : input.user_id}, where = "user_id=$id")
        else:
            results = db.select('address', vars = {'aid' : input.address_id, 'id' : input.user_id},
                                where = "address_id=$aid and user_id=$id")

            if len(results) == 0:
                return output(465)

        addressList = []

        for i in results:
            addressList.append({'address_id' : i.address_id, 'phone' : i.phone,
                                'consignee' : i.consignee, 'further_detail' : i.further_detail,
                                'region_id' : i.region_id})

        for i in addressList:
            region_id = i['region_id']
            del i['region_id']

            results = db.select('region', vars = {'id' : region_id}, where = "region_id=$id")[0]
            i['region_name'] = results.region_name

            results = db.select('campus', vars = {'id' : results.campus_id},
                                where = 'campus_id=$id')[0]
            i['campus_name'] = results.campus_name

            results = db.select('school', vars = {'id' : results.school_id},
                                where = 'school_id=$id')[0]
            i['school_name'] = results.school_name

        return output(200, addressList)

