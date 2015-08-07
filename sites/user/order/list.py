#!/usr/bin/python
# -*- coding: utf8 -*-

"""
    author:nango

update_time: 2015/7/22--16:05

apis:
    /user/order/list
"""

import route
import web
from database import *
from output import *


@route.route('/user/order/list')
class UserOrderList:  # 返回该用户的订单列表
    def POST(self):  # 传入access_token,user_id以及order_id(选填），oder_id 不填代表返回所有订单
        input = web.input(access_token='', user_id='', order_id=0)
        try:
            input.order_id = int(input.order_id)
            input.user_id = int(input.user_id)
        except:
            # TODO:参数错误
            return output(700)

        db = getDb()
        # 查看access——token是否存在且相等，即验证用户
        result_token = db.select('token', vars={'token': input.access_token, 'user_id': input.user_id},
                                 where='user_id=$user_id and access_token=$token', what="user_id")
        # 查看access_token和用户是否对应正确
        if len(result_token) != 1:
            return output(420)
        # 获取用户的订单
        try:
            # 获取全部订单或者指定订单
            results = getOrder.getOrderList(input.order_id, input.user_id, db)
            return output(200, results)
        except:
            # TODO:系统出错
            return output(700)


class getOrder:
    @staticmethod
    def getfoodlist(input_order_id=0, db=getDb()):  # 返回某订单号订单的foollist
        food_list = []
        results_food = db.select("ordered_food", vars={'order_id': input_order_id}, where="order_id=$order_id",
                                 what="food_id,number")

        for i in results_food:
            food_list.append({"food_id": i.food_id, "number": i.number})
        return food_list

    @staticmethod
    def getOrderList(input_order_id=0, input_user_id=0, db=getDb()):  # 返回订单的详细消息。
        if input_order_id == 0:  # 返回该用户的所有订单
            results = db.select('orders', vars={'user_id': input_user_id}, where="user_id=$user_id")

        else:  # 获取该指定订单号的订单
            results = db.select('orders', vars={"order_id": input_order_id, 'user_id': input_user_id},
                                where="order_id=$order_id and user_id=$user_id")
        orderlist = []
        for i in results:
            campus_name = db.select('campus', vars = {'id' : i.campus_id}, where = "campus_id=$id")[0].campus_name
            orderlist.append({"order_id": i.order_id, "address_id": i.address_id,
                              "campus_name": campus_name, "add_time": str(i.add_time),
                              "status": i.status,
                              "food_list": getOrder.getfoodlist(i.order_id, db)})
        return orderlist
