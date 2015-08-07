#!/usr/bin/python
# -*- coding: utf8 -*-

import route
import web

from database import *
from output import *

@route.route('/campus/list')
class CampusList:
    def POST(self):
        db = getDb()
        input = web.input(school_id = None)
        print input
        if input.school_id == None:
            return output(110)

        try:
            input.school_id = int(input.school_id)
        except :
            return output(111)

        results = db.select('campus' ,vars = {'school_id':input.school_id} , where = "school_id=$school_id")

        if len(results) == 0:
            return output(417)

        list = []

        for i in results:
            list.append({'id':i.campus_id , 'name':i.campus_name})

        return output(200 ,list)
