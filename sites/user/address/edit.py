#!/usr/bin/python
# -*- coding: utf8 -*-

import web
import re
import route

from output import *
from database import *


@route.route('/user/address/edit')
class UserAddressEdit:
    def POST(self):
        input = web.input(access_token = None, user_id = None, address_id = None, region_id = None,
                          phone = None, consignee = None, further_detail = None)

        if (input.access_token == None or input.user_id == None or input.address_id == None
            or input.region_id == None or input.phone == None or input.consignee == None):
            return output(110)

        try:
            input.user_id = int(input.user_id)
            input.address_id = int(input.address_id)
            input.region_id = int(input.region_id)
        except:
            return output(111)

        if not re.compile(r'[0-9]{11}').match(input.phone):
            return output(121)

        if input.further_detail == None:
            input.further_detail = ''

        db = getDb()

        if len(db.select('token', vars = {'id' : input.user_id, 'token' : input.access_token},
                         where = "access_token=$token and user_id=$id")) == 0:
            return output(410)

        if len(db.select('address', vars = {'aid' : input.address_id, 'id' : input.user_id},
                         where = "address_id=$aid and user_id=$id")) == 0:
            return output(465)

        if len(db.select('region', vars = {'id' : input.region_id}, where = 'region_id=$id')) == 0:
            return output(464)

        try:
            db.update('address', vars = {'id' : input.address_id}, where = "address_id=$id",
                      region_id = input.region_id, phone = input.phone,
                      consignee = input.consignee, further_detail = input.further_detail)
        except:
            return output(700)

        return output(200)

