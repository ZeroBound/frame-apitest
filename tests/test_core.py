#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author      : zzw
@time        : 2019/8/3 14:35
@file        : test_core.py
@description : 
"""
from tests.api.httpbin import ApiHttpBinGet, ApiHttpBinPost, ApiHttpBinGetCookies, ApiHttpBinGetSetCookies


def test_version():
    from frameapitest import __version__
    assert "0.1.0" == __version__


def test_httpbin_get():
    ApiHttpBinGet().run()\
        .validate("status_code", 200)\
        .validate("headers.server", "nginx")\
        .validate("json().url", "https://httpbin.org/get")\
        .validate("json().args", {})\
        .validate("json().headers.Accept", "application/json")


def test_httpbin_get_with_prams():
    ApiHttpBinGet().set_params(abc=123, xyz=456).run()\
        .validate("status_code", 200)\
        .validate("headers.server", "nginx")\
        .validate("json().url", "https://httpbin.org/get?abc=123&xyz=456")\
        .validate("json().headers.Accept", "application/json")


def test_httpbin_post():
    ApiHttpBinPost().set_json({"abc": 456}).run()\
        .validate("status_code", 200)\
        .validate("headers.server", "nginx")\
        .validate("json().url", "https://httpbin.org/post")\
        .validate("json().headers.Accept", "application/json")\
        .validate("json().json.abc", 456)


def test_httpbin_parameters_share():
    user_id = "adb110"
    ApiHttpBinGet().set_params(user_id=user_id).run()\
        .validate("status_code", 200)\
        .validate("headers.server", "nginx")\
        .validate("json().url", "https://httpbin.org/get?user_id={}".format(user_id))\
        .validate("json().headers.Accept", "application/json")\

    ApiHttpBinPost().set_json({"user_id": user_id}).run()\
        .validate("status_code", 200)\
        .validate("headers.server", "nginx")\
        .validate("json().url", "https://httpbin.org/post")\
        .validate("json().headers.Accept", "application/json")\
        .validate("json().json.user_id", user_id)


def test_httpbin_extract():
    api_run = ApiHttpBinGet().run()
    status_code = api_run.extract("status_code")
    assert status_code == 200

    server = api_run.extract("headers.server")
    assert server == "nginx"

    accept_type = api_run.extract("json().headers.Accept")
    assert accept_type == "application/json"


def test_httpbin_setcookies():
    cookies = {
        "freeform1": "123",
        "freeform2": "456"
    }

    api_run = ApiHttpBinGetCookies().set_cookies(**cookies).run()
    free1 = api_run.extract("json().cookies.freeform1")
    free2 = api_run.extract("json().cookies.freeform2")
    assert free1 == "123" and free2 == "456"


def test_httpbin_patameters_extract():
    # get value
    freeform = ApiHttpBinGetCookies().set_cookie("freeform", "123").run()\
        .extract("json().cookies.freeform")
    assert freeform == '123'

    # use value as parameter
    ApiHttpBinPost().set_json({"freeform": freeform}).run()\
        .validate("status_code", 200)\
        .validate("headers.server", "nginx")\
        .validate("json().url", "https://httpbin.org/post")\
        .validate("json().headers.Accept", "application/json")\
        .validate("json().json.freeform", freeform)


def test_httpbin_login_status():
    import requests
    session = requests.sessions.Session()

    # login and get cookies
    ApiHttpBinGetSetCookies().set_params(freeform="567").run(session)

    # request another api, check cookie
    res = ApiHttpBinPost().set_json({"abc": 123})\
        .run(session).get_response()

    request_headers = res.request.headers

    # print(request_headers)
    assert "freeform=567" == request_headers["Cookie"]
