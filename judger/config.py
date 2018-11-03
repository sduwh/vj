"""Judger配置"""
# Host
host = 'localhost'

# 数据库地址
dbhost = 'mongodb://{}:27017/'.format(host)

# 数据库名
dbname = 'vj'

# 超时重试(秒)
timeout = 3

# 页面访问间隔(秒)
time_interval = 1

# 账号信息
# 用于向OJ提交代码
account_list = {
    'POJ2': {
        'username': 'sduwhvj',
        'password': 'sdu@wh',
        'nickname': 'sduwhvj',
    },
    'POJ': {
        'username': 'tester666',
        'password': 'tester666',
        'nickname': 'tester666',
    },
    'HDU': {
        'username': 'sduwhvj',
        'password': 'sduwhvj2016',
        'nickname': 'sduwhvj',
    },
    'SDUT': {
        'username': 'sduwhvj1',
        'password': 'sduwhvj1',
        'nickname': 'sduwhvj',
    },
    'VJudge_list': [
        # {
        #     'username': 'sduwhvj',
        #     'password': 'sduwhvj2016',
        #     'nickname': 'sduwhvj',
        # },
        # {
        #     'username': 'sduwhvj2018',
        #     'password': 'sduwhvj2018',
        #     'nickname': 'sduwhvj2018',
        # },
        # {
        #     'username': 'sduwhvjtest',
        #     'password': 'sduwhvjtest',
        #     'nickname': 'sduwhvjtest',
        # },
        {
            'username': 'sduwhvj0',
            'password': 'sduwhvj0',
            'nickname': 'sduwhvj0',
        },
        {
            'username': 'sduwhvj1',
            'password': 'sduwhvj1',
            'nickname': 'sduwhvj1',
        },
        {
            'username': 'sduwhvj2',
            'password': 'sduwhvj2',
            'nickname': 'sduwhvj2',
        },
        {
            'username': 'sduwhvj3',
            'password': 'sduwhvj3',
            'nickname': 'sduwhvj3',
        },
        {
            'username': 'sduwhvj4',
            'password': 'sduwhvj4',
            'nickname': 'sduwhvj4',
        },
        {
            'username': 'sduwhvj5',
            'password': 'sduwhvj5',
            'nickname': 'sduwhvj5',
        },
        {
            'username': 'sduwhvj6',
            'password': 'sduwhvj6',
            'nickname': 'sduwhvj6',
        },
        {
            'username': 'sduwhvj7',
            'password': 'sduwhvj7',
            'nickname': 'sduwhvj7',
        },
        {
            'username': 'sduwhvj8',
            'password': 'sduwhvj8',
            'nickname': 'sduwhvj8',
        },
        {
            'username': 'sduwhvj9',
            'password': 'sduwhvj9',
            'nickname': 'sduwhvj9',
        },
    ]
}

# scylla 代理
scylla_proxy = {'http': '{}:8081'.format(host)}

# 全局代理
proxy = None

# headers
headers = {
    'connection': 'close',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'cache-control': 'no-cache',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Mobile Safari/537.36',
}
