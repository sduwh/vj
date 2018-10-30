"""判题模块"""
import time

import config
import pymongo
from config import get_proxy, delete_proxy, print_error, print_info
from support.VJudge import VJudge

client = pymongo.MongoClient(config.dbhost)
db = client[config.dbname]


def serve():
    """判题服务主循环
    执行流程：
    1. 从数据库中取出一条最早的result字段为Queueing的记录
    2. 根据它的soj调用不同的OJ类进行判题
    3. 用判题后得到的结果更新该记录
    4. 重复 1-3
    """
    retry = 0

    oj_virtual_judge = VJudge(
        config.account_list["VJudge"], config.timeout, config.time_interval,
        config.headers, config.proxy, db, config.print_error, config.print_info)
    while True:
        proxy = get_proxy()
        oj_virtual_judge.proxy = {"http": "http://{}".format(proxy)}
        try:
            oj_virtual_judge.login()
        except Exception as e:
            print_error("登录失败", e)
            delete_proxy(proxy)
        else:
            break

    while True:
        # 按照FIFO的顺序从数据库读取一条待测评记录
        sub = db["submission"].find_one({
            "result": "Queueing"
        }, sort=[
            ("submittime", 1),
        ])
        if not sub:
            # 如果数据库中没有待测评记录
            # 等待3秒后继续尝试读取
            time.sleep(3)
            continue
        print_info("新任务 _id: %s" % sub['_id'])
        proxy = get_proxy()
        oj_virtual_judge.proxy = {"http": "http://{}".format(proxy)}
        try:
            sub["runid"], sub["result"], sub["timeused"], sub["memoryused"], sub["errorinfo"] = \
                oj_virtual_judge.judge(
                    sub['soj'], sub["sid"], sub["language"], sub["code"])

        except Exception as e:
            # 未知错误
            print_error("未知错误", e)
            delete_proxy(proxy)
            retry += 1
            time.sleep(3)
            if retry == 3:
                sub["result"] = "Unknown Error"
                _id = sub.pop("_id")
                db["submission"].update_one({
                    "_id": _id,
                }, {
                    "$set": sub,
                })
                retry = 0
        else:
            _id = sub.pop("_id")
            # 更新判题结果到数据库
            db["submission"].update_one({
                "_id": _id,
            }, {
                "$set": sub,
            })
            retry = 0
        time.sleep(3)


def main():
    serve()


if __name__ == "__main__":
    main()
