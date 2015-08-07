#!/usr/bin/python
# -*- coding: utf8 -*-
"""
author nango
update_time: 2015/7/24--21:23
apis:
    /campus/order/food/list
"""

import route
import web
import time
from output import *
from database import *
from datetime import datetime


@route.route('/campus/order/food/list')
class CampusOrderFoodList:
    def POST(self):
        input = web.input(access_token="", batch_number=0, subbatch_number=0)

        try:
            input.batch_number = int(input.batch_number)
            input.subbatch_number = int(input.subbatch_number)

            if input.batch_number == 0 or input.subbatch_number == 0:
                return output(110)  # 缺少必填参数
            elif input.batch_number < 0 or input.subbatch_number < 0:
                return output(117)  # 传入参数非法
        except:
            return output(117)  # 传入参数非法

        # 查看access_token是否存在
        db = getDb()
        result_token = db.select('campus_token', vars={'token': input.access_token},
                                 where='access_token=$token')
        # 查看access_token和用户是否对应正确
        if len(result_token) != 1:
            return output(420)  # 权限不足
        result_token = result_token[0]

        # 获取dibatch_number批次的开始时间。
        # 查询batch_segment表，获取数据并排序
        results = db.select('batch_segment', vars={'campus_id': result_token.campus_id},
                            where='campus_id=$campus_id',
                            order="begin_hour,begin_min,begin_second,end_hour,end_min,end_second asc")
        try:
            results = results[input.batch_number - 1]
        except:
            return output(434)  # batch_number太大


        # 获取start_time的时间戳，即某批次开始的时间戳
        start_time = GetTimeStr.getTimeStamp(results)
        # 获得子批次的开始时间
        start_time = (input.subbatch_number - 1) * 5 * 60
        end_time = start_time + 5 * 60  # 一个批次五分钟

        # 三张表查询，获取食物名称和 mktime()

        formats = "%Y-%m-%d %H:%M:%S"
        start_time = int(time.mktime(time.strptime(start_time, formats)))
        end_time = int(time.mktime(time.strptime(end_time, formats)))

        try:
            results = db.select('orders', vars={"start_time": start_time, "end_time": end_time,
                                                "campus_id": result_token.campus_id},
                                where="campus_id=$campus_id and (unix_timestamp(add_time) between $start_time and $end_time)",
                                what="order_id")
            food_list = {}

            for i in results:
                ordered_food = db.select('ordered_food', vars={'id': i.order_id}, where="order_id=$id")
                for food in ordered_food:
                    food_list[food.food_id] = food_list.get(food.food_id, 0) + food.number

            food_list2 = []

            for id in food_list:
                food_name = db.select('food', vars={'id': id}, where="food_id=$id", what='food_name')[0].food_name
                food_list2.append({'food_name': food_name, 'number': food_list[id]})

            return output(200, food_list2)

        except:
            return output(700)


class GetTimeStr:
    @staticmethod
    def getStr(number=0):
        if number < 10:
            number = "0" + str(number)
        else:
            number = str(number)
        return number

    @staticmethod
    def getTimeStamp(results):
        batch_time_start = GetTimeStr.getStr(results.begin_hour) + ":" + GetTimeStr.getStr(
            results.begin_min) + GetTimeStr.getStr(results.begin_second)
        now_time = datetime.now()
        start_time = GetTimeStr.getStr(now_time.year) + "-" + GetTimeStr.getStr(
            now_time.month) + "-" + GetTimeStr.getStr(now_time.day) + " "
        formats = "%Y-%m-%d %H:%M:%S"
        # 将start_time、endtime转换成timestamp
        start_time = start_time + str(batch_time_start)
        start_time = int(time.mktime(time.strptime(start_time, formats)))
        return start_time
