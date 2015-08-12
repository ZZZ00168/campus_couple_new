#!/usr/bin/python
# -*- coding: utf8 -*-
"""
author: nango
update_time: 2015/7/30--13:23

apis:
    /user/post/campus/list
"""

import route
import re
import web
from database import *
from output import *
from encrypt import *
from verify import *


@route.route('/user/post/campus/list')
class UserPostCampusList:  # 查询校区文章更新情况
    def POST(self):  # 传入access_token,user_id,start_poost_id,start_index,end_index
        input = web.input(access_token=None, user_id=None, start_post_id=None, start_index=None, post_count=None)

        # 缺少必填参数
        if (input.access_token == None or input.user_id == None or input.start_post_id == None or
                    input.start_index == None or input.post_count == None):
            return output(110)
        try:
            input.user_id = int(input.user_id)
            input.start_post_id = int(input.start_post_id)
            input.start_index = int(input.start_index)
            input.post_count = int(input.post_count)
            if input.start_index < 0 or input.post_count <= 0 or input.start_post_id < 0:  # 参数值非法
                return output(112)
        except:
            return output(111)

        if True:
            db = getDb()
            results = db.select('token', vars={'user_id': input.user_id, 'access_token': input.access_token},
                                where="user_id=$user_id and access_token=$access_token")
            # access_token权限不足
            if len(results) != 1:
                return output(410)

            campus_id = db.select('user', vars = {'id' : input.user_id}, where = "user_id=$id",
                                what = 'campus_id')[0].campus_id

            try:
                campus_id = int(campus_id)
                if campus_id <= 0:
                    return output(460)
            except:
                return output(460)

            # 查询是否存在start_post_id
            if input.start_post_id != 0:
                post_ids = db.select('post', vars={'post_id': input.start_post_id},
                                 where='post_id=$post_id', what='post_id')
                if len(post_ids) != 1:
                    return output(467)

            # start_post_id不存在

            # 先定义json中data的post_list
            post_list = []
            is_more = False


            post_number = input.post_count + 1

            what = "post.post_id as post_id, post.add_time as add_time, post.user_id as user_id, "
            what += "post.content as content, post.img_url as img_url, "
            what += "post.thumbnail_img_url as thumbnail_img_url"

            if input.start_post_id != 0:
                results = db.select('post,user',
                                    vars = {'id':input.start_post_id,
                                            'post_count':post_number,
                                            'start_index':input.start_index,
                                            'campus_id':campus_id},
                                    where = "post_id<=$id and user.user_id=post.user_id and user.campus_id=$campus_id",
                                    order = 'post_id desc',
                                    what = what,
                                    limit = "$start_index, $post_count")

                for i in results:
                    post_list.append({'user_id':i.user_id, 'post_id':i.post_id, 'add_time':i.add_time,
                            'content':i.content, 'img_url':i.img_url,
                            'thumbnail_img_url':i.thumbnail_img_url})
                post_count = len(results)

                if post_count == post_number:
                    post_count = post_number - 1
                    post_list.pop()
                    is_more = True
                else:
                    is_more = False
            else:
                results = db.select('post,user',
                                    vars = {'campus_id':campus_id},
                                    where = "user.user_id=post.user_id and user.campus_id=$campus_id",
                                    order = 'post_id desc',
                                    what = what,
                                    limit = '0, 11')

                for i in results:
                    post_list.append({'user_id':i.user_id, 'post_id':i.post_id, 'add_time':i.add_time,
                            'content':i.content, 'img_url':i.img_url,
                            'thumbnail_img_url':i.thumbnail_img_url})
                post_count = len(results)

                if post_count == 11:
                    post_count = 10
                    post_list.pop()
                    is_more = True
                else:
                    is_more = False

                input.start_index = 0

            for i in post_list:
                results = db.select('userinfo', vars = {'id':i['user_id']},
                                    where = "user_id=$id and type='nickname'",
                                    what = "information")
                if len(results) > 0:
                    i['user_name'] = results[0].information
                else:
                    mobile = db.select('user', vars = {'id':i['user_id']},
                                       where = "user_id=$id",
                                       what = "mobile")[0].mobile

                    i['user_name'] = "用户" + mobile[-4:]

                results = db.select('userinfo', vars = {'id':i['user_id']},
                                where = "user_id=$id and type='img_url'",
                                what = "information")
                if len(results) > 0:
                    i['user_img_url'] = results[0].information
                else:
                    i['user_img_url'] = None

                i['favor_count'] = db.select('favor', vars = {'id':i['post_id']},
                                             where = "post_id=$id",
                                             what = "count(*) as favor_count")[0].favor_count

                i['comment_count'] = db.select('comments', vars = {'id':i['post_id']},
                                             where = "post_id=$id",
                                             what = "count(*) as comment_count")[0].comment_count
            if len(post_list) > 0:
                start_post_id = post_list[0]['post_id']
            else:
                start_post_id = 0
            return output(200, {'start_post_id':start_post_id, "start_index":0,
                                'post_count':post_count, 'is_more':is_more,
                                'post_list':post_list})

        # except:
        #     return output(700)
