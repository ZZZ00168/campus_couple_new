#!/usr/bin/python
# -*- coding: utf8 -*-
#Author :zzz


import route
import web
import re

from output import *
from database import *


@route.route('/user/address/add')
class UserAddressAdd:
    def POST(self):
        input = web.input(access_token = None, user_id = None, region_id = None, phone = None,
                          consignee = None, further_detail = None)

        if (input.access_token == None or input.user_id == None or input.region_id == None
            or input.phone == None or input.consignee == None):
            return output(110)

        try:
            input.user_id = int(input.user_id)
            input.region_id = int(input.region_id)
        except:
            return output(111)

        if not re.compile(r'[0-9]{11}').match(input.phone):
            return output(121)

        db = getDb()

        result = db.select('token', vars = {'token' : input.access_token , 'user_id' : input.user_id},
                           where = "access_token=$token and user_id=$user_id")

        if len(result) == 0:
            return output(410)

        if len(db.select('region', vars = {'id' : input.region_id}, where = "region_id=$id")) == 0:
            return output(464)

        default_address_id = db.select('user', vars = {'id':input.user_id}, where = "user_id=$id",
                                       what = "default_address_id")[0].default_address_id
        if default_address_id == None:
            default_address_id = 0

        t = db.transaction()
        try:
            further_detail = ''
            if input.further_detail != None:
                further_detail = input.further_detail
            address_id = db.insert('address', user_id = input.user_id, region_id = input.region_id,
                      phone = input.phone, consignee = input.consignee,
                      further_detail = further_detail)

            if default_address_id == 0:
                db.update('user', vars = {'id':input.user_id}, where = "user_id=$id",
                          default_address_id = address_id)
            t.commit()
        except:
            t.rollback()
            return output(700)

        return output(200)


@route.route('/user/address/delete')
class UserAddressDelete:
    def POST(self):
        input  = web.input(access_token = None, user_id = None, address_id = None)

        if input.access_token == None or input.user_id == None or input.address_id == None:
            return output(110)

        try:
            input.user_id = int(input.user_id)
            input.address_id = int(input.address_id)
        except:
            return output(111)

        db = getDb()
        result = db.select('token' , vars = {'token':input.access_token , 'user_id':input.user_id} ,
                           where = "access_token=$token and user_id=$user_id ")

        if len(result)!=1:
            return output(410)

        results = db.select('address', vars = {'aid' : input.address_id, 'id' : input.user_id},
                            where = "address_id=$aid and user_id=$id")

        if len(results) == 0:
            return output(465)

        default_address_id = db.select('user', vars = {'id':input.user_id}, where = "user_id=$id",
                                       what = "default_address_id")[0].default_address_id
        if default_address_id == None:
            default_address_id = 0

        t = db.transaction()
        try:
            db.delete('address', vars = {'id' : input.address_id}, where = "address_id=$id")
            address_list = db.select('address', vars = {'id' : input.user_id}, where = "user_id=$id")
            if len(address_list) == 0:
                new_default_address_id = 0
            else:
                new_default_address_id = address_list[0].address_id

            db.update('user', vars = {'id' : input.user_id}, where = "user_id=$id",
                      default_address_id = new_default_address_id)
            t.commit()
        except:
            t.rollback()
            return output(700)

        return output(200)

