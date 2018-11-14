"""Judger 全局配置"""

# host
host = "localhost"

# 数据库
dbhost = "mongodb://{}:27017/".format(host)

# 数据库名
dbname = "vj"

# 超时重试
timeout = 10 # s

# 页面访问间隔
time_interval = 0.5 # s

# scylla 代理
scylla_proxy = {'http': 'http://{}:8081'.format(host)}

# 账号信息
# 用于向OJ提交代码
accounts = {
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
}
