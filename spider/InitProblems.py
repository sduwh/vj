'''初始化题库'''
import json
import re
import threading
import time

import config
import pymongo
import requests
from bs4 import BeautifulSoup as bs
from config import print_error, print_info, get_proxy, delete_proxy

# 链接数据库
client = pymongo.MongoClient(config.dbhost)
db = client[config.dbname]


def init_problems_multithreading():
    """使用多线程爬取某 oj 所有题目并保存到数据库"""
    for problem_list in get_problem_lists():
        t = threading.Thread(
            target=init_problems_from_problem_list, args=(problem_list,))
        t.start()


def init_problems_from_problem_list(problem_list):
    for problem in problem_list:
        if problem['allowSubmit'] and db["remoteOJs"].find({
            "soj": problem['originOJ'],
        }).count():
            _problem = {
                "title": problem['title'],
                "soj": problem['originOJ'],
                "sid": problem['originProb'],
                # 防止 source 为 None, Web 中正则过滤出错
                "source": problem.get('source') if problem.get('source') else "",
            }
            problem_id = problem['originOJ'] + '-' + problem['originProb']
            problem_detail_url = "https://vjudge.net/problem/" + problem_id
            response = get_problem_detail(problem_detail_url)
            try:
                problem_html = bs(response.text, 'lxml')
                problem_info = problem_html.find(
                    "div", id="prob-properties").find_all('dd')
                problem_info_title = problem_html.find(
                    "div", id="prob-properties").find_all('dt')
            except Exception as e:
                print_error("获取题目详细信息时 bs4 出错", e)
                continue
            try:
                targets = re.findall(
                    r'<dt class="col-sm-5">(.+?)</dt>', str(problem_info_title))
                ans = re.findall(
                    r'<dd class="col-sm-7">(.+?)</dd>', str(problem_info))
            except Exception as e:
                print_error("获取题目详细信息时 re 出错", e)
            else:
                for i in range(len(targets)):
                    if i < len(ans):
                        _problem[targets[i]] = ans[i]
            _problem['description_url'] = "https://vjudge.net" + \
                                          problem_html.iframe['src']
            save_problem(_problem)
        else:
            # 如果vj里该题已经不允许提交,确保本地数据库也删掉该题
            db["problem"].delete_one({
                "title": problem['title'],
                "soj": problem['originOJ'],
                "sid": problem['originProb'],
            })


def get_problem_lists():
    '''获得某 oj 的题目列表'''
    print_info("开始获取题目列表")
    index = 0
    for oj_name in config.oj_list:
        print_info("正在获取 %s oj 的题目列表" % oj_name)
        config.form_data['OJId'] = oj_name
        while True:
            config.form_data['start'] = str(index * config.problem_num_once)
            print_info("当前 oj: %s, 开始题号: %s" %
                       (oj_name, config.form_data['start']))
            proxy = get_proxy()
            proxies = {"http": "http://{}".format(proxy)}
            try:
                problem_response = requests.post(
                    url=config.problem_api_url, headers=config.headers, data=config.form_data, proxies=proxies,
                    timeout=config.timeout)
                problems_list = json.loads(problem_response.text)['data']
            except Exception as e:
                print_error("获取题目列表时 requests 出错", e)
                delete_proxy(proxy)
                time.sleep(config.timeout)
                continue
            if not len(problems_list):
                index = 0
                break
            yield problems_list
            index += 1
            time.sleep(config.timeout)


def get_problem_detail(detail_url):
    '''获得 detail_url 对应题目的 response'''
    while True:
        proxy = get_proxy()
        proxies = {"http": "http://{}".format(proxy)}
        try:
            response = requests.get(
                url=detail_url, proxies=proxies, timeout=config.timeout)
        except Exception as e:
            # 有任何未知错误发生（网络超时等）都进行retry
            print_error("获取题目详细信息时 requests 出错", e)
            delete_proxy(proxy)
            time.sleep(config.timeout)
            continue
        break
    return response


def save_problem(problem):
    '''保存 problem 到数据库'''
    # 如果题目在数据库中已经存在
    if db["problem"].find({
        "soj": problem['soj'],
        "sid": problem['sid'],
    }).count():
        # 不添加 只更新
        db["problem"].update_one({
            "soj": problem['soj'],
            "sid": problem['sid'],
        }, {
            "$set": problem,
        })
        print_info("更新 %s-%s %s" %
                   (problem['soj'], problem['sid'], problem["title"]))
    else:
        # 添加新题目
        problem["totalsm"] = 0
        problem["totalac"] = 0
        db["problem"].insert_one(problem)
        print_info("添加 %s-%s %s" %
                   (problem['soj'], problem['sid'], problem["title"]))


def main():
    init_problems_multithreading()
    client.close()


if __name__ == "__main__":
    main()

# def init_problems():
#     """爬取某 oj 所有题目并保存到数据库"""
#     for problem_list in get_problem_lists():
#         print_info("正在处理题目列表")
#         for problem in problem_list:
#             if problem['allowSubmit'] and db["remoteOJs"].find({
#                     "soj": problem['originOJ'],
#             }).count():
#                 _problem = {
#                     "title": problem['title'],
#                     "soj": problem['originOJ'],
#                     "sid": problem['originProb'],
#                     "source": problem.get('source'),
#                 }
#                 problem_id = problem['originOJ'] + '-' + problem['originProb']
#                 problem_detail_url = "https://vjudge.net/problem/" + problem_id
#                 response = get_problem_detail(problem_detail_url)
#                 try:
#                     problem_html = bs(response.text, 'lxml')
#                     problem_info = problem_html.find(
#                         "div", id="prob-properties").find_all('dd')
#                     problem_info_title = problem_html.find(
#                         "div", id="prob-properties").find_all('dt')
#                 except Exception as e:
#                     print_error("获取题目详细信息时 bs4 出错", e)
#                     continue
#                 try:
#                     targets = re.findall(
#                         r'<dt class="col-sm-5">(.+?)</dt>', str(problem_info_title))
#                     ans = re.findall(
#                         r'<dd class="col-sm-7">(.+?)</dd>', str(problem_info))
#                 except Exception as e:
#                     print_error("获取题目详细信息时 re 出错", e)
#                 else:
#                     for i in range(len(targets)):
#                         if i < len(ans):
#                             _problem[targets[i]] = ans[i]
#                 _problem['description_url'] = "https://vjudge.net" + \
#                     problem_html.iframe['src']
#                 save_problem(_problem)
#             else:
#                 # 如果vj里该题已经不允许提交,确保本地数据库也删掉该题
#                 db["problem"].delete_one({
#                     "title": problem['title'],
#                     "soj": problem['originOJ'],
#                     "sid": problem['originProb'],
#                 })
