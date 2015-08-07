#!/usr/bin/python
# -*- coding: utf8 -*-

import route
import web

from output import *
from database import *

@route.route('/user/default/address/set')
class SetDefaultAddress:
    def POST(self):
        input = web.input(access_token = None, user_id = None, address_id = None)

        if input.access_token == None or input.user_id == None or input.address_id == None:
            return output(110)

        try:
            input.user_id = int(input.user_id)
            input.address_id = int(input.address_id)
        except:
            return output(111)

        db = getDb()
        if len(db.select('token', vars = {'token' : input.access_token, 'id' : input.user_id},
                         where = "access_token=$token and user_id=$id")) == 0:
            return output(410)

        if len(db.select('address', vars = {'id' : input.user_id, 'aid' : input.address_id},
                         where = "user_id=$id and address_id=$aid")) == 0:
            return output(465)

        try:
            db.update('user', vars = {'id' : input.user_id}, where = "user_id=$id",
                      default_address_id = input.address_id)
        except:
            return output(700)

        return output(200)
