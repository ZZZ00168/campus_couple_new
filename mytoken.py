#!/usr/bin/python
# -*- coding: utf8 -*-

from database import *
def getUserByToken(db, token):
    try:
        results = db.select('token', vars = {'token' : str(token)},
                  where = "access_token=$token", what = 'user_id')

        if len(results) == 0:
            return None
        db.update('token', vars = {'token' : token},
                  where = "access_token=$token", activate_time = None)
        return results[0].user_id
    except:
        return None