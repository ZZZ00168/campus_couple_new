#!/usr/bin/python
# -*- coding: utf8 -*-
#test

import web
import time

def sortbatch(campus_id):
    db = web.database(dbn='mysql', db='campus_couple', user='root', pw='123456')

    batches = db.select('batch_segment' , vars = {'campus_id':campus_id} , where = "campus_id=$campus_id")
    if len(batches) == 0:
        return None
    print 111
    # 得到当前日期
    timeStamp = time.time()
    timeArray = time.localtime(timeStamp)
    day =  str(time.strftime("%Y-%m-%d"))
    print 112
    list = []
    for i in batches:
        list.append({'begin_time':day + ' ' + str(i.begin_hour) + ':' +str(i.begin_min) + ':' + str(i.begin_second) ,
                     'end_time':day + ' ' + str(i.end_hour) + ':' +str(i.end_min) + ':' + str(i.end_second) })
    # 把 string 转化 格式
    format = "%Y-%m-%d %H:%M:%S"
    for i in list:
        i['begin_time'] = time.strptime(i['begin_time'] , format)
        i['end_time'] = time.strptime(i['end_time'] , format)
    print 113
    # hourAndMin = []
    #
    # for i in batches:
    #     hourAndMin.append({'begin_hour':i.begin_hour , 'begin_min':i.begin_min , 'begin_second':0 ,
    #                        'end_hour':i.end_hour , 'end_min':i.end_min , 'end_second':i.end_second})
    print 114
    #只要对开始时间进行排序
    for i in list:
        print i['begin_time']

    for i in range(len(list)):
        print i
        for j in range(len(list)):
            print 'fuck'
            if list[i]['begin_time'] < list[j]['begin_time'] :
                print 123
                list[i],list[j] = list[j],list[i]
            print 456
    print 115
    # 这里得到的是 [｛'begin_time':string , 'end_time':string｝,........]

    return list


