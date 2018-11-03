"""Spider 全局配置"""
# ip 地址
host = "localhost"

# 数据库地址
dbhost = "mongodb://{}:27017/".format(host)

# 数据库名
dbname = "vj"

# 全局超时重试(秒)
timeout = 3

# 一次获得的题目数量(尽量大一些，太小会严重影响性能)
problem_num_once = 100

# 支持的 oj 源
oj_list = [
    # 'All',
    # '51Nod',
    # 'ACdream',
    # 'Aizu',
    # 'AtCoder',
    # 'CodeChef',
    # 'CodeForces',
    # 'CSU',
    # 'EIJudge',
    # 'EOlymp',
    # 'FZU',
    # 'Gym',
    # 'HackerRank',
    'HDU',
    # 'HihoCoder',
    # 'HIT',
    # 'HRBUST',
    # 'HUST',
    # 'HYSBZ',
    # 'Kattis',
    # 'LightOJ',
    # 'Minieye',
    # 'NBUT',
    # 'OpenJ_Bailian',
    # 'OpenJ_POJ',
    # 'POJ',
    # 'SCU',
    # 'SGU',
    # 'SPOJ',
    # 'TopCoder',
    # 'UESTC',
    # 'UESTC_old',
    # 'URAL',
    # 'UVA',
    # 'UVALive',
    # 'Z_trening',
    # 'ZOJ',
]

# scylla 代理
scylla_proxy = {'http': "{}:8081".format(host)}

# 全局代理
proxy = None

# 获取题目 url
problem_api_url = 'https://vjudge.net/problem/data'

# 获得远程 oj 提交方式 url
remote_oj_url = "https://vjudge.net/util/remoteOJs"

# 对应 https://vjudge.net/problem/data 的 Form Data
form_data = {
    'draw': '3',
    'columns[0][data]': '0',
    'columns[0][name]': '',
    'columns[0][searchable]': 'true',
    'columns[0][orderable]': 'false',
    'columns[0][search][value]': '',
    'columns[0][search][regex]': 'false',
    'columns[1][data]': '1',
    'columns[1][name]': '',
    'columns[1][searchable]': 'true',
    'columns[1][orderable]': 'true',
    'columns[1][search][value]': '',
    'columns[1][search][regex]': 'false',
    'columns[2][data]': '2',
    'columns[2][name]': '',
    'columns[2][searchable]': 'false',
    'columns[2][orderable]': 'false',
    'columns[2][search][value]': '',
    'columns[2][search][regex]': 'false',
    'columns[3][data]': '3',
    'columns[3][name]': '',
    'columns[3][searchable]': 'true',
    'columns[3][orderable]': 'true',
    'columns[3][search][value]': '',
    'columns[3][search][regex]': 'false',
    'columns[4][data]': '4',
    'columns[4][name]': '',
    'columns[4][searchable]': 'true',
    'columns[4][orderable]': 'true',
    'columns[4][search][value]': '',
    'columns[4][search][regex]': 'false',
    'columns[5][data]': '5',
    'columns[5][name]': '',
    'columns[5][searchable]': 'true',
    'columns[5][orderable]': 'true',
    'columns[5][search][value]': '',
    'columns[5][search][regex]': 'false',
    'columns[6][data]': '6',
    'columns[6][name]': '',
    'columns[6][searchable]': 'true',
    'columns[6][orderable]': 'false',
    'columns[6][search][value]': '',
    'columns[6][search][regex]': 'false',
    'order[0][column]': '3',  # 3-按照题号排序
    'order[0][dir]': 'asc',  # 排序 [asc/desc]
    'start': '0',  # 开始位置
    'length': '100',  # 长度
    'search[value]': '',
    'search[regex]': 'false',
    'OJId': 'All',  # oj名字
    'probNum': '',
    'title': '',
    'source': '',
    'category': 'all',
}

# headers
headers = {
    'connection': 'close',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'cache-control': "no-cache",
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Mobile Safari/537.36',
}

# 日志
ERROR = True
INFO = True

import time


def getTime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


def print_error(message, e):
    if ERROR:
        try:
            print("%s [ERROR] %s\n%s" % (getTime(), message, e))
        except Exception as e:
            print("%s [ERROR] 编码错误\n%s" % (getTime(), e))


def print_info(message):
    if INFO:
        try:
            print("%s [INFO] %s" % (getTime(), message))
        except Exception as e:
            print("%s [ERROR] 编码错误\n%s" % (getTime(), e))


# proxy_pool
import requests

proxy_pool_url = "http://{}:5010".format(host)


def get_proxy():
    return requests.get("{}/get/".format(proxy_pool_url)).text


def delete_proxy(proxy):
    requests.get("{}/delete/?proxy={}".format(proxy_pool_url, proxy))
