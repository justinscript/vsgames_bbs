#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    define return code
'''

# code for a json-request
class jsoncode():
    success = {'data': 1}
    
    fail = {'data': 0}

# add extra message    
def add_item(dic, key, value):
    dic.__setitem__(key, value)
    return dic