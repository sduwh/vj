"""Web 全局配置"""
from os import environ

# 数据库Host
if environ.get('ENV') == 'DEV':
    host = 'davidz.cn'
else:
    host = "localhost"

# Web服务端口
port = 8000

# 数据库地址
dbhost = "mongodb://{}:27017/".format(host)

# 数据库名
dbname = "vj"

# 静态文件目录
static_path = "./static"

# 模板文件目录
template_path = "./templates"

# Problem/Submisson/Contest/...每页显示的记录数
rows_per_page = 50
