#!/usr/bin/python
# -*- coding: utf8 -*-
#author:zzz

import web
import route
import time

from output import *
from database import *
from sortBatch import *

@route.route('/campus/order/confirm')
class CampusOrderConfirm:
    def POST(self):
        db = getDb()
        input = web.input(access_token = None , batch_number = None , subbatch_number = None )

        #判断格式
        try :
            input.batch_number = int(input.batch_number)
            input.subbatch_number = int(input.subbatch_number)
        except:
            return output(117)#todo 参数错误

        #判断是否存在token
        campus = db.select('campus_token' , vars= {'token':input.access_token} , where="access_token=$token")
        if len(campus) == 0:
            return output(420) #todo 用户权限不足
        campus = campus[0]

        #读取出campus 对应的batch 并且对其排序  其格式是  [ { 'begin_time':     , 'end_time'.           }]
        batches = sortbatch(campus.campus_id)
        if batches == None:
            return output(700)

        #取出对应时段的batch
        batch = batches[input.batch_number - 1]

        #todo 接下来这里要根据campous设定的间隔时间 ，还有传入的参数subbatch_num 截取时间
        #todo 这里暂时假设 间隔时间 interval 是 5min

        interval = 5

        #计算开始和结束时间
        #todo 这里不考虑23：59：59 - 00：00：00的情况
        subbatch_begin_min = batch['begin_time'][4] + interval*(input.subbatch_number-1)

        subbatch_begin_hour = batch['begin_time'][3]

        #对时间越界进行判断
        while subbatch_begin_min >= 60:
            subbatch_begin_hour = subbatch_begin_hour + 1
            subbatch_begin_min = subbatch_begin_min - 60


        #结束时间也要判断一下是否跨小时

        subbatch_end_hour = subbatch_begin_hour
        subbatch_end_min = subbatch_begin_min + interval


        if subbatch_end_min >= 60:
            subbatch_hour = subbatch_end_hour + 1
            subbatch_begin_min = subbatch_begin_min - 60

        #先把得到的开始和结束的时间转化为 string 再转化成 struct_time 类型

        begin_time_string = str(batch['begin_time'][0]) + '-' + str(batch['begin_time'][1]) + '-' +str(batch['begin_time'][2]) +\
                        ' ' + str(subbatch_begin_hour) + ':' + str(subbatch_begin_min) +':' + str(batch['begin_time'][5])

        end_time_string = str(batch['end_time'][0]) + '-' + str(batch['end_time'][1]) + '-' +str(batch['end_time'][2]) + ' ' +\
                        str(subbatch_begin_hour) + ':' + str(subbatch_end_min) +':' + str(batch['end_time'][5])


        formats = "%Y-%m-%d %H:%M:%S"

        begin_time = time.strptime(begin_time_string , formats)
        end_time = time.strptime(end_time_string , formats)

        #查表，替换
        orders = db.select('orders' , vars={'campus_id':campus.campus_id} , where="campus_id=$campus_id")
        if len(orders)==0:
            return output(0000) #todo ，没有设置时间段
        #遍历
        for i in orders:
            add_time_string  = str(i.add_time)
            add_time = time.strptime(add_time_string , formats)
            if begin_time <=  add_time < end_time:
                db.update('orders' , vars = {'order_id':i.order_id} ,where = "order_id=$order_id" , status = 'confirmed')

        return output(200)
