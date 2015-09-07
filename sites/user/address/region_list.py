#!/usr/bin/python
# -*- coding: utf8 -*-
"""
update_time: 2015/9/8 2:05
apis:
    /region/list
"""

import route
import web
from database import *
from output import *

@route.route('/region/list')
class RegionList:
    def POST(self):
        input = web.input(access_token = None, user_id = None)

        if input.access_token == None or input.user_id == None:
            return output(110)

        try:
            input.user_id = int(input.user_id)
        except:
            return output(111)

        db = getDb()

        if len(db.select('token', vars = {'token':input.access_token, 'id':input.user_id},
                         where = "access_token=$token and user_id=$id")) == 0:
            return output(410)

        campus_id = db.select('user', vars = {'id':input.user_id},
                              where = "user_id=$id", what = "campus_id")[0].campus_id

        results = db.select('region', vars = {'id':campus_id}, where = "campus_id=$id",
                            what = "region_id, region_name")

        region_list = []
        for i in results:
            region_list.append({'id':i.region_id, 'name':i.region_name})

        return output(200, region_list)
