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
        input = web.input(access_token=None, user_id=None, start_post_id=None, start_index=None, end_index=None, )

        # 缺少必填参数
        if input.access_token == None or input.user_id == None or input.start_post_id == None or input.start_index == None or input.end_index == None:
            return output(110, False)
        try:
            input.user_id = int(input.user_id)
            input.start_post_id = int(input.start_post_id)
            input.start_index = int(input.start_index)
            input.end_index = int(input.end_index)
            if input.start_index < 0 or input.start_index > input.end_index:  # 参数值非法
                return output(112, False)
        except:
            return output(111, False)

        try:
            db = getDb()
            results = db.select('token', vars={'user_id': input.user_id, 'access_token': input.access_token},
                                where="user_id=$user_id and access_token=$access_token")
            # access_token权限不足
            if len(results) != 1:
                return output(410, False)

            # 查询是否存在start_post_id
            post_ids = db.select('post', vars={'post_id': input.start_post_id},
                                 where='post_id=$post_id', what='post_id')
            if len(post_ids) != 1:
                return output(467, False)  # start_post_id不存在

            json_data = []
            # 先定义json中data的post_list
            post_list = []
            is_more = False

            # start_post_id_index = input.start_post_id - input.start_index
            # end_post_id_index = input.start_post_id - input.end_index-1
            post_id_number = input.end_index - input.start_index + 2  # 为了判断是否又更多post而设计,如果还有post的话，则is_more=True
            results = db.select('post', vars={ 'post_id': input.start_post_id,
                                                     "post_id_number": post_id_number},
                                where="post_id>$post_id",
                                what='user_id as post_user_id,add_time,content,post_id', order='post_id desc',
                                limit="$post_id_number")
            post_count_number = len(results)
            if post_count_number == post_id_number:
                is_more = True  # 判断时候有更多

            for i in results:
                post_user_id = i.post_user_id
                post_user_info = db.select('userinfo',
                                           vars={'user_id': post_user_id,
                                                 'type1': 'nickname', 'type2': 'img_url'},
                                           where='user_id=user_id and (type=$type1 or type=$type2)')

                # 下面实现可以预先存名字，以来加快系统响应
                user_nickname = None
                user_img_url = None
                # 将user的昵称和url赋值，如果有为空的，则默认为上的的值。
                # 显然这儿是两条记录，一条nickname，一条birthday，故用try包围。
                # 目的是防止查表两次，这样的话查表一次就行。
                for j in post_user_info:
                    try:
                        user_nickname = j.nickname
                    except:
                        pass
                    try:
                        user_img_url = j.img_url
                    except:
                        pass
                user_mobile = '1234'
                if user_nickname == None:  # 加上他的电话后四位。
                    user_mobile = db.select('user', vars={'user_id': post_user_id}, where='user_id=$user_id',
                                            what='mobile')
                    # 用户电话必定有，否则系统错误。
                    # 截取后四位
                    try:
                        user_mobile = str(user_mobile[0].mobile)[-4:]
                    except:
                        return output(700, False)
                    user_nickname = '用户' + str(user_mobile)



                # 对该post_user_id的点赞总数目
                favor_count_num = db.select('favor', vars={'post_id': post_user_id}, where='post_id=$post_id',
                                            what='count(user_id)')
                favor_count_num = int(len(favor_count_num))

                # 该post的评论总数目
                comment_count_num = db.select('comments', vars={'post_id': post_user_id}, where='post_id=$post_id',
                                              what='count(user_id)')
                comment_count_num = int(len(comment_count_num))

                # 文章图片的url列表
                img_urls_list = []
                img_urls_list_db = db.select('post_img', vars={'post_id': post_user_id}, where='post_id=$post_id',
                                             what='img_url')
                if len(img_urls_list_db) > 0:
                    for img_i in img_urls_list_db:
                        img_urls_list.append(img_i.img_url)

                post_list.append({"user_id": i.post_user_id, "user_img_url": user_img_url, "user_name": user_nickname,
                                  "post_id": i.post_id, "add_time": str(i.add_time), "content": i.content,
                                  "img_urls_list": img_urls_list, "favor_count": favor_count_num,
                                  "comment_count": comment_count_num})
            json_data.append(
                {"start_post_id": input.start_post_id, "start_index": input.start_index,
                 "post_count": post_count_number, "is_more": is_more, "post_list": post_list})
            return output(200, json_data)

        except:
            return output(700, False)
