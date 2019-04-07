"""爬虫模块"""

import re
import threading
import time

import pymongo
import requests

import config
import support.HDU
import support.POJ
import support.SDUT

# Database
db = pymongo.MongoClient(config.dbhost)[config.dbname]


def crawl(oj, sid):
    """爬取一道题目并返回该题目的dict"""
    # 下载题目页面
    r = requests.get(oj.problem_url % sid, timeout=config.timeout)
    r.encoding = oj.encoding
    html = r.text
    # 创建题目dict
    problem = {
        "soj": oj.name,
        "sid": sid,
    }
    # 遍历regexp进行正则提取
    for key, reg in oj.regexp.items():
        match = re.findall(reg, html)
        if not match:
            problem[key] = ""
            # Source字段可以为空
            # if key == "source":
            # problem["source"] = ""
            # 其它字段只要没匹配到就直接返回None
            # else:
            # return None
        else:
            # 保存该字段的值
            problem[key] = match[0]
    # 将 timelimit memorylimit 从字符串转为整数
    problem["timelimit"] = int(problem["timelimit"])
    problem["memorylimit"] = int(problem["memorylimit"])
    # 替换description的相对地址为绝对地址
    problem["description"] = oj.replace_src(problem["description"])
    return problem


def process(oj):
    """爬取某oj所有题目并保存到数据库"""
    no_such_sid_times = 0
    sid = oj.minid
    while sid <= oj.maxid:
        try:
            # 调用函数爬取
            problem = crawl(oj, sid)
            # 没有抓取到
            if not problem:
                print("[NO MATCH] [SKIP] %s-%d" % (oj.name, sid))
                # 如果oj里该题已经被删除 就确保本地数据库也删掉该题
                db["problem"].delete_one({
                    "soj": oj.name,
                    "sid": sid,
                })
                sid += 1
                continue
        except ValueError:
            print("[ERROR] No such sid %s-%d" % (oj.name, sid))
            no_such_sid_times += 1
            if no_such_sid_times >= 100:
                print("[INFO] Continuous 100 problems from %s can not be crawled" % oj.name)
                break
            sid += 1
            continue
        except Exception as err:
            # 有任何未知错误发生（网络超时等）都进行retry
            print("[ERROR] [RETRY] %s-%d %s" % (oj.name, sid, err))
            # 每秒retry一次
            time.sleep(1)
            # 这里不执行 sid += 1 实现了retry
            continue
        # 如果题目在数据库中已经存在
        if db["problem"].find({
            "soj": oj.name,
            "sid": sid,
        }).count():
            # 不创建 只更新
            db["problem"].update_one({
                "soj": oj.name,
                "sid": sid,
            }, {
                "$set": problem,
            })
            print("[SUCCESS] [UPDATE] %s-%d %s" % (oj.name, sid, problem["title"]))
        else:
            # 创建新题目
            problem["totalsm"] = 0
            problem["totalac"] = 0
            db["problem"].insert_one(problem)
            print("[SUCCESS] [CREATE] %s-%d %s" % (oj.name, sid, problem["title"]))
        no_such_sid_times = 0
        # 下一题
        sid += 1


def process_with_threading():
    thread_pool = []
    thread_pool.append(threading.Thread(target=process, args=(support.HDU,)))
    thread_pool.append(threading.Thread(target=process, args=(support.POJ,)))
    thread_pool.append(threading.Thread(target=process, args=(support.SDUT,)))
    for t in thread_pool:
        t.start()
    for t in thread_pool:
        t.join()
    print("Finished")


if __name__ == "__main__":
    process_with_threading()
