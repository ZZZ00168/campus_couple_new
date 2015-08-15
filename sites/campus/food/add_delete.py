#!/usr/bin/python
# -*- coding: utf8 -*-

#author:zzz

import route
import web
import base64
import consts

from database import *
from output import *

@route.route('/campus/food/add')
class FoodAdd:
    def POST(self):
        db = getDb()
        input = web.input(access_token = None, food_name = None, food_price = None,
                          food_desc = None, img_file = {})

        if (input.access_token == None or input.food_name == None or input.food_price == None
            or input.food_desc == None or input.img_file == {}):
            return output(110)

        try:
            input.food_price = float(input.food_price)
        except:
            return output(111)

        results = db.select('campus_token' , vars={'access_token':input.access_token},
                              where = "access_token=$access_token")

        if len(results) == 0:
            return output(410)

        campus_id = results[0].campus_id

        t = db.transaction()
        try:
            food_id = db.insert('food' , campus_id = campus_id, food_name = input.food_name,
                      food_price = input.food_price, food_desc = input.food_desc,
                      is_sold_out = 'no', is_served = 'no')

            filename = input.img_file.filename.replace('\\', '/')
            filename = filename.split('/')[-1]
            i = filename.rfind('.')
            if i == -1:
                t.rollback()
                return output(440)
            suffix = filename[i:]
            filename = "logo image of food_id %d" % (food_id)
            filename = base64.b64encode(filename) + suffix

            #open the file and write data into it
            fout = open('/var/campus_couple_img/static/' + filename, 'w')
            fout.write(input.img_file.file.read())
            fout.close()

            food_img_url = consts + '/static/' + filename
            db.update('food', vars = {'id' : food_id},
                      where = "food_id=$id", food_img_url = food_img_url)
            t.commit()
            return output(200)


        except:
            t.rollback()
            return output(440)

    def GET(self):
        html_text = """<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
</head>
<body>
    <form action="/campus/food/add" method="post" enctype="multipart/form-data">
        令牌: <input name="access_token" type="text"/><br/>
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


@route.route('/campus/food/delete')
class FoodDelete:
    def POST(self):

        input = web.input(access_token = None,food_id = None)

        if input.access_token == None or input.food_id == None:
            return  output(110)

        try:
            input.food_id=int(input.food_id)
        except:
            return output(111)

        db = getDb()

        results = db.select('campus_token' , vars={'access_token':input.access_token},
                              where = "access_token=$access_token")

        if len(results) == 0:
            return output(410)

        campus_id = results[0].campus_id

        if len(db.select('food', vars = {'fid' : input.food_id, 'cid' : campus_id},
                         where = "food_id=$fid and campus_id=$cid")) == 0:
            return output(463)

        try:
            db.delete('food' ,vars={'fid':input.food_id} , where = "food_id=$fid")
            return output(200)
        except:
            return output(700)


