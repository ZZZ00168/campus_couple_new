#!/usr/bin/python
# -*- coding: utf8 -*-

import route
import web
from database import *
from output import *


# update food message
@route.route('/campus/food/setinfo')
class FoodSetInfo:
    def POST(self):
        input = web.input(access_token = None, food_id = None, food_name = None,
                          food_desc = None, food_price = None, img_file = {})

        if (input.access_token == None or input.food_id == None or input.food_name == None
            or input.food_desc == None or input.food_price == None or input.img_file == {}):
            return output(110)

        try:
            input.food_id = int(input.food_id)
            input.food_price = float(input.food_price)
        except:
            return output(111)

        db = getDb()

        results = db.select('campus_token', vars = {'token' : input.access_token},
                            where = "access_token=$token")

        if len(results) == 0:
            return output(410)

        campus_id = results[0].campus_id

        if len(db.select('food', vars = {'fid' : input.food_id, 'cid' : campus_id},
                         where = "food_id=$fid and campus_id=$cid")) == 0:
            return output(463)

        try:
            db.update('food', vars = {'id' : input.food_id}, where = "food_id=$id",
                      food_name = input.food_name, food_desc = input.food_desc,
                      food_price = input.food_price)
        except:
            return output(700)
        return output(200)


@route.route('/campus/food/setstatus')
class FoodSetStatus:
    def POST(self):
        input = web.input(access_token = None, food_id = None, is_sold_out = None, is_served = None)

        if (input.access_token == None or input.food_id == None or input.is_sold_out == None
            or input.is_served == None):
            return output(110)

        try:
            input.food_id = int(input.food_id)
        except:
            return output(111)

        if input.is_sold_out != 'yes' and input.is_sold_out != 'no':
            return output(112)

        if input.is_served != 'yes' and input.is_served != 'no':
            return output(112)

        db = getDb()

        myvar = {'access_token': input.access_token}
        if_have_campus = db.select('campus_token', vars=myvar,
                                   where='access_token=$access_token', what='campus_id')
        if len(if_have_campus) == 0:
            return output(410)

        campus_id = if_have_campus[0].campus_id

        if len(db.select('food', vars = {'fid' : input.food_id, 'cid' : campus_id},
                         where = "food_id=$fid and campus_id=$cid")) == 0:
            return output(463)

        try:
            db.update('food', vars={'food_id': input.food_id},
                      where="food_id=$food_id",
                      is_sold_out = input.is_sold_out, is_served = input.is_served)
            return output(200)
        except:
            return output(700)
