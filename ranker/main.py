"""排名模块"""
import pymongo

# mongodb host
host = "localhost"

vj = pymongo.MongoClient(host=host, port=27017)['vj']


def process(user_all):
    total = user_all.count()
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
            try:
                last_submit_time = vj['submission'].find_one({'username': username}, sort=[('submittime', -1)])[
                    'submittime']
            except:
                total_sub = 0
                total_ac = 0
                last_submit_time = None
            print("{} {} {} {} {}/{}".format(username, total_sub, total_ac, last_submit_time, cnt, total))
            cnt += 1
            vj['user'].find_and_modify(
                {'username': username},
                {'$set': {
                    'total_sub': total_sub,
                    'total_ac': total_ac,
                    'last_submit_time': last_submit_time
                }})

        except Exception as e:
            print('{}\n{}'.format(username, e))


def main():
    user_all = vj['user'].find()
    process(user_all)


if __name__ == '__main__':
    main()
