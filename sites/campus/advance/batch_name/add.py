#!/usr/bin/python
# -*- coding: utf8 -*-
#Author:zzz
import route
import web
import datetime

from sortBatch import *
from output import *
from database import *

@route.route('/campus/batch/segment/add')
class CampusBatchSegmentAdd:
    def POST(self):

        input = web.input(access_token = None ,begin_time = None , end_time = None)
        db = getDb()

        # 验证campus_token
        result = db.select('campus_token' ,vars={'access_token':input.access_token} , where = "access_token=$access_token" )
        if len(result) == 0 :
            return output(420)#token 权限不足
        else :
            campus_id = result[0].campus_id

        if input.begin_time == None or input.end_time == None:
            return output(99999) #todo 缺少必填参数

        # 得到当前日期
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        day =  str(time.strftime("%Y-%m-%d"))
        # 合并成为格式化的string
        string_begin = day + ' ' + input.begin_time
        string_end = day + ' ' + input.end_time

        format = "%Y-%m-%d %H:%M:%S"

        try:
            begin_time = time.strptime(string_begin , format)
            end_time = time.strptime(string_end , format)
            this_begin_time = datetime.datetime(begin_time[0],begin_time[1] , begin_time[2] , begin_time[3] , begin_time[4] ,begin_time[5])
            this_end_time= datetime.datetime(end_time[0],end_time[1] , end_time[2] , end_time[3] , end_time[4] ,end_time[5])
        except:
            return output(999)# todo 时间格式不正确

        #获取已经存在的 batches 并且是以  【｛'begin_time' :            , 'end_time':              } .........】
        batches = sortbatch(campus_id)

        if len(batches) == 0:
            return output(888) #todo 不存在对应数据

        advanceTime = db.select('campus' , vars = {'campus_id':campus_id} ,where = "campus_id=$campus_id")
        if len(advanceTime) == 0:
            return output(700) #todo 表出错
        print "yes"
        advanceTime = advanceTime[0].advance_time
        print advanceTime
        print batches
        if len(batches) != 0:
            print 123
            for i in range(len(batches)):
                if i != len(batches)-1:
                    next_begin_time = datetime.datetime(batches[i]['begin_time'][0] ,batches[i]['begin_time'][1] ,
                                                   batches[i]['begin_time'][2] , batches[i]['begin_time'][3],
                                                   batches[i]['begin_time'][4] , batches[i]['begin_time'][5])
                if i != 0:
                    last_end_time = datetime.datetime(batches[i-1]['end_time'][0] ,batches[i-1]['end_time'][1] ,
                                                   batches[i-1]['end_time'][2] , batches[i-1]['end_time'][3],
                                                   batches[i-1]['end_time'][4] , batches[i-1]['end_time'][5])
                print i
                if i == 0:
                    if next_begin_time - this_end_time <= advanceTime * 60:
                        return output(999)#todo 有重复时间
                    else :
                        continue

                if i == len(batches)-1:
                    if this_begin_time - last_end_time <= advanceTime * 60 or next_begin_time - this_begin_time <= advanceTime * 60:
                        return output(999)#todo
                    #todo 最后一种情况还没判断
                    else:
                        continue
                else:
                    if this_begin_time - last_end_time <= advanceTime * 60 or next_begin_time - this_begin_time <= advanceTime * 60:
                        return output(999)#todo 有重复时间
                    else:
                        continue

        db.insert('batch_segment' , campus_id = campus_id , begin_hour = begin_time[3] , begin_min = begin_time[4] ,
                  begin_second = begin_time[5] , end_hour = end_time[3] , end_min = end_time[4] , end_second = end_time[5])

        return output(200)

