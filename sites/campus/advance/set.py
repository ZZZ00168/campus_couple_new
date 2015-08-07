#!/usr/bin/python
# -*- coding: utf8 -*-
"""
author:
update_time: 2015/7/29--13:23
apis:
    /campus/advance/time/set
"""
import web

import route
from database import *
from output import *


@route.route('/campus/advance/time/set')
class CampusAdvanceTimeSet:
    def POST(self):                 #设置开始营业前接单提前的时间（单位：分钟）
        input = web.input(access_token='', advance_time='')
        if input.access_token == '' or input.advance_time=='':
            return output(110)
        if input.advance_time>120 or input.advance_time<=0:
            return output(118)
        db = getDb()
        try:
            campus_id = db.select('campus_token', vars={'access_token': input.access_token},
                                  where="access_token=$access_token", what="campus_id")
        except:
            return output(700)

        if len(campus_id) == 0:
            return output(412)
        campus_id = campus_id[0].campus_id

        try:
            result = db.select('batch_segment', vars={'campus_id': campus_id}, where="campus_id=$campus_id")
        except:
            return output(700)
        if len(result) == 0:
            return output(700)
        data = {}
        temp = 0
        for i in result:
            begin = int(i.begin_hour * 60 + i.begin_min)
            end = int(i.end_hour * 60 + i.end_min)
            data[begin] = end
        dict = sorted(data.iteritems(), key=lambda d: d[0])

        for k in dict:
            if temp > k[0]:
                #TODO:返回提前时间超出规定范围
                return output(233)
            temp = int(input.advance_time) + k[1]
        try:
            db.update('campus', vars={'campus_id': campus_id}, where="campus_id=$campus_id",
                      advance_time=input.advance_time)
        except:
            return output(700)
        return output(200)
