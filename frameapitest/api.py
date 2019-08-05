#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author      : zzw
@time        : 2019/8/5 21:48
@file        : api.py
@description : 基础类
"""
import requests


class BaseApi(object):

    method = "GET"
    url = ""
    params = None
    headers = None
    data = None
    cookies = None
    files = None
    auth = None
    timeout = None
    allow_redirects = True
    proxies = None
    hooks = None
    stream = None
    verify = False
    cert = None
    json = None

    def __int__(self):
        self.response = None

    def set_params(self, **params):
        """
        set the params
        :param params: dict or bytes
        :return: BaseApi object
        """
        self.params = params
        return self

    def set_cookie(self, key, value):
        """
        set the cookie by 'key' and 'value', you can set it up multiple cookie
        :param key: key of cookie
        :param value: value of cookie
        :return: BaseApi object
        """
        self.cookies = self.cookies or {}
        self.cookies.update({key: value})
        return self

    def set_cookies(self, **kwargs):
        """
        setting up multiple cookie
        :param kwargs:
        :return:
        """
        self.cookies = self.cookies or {}
        self.cookies.update(kwargs)
        return self

    def set_json(self, json_data):
        """
        set the json data
        :param json_data:
        :return: BaseApi object
        """
        self.json = json_data
        return self

    def run(self, session=None):
        """
        the main method for request to get or post ec.
        :param session:
        :return:
        """
        session = session or requests.sessions.Session()
        self.response = session.request(
            self.method,
            self.url,
            params=self.params,
            data=self.data,
            headers=self.headers,
            cookies=self.cookies,
            files=self.files,
            auth=self.auth,
            timeout=self.timeout,
            allow_redirects=self.allow_redirects,
            proxies=self.proxies,
            hooks=self.hooks,
            stream=self.stream,
            verify=self.verify,
            cert=self.cert,
            json=self.json
        )
        return self

    def extract(self, field):
        """
        extract data for response
        :param field:
        :return:
        """
        value = self.response
        for _key in field.split("."):
            if isinstance(value, requests.Response):
                if _key == "json()":
                    value = self.response.json()
                else:
                    value = getattr(value, _key)
            elif isinstance(value, (requests.structures.CaseInsensitiveDict, dict)):
                value = value[_key]
        return value

    def validate(self, key, expected_value):
        """
        validate results for interface test
        :param key: need to validate key
        :param expected_value: results of expected
        :return:
        """
        actual_value = self.extract(key)
        assert actual_value == expected_value
        return self

    def get_response(self):
        """

        :return:
        """
        return self.response
