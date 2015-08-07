#!/usr/bin/python
# -*- coding: utf8 -*-

import web
import route
from database import  *
from output import  *

@route.route('/campus/order/subbatch/list')
class CampusOrderSubbatchList:
    def POST(self):
        input=web.input(access_token='',batch_number='')
        db=getDb()
        result = db.select('campus_token' ,vars={'access_token':input.access_token} , where = "access_token=$access_token" )
        if len(result) == 0 :
            return output(420)#token 权限不足
        else :
            campus_id = result[0].campus_id

        if input.batch_number == None:
            return output(110)#缺少必填参数
        try:
            batch_number=int(input.batch_number)
        except:
            return output(117)#参数类型非法

        s=db.query("SELECT COUNT(*) AS total_batchs FROM batch_segment")
        all_batchs =int(s[0].total_batchs) #batch 的总数
        if batch_number>all_batchs or batch_number<1 :
            return output(434) #TODO:参数小于1?

        batchSegment=db.select('batch_segment',vars={'campus_id':campus_id},where='campus_id=$campus_id',order='begin_hour asc')
        selectedSegment=batchSegment[batch_number-1]
        beginHour=selectedSegment.begin_hour
        beginMin=selectedSegment.begin_min
        endHour=selectedSegment.end_hour
        endMin=selectedSegment.end_min#提取时间
        #
        served_time=(endHour-beginHour)*60+(endMin-beginMin)
        batch_sum=(served_time+5-1)//5  #暂定5分钟

        test=[[0 for col in range(2)] for row in range(batch_sum+1)]#存hour 和 min的数组

        test[0][0]=beginHour
        test[0][1]=beginMin
        i=1
        while i<batch_sum:
            test[i][1]=test[i-1][1]+5
            if test[i][1]>=60:
                test[i][0]=test[i-1][0]+1
                test[i][1]=test[i][1]-60
                i=i+1
            else:
                test[i][0]=test[i-1][0]
                i=i+1

        test[batch_sum][0]=endHour
        test[batch_sum][1]=endMin

        timeString=[0 for x in range(batch_sum)]#把时间段转化成string并用数组存起来
        f=0
        while f<batch_sum:
            if test[f][1]>9 and test[f+1][1]>9:#补零
                timeString[f]=str(test[f][0])+":"+str(test[f][1])+"-"+str(test[f+1][0])+":"+str(test[f+1][1])
                f=f+1
            else:
                if test[f][1]<=9 and test[f+1][1]>9:
                    timeString[f]=str(test[f][0])+":0"+str(test[f][1])+"-"+str(test[f+1][0])+":"+str(test[f+1][1])
                    f=f+1
                elif test[f][1]>9 and test[f+1][1]<=9:
                    timeString[f]=str(test[f][0])+":"+str(test[f][1])+"-"+str(test[f+1][0])+":0"+str(test[f+1][1])
                    f=f+1
                else:
                    timeString[f]=str(test[f][0])+":0"+str(test[f][1])+"-"+str(test[f+1][0])+":0"+str(test[f+1][1])
                    f=f+1

        resul=[]
        m=0
        while m<batch_sum:
            resul.append({"subbatch_number":m+1,"subbatch_time":timeString[m]})
            m=m+1

        return output(200,resul)





















