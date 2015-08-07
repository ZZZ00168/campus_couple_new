#!/usr/bin/python
# -*- coding: utf8 -*-


"""
    author:nango

update_time: 2015/7/23--12:05

apis:
    /campus/batch/segment/list
"""

import route
import web
import random
import time
from database import *
from output import *
from encrypt import *


@route.route('/campus/batch/segment/list')
class CampusBatchSegmentListGet:
    def POST(self):
        input = web.input(accesstoken='')
        # 参数不足
        if input.access_token == '':
            return output(118)
        db = getDb()
        results = db.select('campus_token', vars={'token': input.access_token},
                            where='access_token=$token', what="campus_id",order="campus_id desc")
        if len(results) > 0:
            try:
                # 获取camupus id
                campus_id = results[0].campus_id
                # 查询batch_segment表，获取数据并排序
                results = db.select('batch_segment', vars={'campus_id': campus_id},
                                    where='campus_id=$campus_id',
                                    order="begin_hour,begin_min,begin_second,end_hour,end_min,end_second asc")

                data = []
                for i in results:
                    data.append(GetTimeStr.getTimeStr(i.begin_hour, i.begin_min, i.end_hour, i.end_min))

                # data = sorted(data)
                data1 = []
                indext = 1
                for i in data:
                    data1.append({"batch_number": indext, "bacth_string": i})
                    indext = indext + 1
                return output(200, data1)
            except:
                return output(700)
        else:
            # 权限不足，不允许删
            return output(420)


class GetTimeStr:
    @staticmethod
    def getStr(number=0):
        if number < 10:
            number = "0" + str(number)
        else:
            number = str(number)
        return number

    @staticmethod
    def getTimeStr(begin_hour=0, begin_min=0, end_hour=0, end_min=0):
        begin_hour = GetTimeStr.getStr(begin_hour)
        begin_min = GetTimeStr.getStr(begin_min)
        end_hour = GetTimeStr.getStr(end_hour)
        end_min = GetTimeStr.getStr(end_min)
        print begin_hour + ":" + begin_min + "-" + end_hour + ":" + end_min
        return begin_hour + ":" + begin_min + "-" + end_hour + ":" + end_min
