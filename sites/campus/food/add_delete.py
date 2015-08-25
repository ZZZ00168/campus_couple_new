#!/usr/bin/python
# -*- coding: utf8 -*-

#author:zzz

import route
import web
import base64
import consts
import os
import os.path
import Image
import StringIO

from database import *
from output import *


def getCropBox(w, h):
    if w > h:
        lpoint = ((w - h) / 2, 0)
    else:
        lpoint = (0, (h - w) / 2)
    min_dist = min(w, h)
    return (lpoint[0], lpoint[1], lpoint[0] + min_dist, lpoint[1] + min_dist)

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
            if not (input.food_price > 0 and input.food_price <= 500):
                return output(111)
        except:
            return output(111)

        results = db.select('campus_token' , vars={'access_token':input.access_token},
                              where = "access_token=$access_token")

        if len(results) == 0:
            return output(410)

        campus_id = results[0].campus_id

        filename = ""
        t = db.transaction()
        try:
            food_id = db.insert('food' , campus_id = campus_id, food_name = input.food_name,
                      food_price = input.food_price, food_desc = input.food_desc,
                      is_sold_out = 'no', is_served = 'no')

            # filename = input.img_file.filename.replace('\\', '/')
            # filename = filename.split('/')[-1]
            # i = filename.rfind('.')
            # if i == -1:
            #     t.rollback()
            #     return output(440)
            # suffix = filename[i:]
            suffix = '.jpg'
            filename = "logo image of food_id %d" % (food_id)
            filename = base64.b64encode(filename) + suffix


            #open the file and write data into it
            im = Image.open(StringIO.StringIO(input.img_file.file.read()))
            width, height = im.size
            im = im.crop(getCropBox(width, height))
            im.thumbnail((200, 200))
            im.save('/var/campus_couple_img/static/' + filename, 'jpeg')

            food_img_url = consts.domain_name + '/static/' + filename
            db.update('food', vars = {'id' : food_id},
                      where = "food_id=$id", food_img_url = food_img_url)
            t.commit()
            return output(200)

        except:
            try:
                if os.path.exists(filename) == True:
                    os.remove(filename)
            except:
                pass
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
        input = web.input(access_token = None, food_id = None)

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
            db.delete('food' ,vars={'fid':input.food_id} , where = "food_id=$fid")
            return output(200)
        except:
            return output(700)


