"""Spider 全局配置"""
from os import environ

# HOST 地址
if environ.get('ENV') == 'DEV':
    host = 'davidz.cn'
else:
    host = "localhost"

# 数据库地址
dbhost = "mongodb://{}:27017/".format(host)

# 数据库名
dbname = "vj"

# 超时重试
timeout = 3  # s
