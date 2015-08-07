#!/usr/bin/python
# -*- coding: utf8 -*-

import route
import web
from database import *
from output import *

@route.route('/campus/batch/segment/delete')
class CampusBatchSegmentDelete:
    def POST(self):
        input=web.input(access_token='',delete_num='')
        db=getDb()
        result = db.select('campus_token' ,vars={'access_token':input.access_token} , where = "access_token=$access_token" )
        if len(result) == 0 :
            return output(420)#token 权限不足
        else :
            campus_id = result[0].campus_id

        allTime = db.select('batch_segment' ,vars={'campus_id':campus_id} , where = "campus_id=$campus_id",order='begin_hour asc,begin_min asc')

        data=[]
        for i in allTime:
            data.append(i.begin_hour)
        deleted_line=int(input.delete_num)-1

        db.delete('batch_segment',vars={"data1":data[deleted_line]},where='begin_hour=$data1')


        return output(200)





