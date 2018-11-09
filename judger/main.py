"""判题模块"""
"""从数据库中找到所有Queueing的记录
全部取出并且每一个记录用一个线程处理
每个线程对应一个VJudge.judge
vjudge的验证码策略是一个用户4分钟内不得提交超过5个题目
"""
import time
import datetime
import threading

import pymongo

import config
from support.VJudge import VJudge, log

db = pymongo.MongoClient(config.dbhost)[config.dbname]
account_list = config.account_list['VJudge_list']


def serve():
    # 初始化最后一次提交时间，用于比较
    last_submit_time = datetime.datetime(1970, 1, 1)

    # 初始化用户列表
    for account in account_list:
        account['last_submit_time'] = last_submit_time
        account['submit_count'] = 0

    # 主循环
    account_no = 0
    while True:
        # 按照FIFO的顺序从数据库读取一条待测评记录
        sub = db['submission'].find_one({'result': {'$in': ['Queueing', 'Submit Failed']}, 'submittime': {'$gt': last_submit_time}},
                                        sort=[('submittime', 1)])
        if not sub:
            # 如果数据库中没有待测评记录
            time.sleep(config.time_interval)
            continue
        else:
            if account_list[account_no]['submit_count'] == 5:
                account_list[account_no]['submit_count'] = 0
                account_no = account_no + 1
                if account_no >= len(account_list):
                    account_no = account_no - len(account_list)
                    datetime_delta = datetime.datetime.now() - account_list[account_no]['last_submit_time']
                    if datetime_delta < datetime.timedelta(minutes=5):
                        log('等待中，避免验证码')
                        time.sleep(datetime_delta.total_seconds())
            else:
                account = account_list[account_no]
                account['submit_count'] += 1
                account['last_submit_time'] = datetime.datetime.now()
                last_submit_time = sub['submittime']
                th = threading.Thread(target=submit_target, args=(account, sub))
                th.start()


def submit_target(account, sub):
    # 提交判题
    vj = VJudge(account, config.timeout, config.time_interval, config.headers,
                config.proxy, config.host)
    # 先获得一个代理ip
    vj.proxy_ip = vj._get_proxy_ip()
    sub['runid'], sub['result'], sub['timeused'], sub['memoryused'], sub['errorinfo'] \
        = vj.judge(sub['soj'], sub['sid'], sub['language'], sub['code'])

    # 更新判题结果到数据库
    _id = sub.pop('_id')
    db['submission'].update_one({'_id': _id}, {'$set': sub})


def main():
    serve()


if __name__ == "__main__":
    main()
