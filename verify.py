#!/usr/bin/python
# -*- coding: utf8 -*-

import random
import urllib
import urllib2

from encrypt import *
from database import *


# return values:
#   700: system error
#   701: system error for failing to send out SMS message
#   200: succeed

def sendSMSMessage(mobile, verify_code):
    password = encrypt("woshiruanjin1")
    msg = '【farseer810】您的验证码为%s，在%d分钟内有效。' % (str(verify_code), 3)
    params = {'u' : 'farseer810', 'p' : password, 'm' : mobile, 'c' : msg}
    params = urllib.urlencode(params)
    req = urllib2.Request('http://api.smsbao.com/sms?' + str(params))
    return urllib2.urlopen(req).read()


def sendVerifyCode(mobile, db = None):
    try:
        if db == None:
            db = getDb()
        user_id = db.select('user', vars = {'mobile' : mobile}, where = "mobile=$mobile")[0].user_id


        verify_code = random.randint(100000, 999999)


        if len(db.select('user_verify', vars={'id': user_id}, where="user_id=$id")) > 0:
            db.update('user_verify', vars={'id': user_id}, where="user_id=$id",
                      verify_code=verify_code, add_time=None, fail_count = 0)
        else:
            db.insert('user_verify', user_id = user_id, verify_code = verify_code, fail_count = 0 ,add_time = None)
	result_code = sendSMSMessage(mobile, verify_code)
	result_code = int(result_code)
        #TODO: send SMS message
        if result_code != 0:
            return 700

        return 200
    except:
        return 700
