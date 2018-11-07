"""排名模块"""
import pymongo
import threading

# mongodb host
host = "localhost"

vj = pymongo.MongoClient(host=host, port=27017)['vj']


def process(start, num):
    user_all = vj['user'].find().skip(start).limit(num)
    cnt = 1
    for user in user_all:
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


def main():
    start = 0
    num = 100
    total = vj['user'].count()
    while start < total:
        th = threading.Thread(target=process, args=(start, num))
        th.start()
        start += num


if __name__ == '__main__':
    main()
