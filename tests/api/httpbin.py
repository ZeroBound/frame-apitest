#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author      : zzw
@time        : 2019/8/5 22:29
@file        : httpbin.py
@description : General Test Method
"""
from frameapitest.api import BaseApi


class ApiHttpBinGet(BaseApi):
    """
    Get request method
    """
    url = "http://httpbin.org/get"
    params = {}
    method = "GET"
    headers = {"accept": "application/json"}


class ApiHttpBinPost(BaseApi):
    url = "http://httpbin.org/post"
    method = "POST"
    params = {}
    headers = {"accept": "application/json"}
    json = {"abc": 123}


class ApiHttpBinGetCookies(BaseApi):
    url = "http://httpbin.org/cookies"
    method = "GET"
    params = {}
    headers = {"accept": "application/json"}


class ApiHttpBinGetSetCookies(BaseApi):
    url = "http://httpbin.org/cookies/set"
    method = "GET"
    params = {}
    headers = {"accept": "text/plain"}
