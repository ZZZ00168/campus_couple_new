#!/usr/bin/python
# -*- coding: utf8 -*-

import route
import web
import os
import os.path
import base64
import consts

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
            if not (input.food_price > 0 and input.food_price <= 500):
                return output(111)
        except:
            return output(111)

        db = getDb()

        results = db.select('campus_token', vars = {'token' : input.access_token},
                            where = "access_token=$token")

        if len(results) == 0:
            return output(410)

        campus_id = results[0].campus_id

        results = db.select('food', vars = {'fid' : input.food_id, 'cid' : campus_id},
                         where = "food_id=$fid and campus_id=$cid")
        if len(results) == 0:
            return output(463)

        filename = results[0].food_img_url
        if filename == None:
            filename = ''
        else:
            filename = '/var/campus_couple_img/static/' + filename[filename.rfind('/') + 1:]

        try:
            if os.path.exists(filename) == True:
                os.remove(filename)

            filename = input.img_file.filename.replace('\\', '/')
            filename = filename.split('/')[-1]
            i = filename.rfind('.')
            if i == -1:
                return output(440)
            suffix = filename[i:]
            filename = "logo image of food_id %d" % (input.food_id)
            filename = base64.b64encode(filename) + suffix

            #open the file and write data into it
            fout = open('/var/campus_couple_img/static/' + filename, 'w')
            fout.write(input.img_file.file.read())
            fout.close()

            food_img_url = consts.domain_name + '/static/' + filename

            db.update('food', vars = {'id' : input.food_id}, where = "food_id=$id",
                      food_name = input.food_name, food_desc = input.food_desc,
                      food_price = input.food_price, food_img_url = food_img_url)
        except:
            if os.path.exists(filename) == True:
                os.remove(filename)
            return output(700)

        return output(200)

    def GET(self):
        html_text = """<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
</head>
<body>
    <form action="/campus/food/add" method="post" enctype="multipart/form-data">
        令牌: <input name="access_token" type="text"/><br/>
        ID: <input name="food_id" type="text"/><br/>
        名称: <input name="food_name" type="text"/><br/>
        价格: <input name="food_price" type="text"/><br/>
        描述: <input name="food_desc" type="text"/><br/>
        图片: <input name="img_file" type="file"/><br/>
        <input type="submit" value="提交"/>
    </form>
</body>
</html>
"""
        return html_text


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
