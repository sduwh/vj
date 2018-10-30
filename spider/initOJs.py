'''初始化 oj '''
import json

import config
import pymongo
import requests
from config import print_error, print_info


def init_remote_ojs():
    '''从 https://vjudge.net/util/remoteOJs 获得所有支持的 oj 方式'''
    try:
        response = requests.get(url=config.remote_oj_url,
                                proxies=config.proxy, timeout=config.timeout)
    except Exception as e:
        print_error("获得远程 oj 时 requests 出错", e)
        exit(1)
    remote = json.loads(response.text)
    print_info("开始初始化 oj")
    try:
        save_oj_to_db(remote)
    except Exception as e:
        print_error("获得远程 oj 时 pymongodb 出错", e)


def save_oj_to_db(remote):
    '''保存 oj 到数据库'''
    # 链接数据库
    with pymongo.MongoClient(config.dbhost) as client:
        db = client[config.dbname]
        for oj_name in remote:
            print_info("开始处理 oj: %s" % oj_name)
            # 检查数据库中支持的 OJ
            if not db["OJ"].find({"soj": oj_name}).count():
                db["OJ"].insert({"soj": oj_name})
                print_info("添加 oj %s" % oj_name)
            for key, value in remote[oj_name].get("languages").items():
                if db["remoteOJs"].find({
                    "soj": oj_name,
                    "language": key,
                    "remote": value
                }).count():
                    # 不添加 只更新
                    db["remoteOJs"].update_one({
                        "soj": oj_name,
                        "language": key,
                        "remote": value
                    }, {"$set": {
                        "soj": oj_name,
                        "language": key,
                        "remote": value
                    }})
                    print_info("更新 %s 方法 %s: %s" % (oj_name, key, value))
                else:
                    # 添加
                    db["remoteOJs"].insert({
                        "soj": oj_name,
                        "language": key,
                        "remote": value
                    })
                    print_info("添加 %s 方法 %s: %s" % (oj_name, key, value))


def main():
    init_remote_ojs()


if __name__ == '__main__':
    main()
