#!/usr/bin/python
# -*- coding: utf8 -*-
"""
author: nango

update_time: 2015/7/29--23:23

apis:
    /user/post/comment/list
"""

import route
import re
from database import *
from output import *
from encrypt import *
from verify import *


@route.route('/user/post/comment/list')
class UserPostCommentList:  # 返回某文章的评论列表
    def POST(self):  # 传入 access_token,user_id,post_id
        input = web.input(access_token=None, user_id=None, post_id=None)

        # 缺少必填参数
        if input.access_token == None or input.user_id == None or input.post_id == None:
            return output(110)

        try:
            input.user_id = int(input.user_id)
            input.post_id = int(input.post_id)
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

            if len(db.select('post', vars = {'id':input.post_id}, where = "post_id=$id")) == 0:
                return output(467)

            results = db.select('comments', vars={'post_id': input.post_id}, where="post_id=$post_id")

            comment_list = []
            # 整体放入try里面，防止系统崩
            for i in results:
                user_commenter = db.select('userinfo',
                                           vars={'commented_id': i.commented_id,
                                                 'type1': 'nickname', 'type2': 'img_url'},
                                           where='user_id=$commented_id and (type=$type1 or type=$type2)')
                user_nickname = None
                user_img_url = None
                # 将user的昵称和url赋值，如果有为空的，则默认为上的的值。
                # 显然这儿是两条记录，一条nickname，一条birthday，故用try包围。
                # 目的是防止查表两次，这样的话查表一次就行。
                for j in user_commenter:
                    if j.type == 'nickname':
                        user_nickname = j.information
                    elif j.type == 'img_url':
                        user_img_url = j.information

                user_mobile = '1234'
                if user_nickname == None:  # 加上他的电话后四位。
                    user_mobile = db.select('user', vars={'user_id': i.user_id}, where='user_id=$user_id',
                                            what='mobile')
                    # 用户电话必定有，否则系统错误。
                    # 截取后四位
                    try:
                        user_mobile = str(user_mobile[0].mobile)[-4:]
                    except:
                        return output(700)
                    user_nickname = u'用户' + str(user_mobile)

                commented_name = None
                if i.commented_id != 0:
                    user_mobile = db.select('user', vars={'user_id': i.commented_id}, where='user_id=$user_id',
                                            what='mobile')
                    try:
                        user_mobile = str(user_mobile[0].mobile)[-4:]
                    except:
                        return output(700)
                    commented_name = u'用户' + str(user_mobile)

                # 最后添加进评论列表中
                comment_list.append({"comment_id": i.comment_id, "user_id": i.user_id,
                                     'user_name': user_nickname,
                                     'user_img_url': user_img_url,
                                     'add_time': str(i.add_time), 'content': i.content,
                                     "commented_name": commented_name})
            return output(200, comment_list)
        except:
            return output(700)
