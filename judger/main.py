"""判题模块"""
import time

import pymongo

import config
import support
import support.POJ
import support.HDU
# import support.SDUT

db = pymongo.MongoClient(config.dbhost)[config.dbname]


def serve():
    """判题服务主循环
    执行流程：
    1. 从数据库中取出一条最早的result字段为Queueing的记录
    2. 根据它的soj调用不同的OJ类进行判题
    3. 用判题后得到的结果更新该记录
    4. 重复 1-3
    """
    retry = 0
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
        print("New task")


        try:
            # oj dispatcher
            ojclass = {
                # str => class
                "POJ": support.POJ.Runner,
                "HDU": support.HDU.Runner,
                # "SDUT": support.SDUT.Runner,
            }[sub["soj"]]
            sub["runid"], sub["result"], sub["timeused"], sub["memoryused"], sub["errorinfo"] = \
                ojclass(config.accounts[sub["soj"]], config.timeout, config.time_interval, config.scylla_proxy).judge(
                    sub["sid"],
                    sub["language"],
                    sub["code"])
        except Exception as err:
            # 未知错误
            print("Unknown error: %s" % err)
            retry += 1
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


def main():
    serve()


if __name__ == "__main__":
    main()
