#!/usr/bin/python
# -*- coding: utf8 -*-
#Author:zzz

import web
import route

from output import *
from database import *

@route.route('/user/order/submit')
class UserOrderSubmit:
    def POST(self):
        input = web.input(access_token = None, user_id = None, food_list = None , address_id = None)
        if (input.access_token == None or input.user_id == None or input.food_list == None or
            input.address_id == None):
            return output(110)

        try:
            input.user_id = int(input.user_id)
            input.address_id = int(input.address_id)
        except:
            return output(111)

        db = getDb()
        user_id = db.select('token' , vars={'access_token':input.access_token ,
                                            'user_id' : input.user_id} ,
                         where = "access_token=$access_token and user_id=$user_id")

        if len(user_id) == 0:
            return output(420)

        user_id = user_id[0].user_id

        campus_id = db.select('user' , vars = {'user_id':user_id} , where = "user_id=$user_id")[0].campus_id

        t = db.transaction()
        try:
            new_order_id = db.insert('orders' , address_id = input.address_id ,campus_id = campus_id , status ="submitted"  , user_id = user_id )
            food_list = json.loads(input.food_list)
            for i in food_list:
                db.insert('ordered_food', order_id = new_order_id, food_id = i['food_id'] , number = i['food_num'])
        except:
            t.rollback()
            return output(700)

        else :
            t.commit()
            return output(200)
