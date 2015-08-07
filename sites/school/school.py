#!/usr/bin/python
# -*- coding: utf8 -*-
"""
update_time: 2015/7/19--13:23
apis:
    /school/list
    /school/add
    /school/name
"""

import route
from database import *
from output import *

@route.route('/school/list')
class SchoolList:
    def GET(self):
        return self.getSchoolList()
    def POST(self):
        return self.getSchoolList()

    def getSchoolList(self):
        school_list = []
        db = getDb()
        for i in db.select('school'):
            school_list.append({'id' : i.school_id, 'name' : i.school_name})
        return output(200 , school_list)


@route.route('/school/add')
class SchoolAdd:
    def POST(self):
        pass

@route.route('/school/name')
class SchoolChangeName:
    def POST(self):
        pass


