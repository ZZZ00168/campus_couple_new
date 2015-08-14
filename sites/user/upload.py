#!/usr/bin/python
# -*- coding: utf8 -*-
"""
update_time: 2015/7/19--13:23
apis:
    /user/upload
"""

import route
import web
import base64

from output import *
from database import *


@route.route('/user/upload')
class UserImageUpload:
    def POST(self):
		input = web.input(access_token = None, user_id = None, img_file = {})
		if input.access_token == None or input.user_id == None or input.img_file == None:
			return output(110)

		try:
			input.user_id = int(input.user_id)
		except:
			return output(111)

		db = getDb()
		if len(db.select('token', vars = {'token':input.access_token, 'id':input.user_id},
						 where = 'user_id=$id and access_token=$token')) == 0:
			return output(410)

		try:
			filename = input.img_file.filename.replace('\\', '/')
			filename = filename.split('/')[-1]
			i = filename.rfind('.')
			if i == -1:
				return output(440)
			suffix = filename[i:]
			filename = "head image of user_id %d" % (input.user_id,)
			filename = base64.b64encode(filename) + suffix
		except:
			return output(440)


		try:
			fout = open('/var/campus_couple_img/static/' + filename, 'w')
			fout.write(input.img_file.file.read())
			fout.close()
		except:
			return output(700)
		return output(200)

