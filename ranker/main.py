"""排名模块"""
import pymongo
import threading

# mongodb host
host = "localhost"

vj = pymongo.MongoClient(host=host, port=27017)['vj']


def match_info(start, num):
    """
    获得每个用户的total_sub, total_ac，total_wa，last_submit_time(保证兼容)
    :param start: 开始处理的id号
    :param num: 每次处理的个数
    :return: None
    """
    users = vj['user'].find().skip(start).limit(num)
    cnt = 1
    for user in users:
        username = user['username']
        try:
            total_sub = vj['submission'].count({'username': username})

            total_ac_submit = vj['submission'].find({'username': username, 'result': 'Accepted'})
            total_ac_submit_set = set()
            for ac_submit in total_ac_submit:
                total_ac_submit_set.add("{} {}".format(ac_submit['soj'], str(ac_submit['sid'])))
            total_ac = len(total_ac_submit_set)

            total_wa = vj['submission'].find({'username': username, 'result': 'Wrong Answer'}).count()

            try:
                last_submit_time = vj['submission'].find_one({'username': username}, sort=[('submittime', -1)])[
                    'submittime']
            except:
                total_sub = 0
                total_ac = 0
                total_wa = 0
                last_submit_time = None
            print("{} {} {} {} {} {}/{}".format(username, total_sub, total_ac, total_wa, last_submit_time, cnt, num))

            if user['username'] == '201700800423何雨辰':
                total_sub = 99999
                total_ac = 0
                total_wa = 99999

            cnt += 1
            vj['user'].find_and_modify(
                {'username': username},
                {'$set': {
                    'total_sub': total_sub,
                    'total_ac': total_ac,
                    'total_wa': total_wa,
                    'last_submit_time': last_submit_time
                }})

        except Exception as e:
            print('{}\n{}'.format(username, e))

def match_info_multithreading():
    start = 0
    num = 100
    total = vj['user'].count()
    while start < total:
        th = threading.Thread(target=match_info, args=(start, num))
        th.start()
        start += num

def rank():
    """
    排序，按照total_ac 降序，last_submit_time 降序(保证唯一)
    注意：需要数据库建立索引 {"total_ac": -1}
    :return:None
    """
    users = vj['user'].find().sort([('total_ac', -1), ('last_submit_time', -1)])
    cnt = 1
    for user in users:
        print(cnt, user.get('total_ac'), user.get('last_submit_time'))
        vj['user'].find_and_modify({'_id': user['_id']}, {'$set': {'rank': cnt}})
        cnt += 1

def main():
    match_info_multithreading()
    rank()

if __name__ == '__main__':
    main()
