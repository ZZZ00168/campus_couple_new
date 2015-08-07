#!/usr/bin/python
# -*- coding: utf8 -*-

import hashlib

def encrypt(text):
    m = hashlib.md5()
    m.update(text)
    return m.hexdigest()
