#!/usr/bin/python
# -*- coding: utf8 -*-
"""
author:
update_time: 2015
apis:
    /user/post/add
"""

import route
import web
import Image
import StringIO
import base64
import consts


from output import *
from database import *

def getCropBox(w, h):
    if w > h:
        lpoint = ((w - h) / 2, 0)
    else:
        lpoint = (0, (h - w) / 2)
    min_dist = min(w, h)
    return (lpoint[0], lpoint[1], lpoint[0] + min_dist, lpoint[1] + min_dist)

@route.route('/user/post/add')
class UserPostAdd:
    def POST(self):  # 传入 access_token,user_id,post_id,content
        input = web.input(access_token = None, user_id = None, content = None, img_file = {})

        if input.access_token == None or input.user_id == None or input.content==None:
            return output(110)
        #验证用户的token 和 user_id 是否对应
                #强制转化类型
        try :
            input.user_id = int(input.user_id)
        except:
            return output(111)

        db = getDb()

        #再判断token 和 user_id 是否对应
        result = db.select('token' , vars={'access_token':input.access_token , 'user_id':input.user_id} ,
                           where = "user_id=$user_id and access_token=$access_token")
        if len(result) == 0:
            return output(410)

        img_url = None
        thumbnail_img_url = None

        t = db.transaction()
        try:
            post_id = db.insert('post' , user_id = input.user_id , content = input.content,
                                add_time = None)
            if input.img_file != {}:
                suffix = '.jpg'
                original_filename = "original image of post_id %d" % (post_id,)
                original_filename = base64.b64encode(original_filename) + suffix
                thumbnail_filename = "thumbnail image of post_id %d" % (post_id,)
                thumbnail_filename = base64.b64encode(thumbnail_filename) + suffix

                original_image = Image.open(StringIO.StringIO(input.img_file.file.read()))
                width, height = original_image.size
                thumbnail_image = original_image.crop(getCropBox(width, height))
                thumbnail_image.thumbnail((200, 200))
                thumbnail_image.save('/var/campus_couple_img/static/' + thumbnail_filename, 'jpeg')
                original_image.save('/var/campus_couple_img/static/' + original_filename, 'jpeg')

                img_url = consts.domain_name + '/static/' + original_filename
                thumbnail_img_url = consts.domain_name + '/static/' + thumbnail_filename

            if img_url != None and thumbnail_img_url != None:
                db.update('post', vars = {'id':post_id}, where = "post_id=$id",
                          img_url = img_url, thumbnail_img_url = thumbnail_img_url)
        except:
            return output(700)
        return output(200)

