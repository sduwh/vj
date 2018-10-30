"""Judger 全局配置"""
# ip 地址
ip = "localhost"

# 数据库地址
dbhost = "mongodb://{}:27017/".format(ip)

# 数据库名
dbname = "vj"

# 超时重试(秒)
timeout = 3

# 页面访问间隔(秒)
time_interval = 0.2

# 账号信息
# 用于向OJ提交代码
account_list = {
    "POJ2": {
        "username": "sduwhvj",
        "password": "sdu@wh",
        "nickname": "sduwhvj",
    },
    "POJ": {
        "username": "tester666",
        "password": "tester666",
        "nickname": "tester666",
    },
    "HDU": {
        "username": "sduwhvj",
        "password": "sduwhvj2016",
        "nickname": "sduwhvj",
    },
    "SDUT": {
        "username": "sduwhvj1",
        "password": "sduwhvj1",
        "nickname": "sduwhvj",
    },
    "VJudge": {
        "username": "sduwhvj",
        "password": "sduwhvj2016",
        "nickname": "sduwhvj",
    },
    "VJudge1": {
        "username": "sduwhvj2018",
        "password": "sduwhvj2018",
        "nickname": "sduwhvj2018",
    }
}

# scylla 代理
scylla_proxy = {'http': "{}:8081".format(ip)}

# 全局代理
proxy = None

# headers
headers = {
    'connection': 'close',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'cache-control': "no-cache",
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Mobile Safari/537.36',
}

# 日志级别
ERROR = True
INFO = True

import time


def getTime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


def print_error(message, e):
    if ERROR:
        try:
            print("{} [ERROR] {}\n{}".format(getTime(), message, e))
        except Exception as e:
            print("{} [ERROR] 编码错误\n{}".format(getTime(), e))


def print_info(message):
    if INFO:
        try:
            print("{} [INFO] {}".format(getTime(), message))
        except Exception as e:
            print("{} [ERROR] 编码错误\n{}".format(getTime(), e))


# ipProxy
import requests

proxy_pool_url = "http://{}:5010".format(ip)


def get_proxy():
    return requests.get("{}/get/".format(proxy_pool_url)).text


def delete_proxy(proxy):
    requests.get("{}/delete/?proxy={}".format(proxy_pool_url, proxy))
