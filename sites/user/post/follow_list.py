#!/usr/bin/python
# -*- coding: utf8 -*-
"""
author: nango
update_time: 2015/7/30--15:23

apis:
    /user/post/follow/list
"""

import route
import re
import web
from database import *
from output import *
from encrypt import *
from verify import *


@route.route('/user/post/follow/list')
class UserPostFollowList:  # 获取关注用户的文章列表
    def POST(self):  # 传入access_token,user_id,start_poost_id,start_index,end_index
        input = web.input(access_token=None, user_id=None, start_post_id=None,
                          start_index=None, post_count=None)

        # 缺少必填参数
        if(input.access_token == None or input.user_id == None or input.start_post_id == None or
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

        try:
            db = getDb()
            results = db.select('token', vars={'user_id': input.user_id,
                                               'access_token': input.access_token},
                                where="user_id=$user_id and access_token=$access_token")
            # access_token权限不足
            if len(results) != 1:
                return output(410)



            post_list = []

            post_number = input.post_count + 1
            what = "post.post_id as post_id, post.add_time as add_time, post.user_id as user_id, "
            what += "post.content as content, post.img_url as img_url, "
            what += "post.thumbnail_img_url as thumbnail_img_url"

            if input.start_post_id == 0:
                where = 'post.user_id=follow.followed_id and follow.user_id=$user_id'
                results = db.select('post,follow', vars = {'user_id':input.user_id},
                                    where = where,
                                    what = what,
                                    order = "post_id desc",
                                    limit = "0,11")
                for i in results:
                    post_list.append({'user_id':i.user_id, 'post_id':i.post_id,
                                      'add_time':str(i.add_time),
                            'content':i.content, 'img_url':i.img_url,
                            'thumbnail_img_url':i.thumbnail_img_url})

                post_count = len(post_list)

                if post_count == 11:
                    post_count = 10
                    post_list.pop()
                    is_more = True
                else:
                    is_more = False

                input.start_index = 0

            else:
                where = 'post.post_id<=$id and post.user_id=follow.followed_id '
                where += 'and follow.user_id=$user_id'
                results = db.select('post,follow', vars = {'id':input.start_post_id,
                                                           'post_count':post_number,
                                                           'start_index':input.start_index,
                                                           'user_id':input.user_id},
                                    where = where,
                                    what = what,
                                    order = "post_id desc",
                                    limit = "$start_index, $post_count")

                for i in results:
                    post_list.append({'user_id':i.user_id, 'post_id':i.post_id,
                                      'add_time':str(i.add_time),
                            'content':i.content, 'img_url':i.img_url,
                            'thumbnail_img_url':i.thumbnail_img_url})

                post_count = len(post_list)

                if post_count == post_number:
                    post_count = post_number - 1
                    post_list.pop()
                    is_more = True
                else:
                    is_more = False



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

                    i['user_name'] = u"用户" + mobile[-4:]

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

        except:
            return output(700)

