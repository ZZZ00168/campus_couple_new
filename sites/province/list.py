#!/usr/bin/python
# -*- coding: utf8 -*-
"""
update_time: 2015/7/19--13:23
apis:
    /province/list
"""

import route

from output import *
from database import *

@route.route('/province/list')
class ProvinceList:
    def POST(self):
        return self.getProvinceList()
    def GET(self):
        return self.getProvinceList()

    def getProvinceList(self):
        province_list = []
        db = getDb()
        for i in db.select('province'):
            province_list.append({'id': i.province_id, 'name': i.province_name})
        return output(200, province_list)

