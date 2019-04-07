# OJ配置 示例
#
# OJ名字
# name = "XXX"
#
# 题目地址 用 %d 占位
# problem_url = "http://example.com/problem?id=%d"
#
# 网页编码
# encoding = "gbk"
#
# 最小id
# minid = 1000
#
# 最大id
# maxid = 2333
#
# 正则集
# 用于提取网页中的数据
# 被提取的数据用圆括号圈出
# 每一项都不可缺少
# regexp = {
#     "title": r'<title>(.+?)</title>',
#     "timelimit": r'<timelimit>(\d+?)</timelimit>',
#     "memorylimit": r'<memorylimit>(\d+?)</memorylimit>',
#     "description": r'<description>([.\s\S]+?)</description>',
#     "input": r'<input>([.\s\S]+?)</input>',
#     "output": r'<output>([.\s\S]+?)</output>',
#     "sampleinput": r'<sampleinput>([.\s\S]+?)</sampleinput>',
#     "sampleoutput": r'<sampleoutput>([.\s\S]+?)</sampleoutput>',
# }
#
# 将爬取到的description中图片的相对地址替换为绝对地址
# 参数 替换前的数据
# 返回 替换后的数据
# def replace_src(description):
#     # Do replace
#     return description