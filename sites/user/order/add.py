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
        input = web.input(access_token = '' , user_id = '' , food_list = None , address_id = '')

        try:
            input.user_id = int(input.user_id)
        except:
            #TODO:user_id is not an integer
            return output(700)

        db = getDb()
        user_id = db.select('token' , vars={'access_token':input.access_token , 'user_id' : input.user_id} ,
                         where = "access_token=$access_token and user_id=$user_id")

        if len(user_id) == 0:
            return output(420) #todo 权限不足

        user_id = user_id[0].user_id

        campus_id =db.select('user' , vars = {'user_id':user_id} , where = "user_id=$user_id")[0].campus_id

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

