#!/usr/bin/python
# -*- coding: utf8 -*-

"""
    author:nango

update_time: 2015/7/21--22:05

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


@route.route('/user/food/list')
class FoodList:
    def POST(self):
        input = web.input(access_token = None, user_id = None)
        input = web.input(campus_id = None, food_id = None)

        if input.access_token == None or input.user_id == None:
            return output(110)

        try:
            input.user_id = int(input.user_id)
        except:
            return output(111)



        if input.campus_id == None:
            return output(110)

        try:
            input.campus_id = int(input.campus_id)
            if input.food_id != None:
                input.food_id = int(input.food_id)
        except:
            output(111)

        db = getDb()

        results = db.select('token', vars = {'token':input.access_token, 'id':input.user_id},
                            where = "access_token=$token and user_id=$id")
        if len(results) == 0:
            return output(410)

        campus_id = db.select('user', vars = {'id':input.user_id}, where = "user_id=$id")[0].campus_id

        # 查看campus_id 是否存在
        results = db.select('campus', vars={'campus_id' : input.campus_id},
                            where="campus_id=$campus_id", what="campus_id")

        if len(results) != 1:
            return output(460)

        results = db.select('food', vars={'campus_id': input.campus_id},
                                where="campus_id=$campus_id")

        resul = []
        for i in results:
            resul.append(
                {"id": i.food_id, "name": i.food_name, "price": i.food_price,
                 "desc": i.food_desc, "img_url": i.food_img_url, "is_sold_out": i.is_sold_out,
                 "is_server": i.is_served})
        return output(200, resul)