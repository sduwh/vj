import datetime
import functools

from tornado import gen
from tornado.web import RequestHandler


class Handler(RequestHandler):
    """
    VJ 成长记录 API
    # """

    @gen.coroutine
    def get(self):
        params = self._get_params()
        username = self._get_cookie_username()
        user = yield self._find_user_info(username)
        self.contest_id_list = yield self._get_contest_id_list(username)
        if params['type'] == 'index':
            self.write({
                'username': user.get('username'),
                'nickname': user.get('nickname'),
                'registration_time': (user.get('_id').generation_time.timestamp() * 1000),
                'total_sub': user.get('total_sub'),
                'total_ac': user.get('total_ac'),
                'total_wa': user.get('total_wa'),
                # 处理last_submit_time为None的情况
                'last_submit_time': user.get('last_submit_time').timestamp() * 1000
                if user.get('last_submit_time') else None,
            })
        elif params['type'] == 'others':
            self.write({
                'rank': (yield self._get_rank(user)),
                'first_ac': (yield self._get_first_ac(username)),
                'last_ac': (yield self._get_last_ac(username)),
                'diffiult_ac': (yield self._get_difficult_ac(username)),
                'achievement': (yield self._get_achievement(username)),
                'contest_list': (yield self._get_contest_list(username)),
            })
        else:
            self.send_error(500)

    @gen.coroutine
    def _find_user_info(self, username):
        user = yield self.settings["database"]["user"].find_one({
            "username": username,
        })
        return user

    @gen.coroutine
    def _get_rank(self, user):
        """
        :param user:
        :return:
        "rank": {
            "my_rank": "",
            "other_person": {
                "first": {
                    "nickname": "",
                    "total_ac": ""
                },
                "last": {
                    "nickname": "",
                    "total_ac": ""
                },
                "prve": {
                    "nickname": "",
                    "total_ac": ""
                },
                "next": {
                    "nickname": "",
                    "total_ac": ""
                }
            }
        }
        """
        ret = {}
        my_rank = user.get('rank')
        ret['my_rank'] = my_rank

        other_person = {}

        first = {}
        first_user = yield self.settings["database"]["user"].find_one({
            "rank": 1,
        })
        first['nickname'] = first_user.get('nickname')
        first['total_ac'] = first_user.get('total_ac')

        last = {}
        last_user = yield self.settings["database"]["user"].find_one(sort=[('rank', -1)])
        last['nickname'] = last_user.get('nickname')
        last['total_ac'] = last_user.get('total_ac')

        # my_rank为None, 1, last_user_rank时处理
        if not my_rank:
            my_rank = last_user.get('rank') + 1
        prve = {}
        if my_rank != 1:
            prve_user = yield self.settings["database"]["user"].find_one({
                "rank": my_rank - 1,
            })
            prve['nickname'] = prve_user.get('nickname')
            prve['total_ac'] = prve_user.get('total_ac')

        next = {}
        if my_rank < last_user.get('rank'):
            next_user = yield self.settings["database"]["user"].find_one({
                "rank": my_rank + 1,
            })
            next['nickname'] = next_user.get('nickname')
            next['total_ac'] = next_user.get('total_ac')

        other_person['first'] = first
        other_person['last'] = last
        other_person['prve'] = prve
        other_person['next'] = next
        ret['other_person'] = other_person
        return ret

    @gen.coroutine
    def _get_first_ac(self, username):
        """
        :param username:
        :return:
        "first_ac": {
            "time": "",
            "title": "",
            "url": "",
            "code": ""
        }
        """
        ret = {}
        first_ac = yield self.settings['database']['submission'].find_one(
            {
                'username': username,
                'result': 'Accepted'
            }, sort=[('submittime', 1)]
        )
        if first_ac:
            soj = first_ac['soj']
            sid = first_ac['sid']
            submission_id = first_ac.get('_id')
            problem = yield self.settings['database']['problem'].find_one({'soj': soj, 'sid': sid})
            title = ' {}'.format(problem.get('title')) if problem else ''
            title = '{}-{}{}'.format(soj, sid, title)

            ret['time'] = first_ac.get('submittime').strftime('%Y %m %d') if first_ac.get('submittime') else None
            ret['title'] = title
            ret['url'] = '/submission/{}'.format(submission_id) if submission_id else None
            ret['code'] = first_ac.get('code')

        return ret

    @gen.coroutine
    def _get_last_ac(self, username):
        """
        :param username:
        :return:
        "last_ac": {
            "time": "",
            "title": "",
            "url": "",
            "code": ""
        }
        """
        ret = {}
        last_ac = yield self.settings['database']['submission'].find_one(
            {
                'username': username,
                'result': 'Accepted'
            }, sort=[('submittime', -1)]
        )
        if last_ac:
            soj = last_ac['soj']
            sid = last_ac['sid']
            submission_id = last_ac.get('_id')
            problem = yield self.settings['database']['problem'].find_one({'soj': soj, 'sid': sid})
            title = ' {}'.format(problem.get('title')) if problem else ''
            title = '{}-{}{}'.format(soj, sid, title)

            ret['time'] = last_ac.get('submittime').strftime('%Y %m %d') if last_ac.get('submittime') else None
            ret['title'] = title
            ret['url'] = '/submission/{}'.format(submission_id) if submission_id else None
            ret['code'] = last_ac.get('code')

        return ret

    @gen.coroutine
    def _get_difficult_ac(self, username):
        """
        :param username:
        :return:
        "diffiult_ac": {
            "none_ac_cnt": "",
            "time": "",
            "title": "",
            "url": "",
            "code": ""
        }
        """
        ret = {}
        none_ac_submits = yield self.settings['database']['submission'].find(
            {
                'username': username,
                'result': {'$ne': 'Accepted'}
            }, sort=[('submittime', 1)]
        ).to_list(None)
        if none_ac_submits:
            counter = {}
            for none_ac_submit in none_ac_submits:
                key = (none_ac_submit['soj'], none_ac_submit['sid'])
                if not counter.get(key):
                    counter[key] = 1
                else:
                    counter[key] += 1

            max_none_ac_key = max(counter, key=lambda k: counter[k])
            soj = max_none_ac_key[0]
            sid = max_none_ac_key[1]

            difficult_ac = yield self.settings['database']['submission'].find_one(
                {
                    'username': username,
                    'result': 'Accepted',
                    'soj': soj,
                    'sid': sid
                }, sort=[('submittime', 1)]
            )
            if difficult_ac:
                submission_id = difficult_ac.get('_id')
                problem = yield self.settings['database']['problem'].find_one({'soj': soj, 'sid': sid})
                title = ' {}'.format(problem.get('title')) if problem else ''
                title = '{}-{}{}'.format(soj, sid, title)

                ret['none_ac_cnt'] = counter[max_none_ac_key]
                ret['time'] = difficult_ac.get('submittime').strftime('%Y %m %d') if difficult_ac.get(
                    'submittime') else None
                ret['title'] = title
                ret['url'] = '/submission/{}'.format(submission_id) if submission_id else None
                ret['code'] = difficult_ac.get('code')

        return ret

    @gen.coroutine
    def _get_achievement(self, username):
        """
        :param username:
        :return:
        "achievement": {
            "first_ac": "boolean",
            "first_wa": "boolean",
            "continuous_ac_cnt": "",
            "continuous_none_ac_cnt": "",
            "once_ac_cnt": "",
            "once_wa_cnt": "",
            "festival": {
                "valentine": "boolean",
                "newyear": "boolean",
                "single": "boolean"
            },
            "contest": {
                "is_first": "boolean",
                "is_last": "boolean"
            }
        }
        """
        ret = {}
        #
        first_ac = yield self.settings['database']['submission'].find_one(
            {
                'username': username,
                'result': 'Accepted'
            }, sort=[('submittime', 1)]
        )
        ret['first_ac'] = True if first_ac else False
        #
        first_wa = yield self.settings['database']['submission'].find_one(
            {
                'username': username,
                'result': 'Accepted'
            }, sort=[('submittime', 1)]
        )
        ret['first_wa'] = True if first_wa else False
        #
        submissions = yield self.settings['database']['submission'].find(
            {
                'username': username,
            }, sort=[('submittime', 1)]
        ).to_list(None)
        # TODO: 有一个小bug
        result = ''
        max_ac_cnt = 0
        max_none_ac_cnt = 0
        ac_cnt = 0
        none_ac_cnt = 0
        for submit in submissions:
            if submit['result'] == 'Accepted' and result == 'Accepted':
                ac_cnt += 1
            elif submit['result'] != 'Accepted' and result != 'Accepted':
                none_ac_cnt += 1
            elif submit['result'] == 'Accepted':
                max_none_ac_cnt = max(max_none_ac_cnt, none_ac_cnt)
                none_ac_cnt = 0
            elif submit['result'] != 'Accepted':
                max_ac_cnt = max(max_ac_cnt, ac_cnt)
                ac_cnt = 0
            result = submit['result']
        ret['continuous_ac_cnt'] = max_ac_cnt
        ret['continuous_none_ac_cnt'] = max_none_ac_cnt
        #
        counter = {}
        once_ac_cnt = 0
        once_wa_cnt = 0
        for submit in submissions:
            key = (submit['soj'], submit['sid'])
            if not counter.get(key):
                if submit['result'] == 'Accepted':
                    once_ac_cnt += 1
                elif submit['result'] == 'Wrong Answer':
                    once_wa_cnt += 1
            counter[key] = 1
        ret['once_ac_cnt'] = once_ac_cnt
        ret['once_wa_cnt'] = once_wa_cnt
        #
        valentine = False
        newyear = False
        single = False
        for submit in submissions:
            submittime = submit['submittime']
            # 情人节:2月14日
            if submittime.month == 2 and submittime.day == 14:
                valentine = True
            # 元旦:1月1日
            if submittime.month == 1 and submittime.day == 1:
                newyear = True
            # 光棍节:11月11日
            if submittime.month == 11 and submittime.day == 11:
                single = True
        festival = {
                       "valentine": valentine,
                       "newyear": newyear,
                       "single": single
                   },
        ret['festival'] = festival
        #
        is_first = False
        is_last = False
        for contest_id in self.contest_id_list:
            contest = yield self.settings['database']['contest'].find_one({'_id': contest_id})
            rank = self._make_rank(contest, (yield self._find_submissions(contest_id)))
            if rank:
                if rank[0]['username'] == username:
                    is_first = True
                    break
                if rank[-1]['username'] == username and rank[1]:
                    is_last = True
                    break

        contest = {
            "is_first": is_first,
            "is_last": is_last
        }
        ret['contest'] = contest

        return ret

    @gen.coroutine
    def _get_contest_list(self, username):
        """
        :param username:
        :return:
        "contest_list": [
            {
                "title": "",
                "url": "",
                "time": "",
                "description": ""
            },
            {
                "title": "",
                "url": "",
                "time": "",
                "description": ""
            }
        ]
        """
        # 你给我的比赛数据，要是根据比赛时间由近到远排序的，因为我们要优先展示最近的比赛
        contest_list = []
        for contest_id in self.contest_id_list:
            contest = yield self.settings['database']['contest'].find_one({'_id': contest_id})
            contest_rank = self._make_rank(contest, (yield self._find_submissions(contest_id)))
            rank = 1
            for t in contest_rank:
                if t['username'] == username:
                    break
                rank += 1
            contest_list.append({
                'title': contest.get('title'),
                'url': '/contest/entry/{}'.format(str(contest.get('_id'))),
                'time': '{} ~ {}'.format(contest.get('begintime').strftime('%Y-%m-%d %H:%M:%S'),
                                         contest.get('endtime').strftime('%Y-%m-%d %H:%M:%S')),
                'description': contest.get('description'),
                'rank': rank
            })
        ret = sorted(contest_list, key=lambda d:d['time'], reverse=True)
        return ret

    @gen.coroutine
    def _get_contest_id_list(self, username):
        """
        获得一个用户的contest_id_set
        :param username:
        :return: contest_id_set
        """
        contest_id_set = set()
        submissions = yield self.settings['database']['submission'].find(
            {
                'username': username,
            }, sort=[('submittime', 1)]
        ).to_list(None)
        for contest in submissions:
            contest_id = contest.get('contest_id')
            if contest_id:
                # contest 不全
                if (yield self.settings['database']['contest'].count({'_id': contest_id})):
                    contest_id_set.add(contest_id)
        return list(contest_id_set)

    @gen.coroutine
    def _find_submissions(self, _id):
        """
        找到对应的提交记录
        :param _id: contest_id
        :return: submissions
        """
        submissions = yield self.settings["database"]["submission"].find({
            "contest_id": _id,
        }, {
            "username": 1, "nickname": 1, "result": 1, "submittime": 1, "n": 1,
        }).to_list(None)
        return submissions

    def _make_rank(self, contest, submissions):
        """
        获得一次比赛的排名
        :param contest: 比赛
        :param submissions: 比赛的提交
        :return: rank 排名
        """
        rank = {}

        # 遍历submissions
        # 统计数据
        for sub in submissions:
            # 如果用户不在rank表中 先创建一份该用户的初始值到rank表
            if not rank.get(sub["username"]):
                # rank表key为username value为与该用户相关的提交数据
                rank[sub["username"]] = {
                    "username": sub["username"],
                    "nickname": sub["nickname"],
                    "problems": [],
                    "penalty": datetime.timedelta(),
                    "accepted": 0,
                    "total": 0,
                }
                # rank表中每个用户都有一个problems数组
                # 长度为本次比赛题目数量
                # 第n项代表该用户针对第n题的相关提交数据统计
                for _ in contest["problems"]:
                    rank[sub["username"]]["problems"].append({
                        "error": 0,  # 错误次数
                        "first_accepted_time": None,  # 本人首次ac时间
                        "winner": False,  # 所有人中第一个解答出该题的
                    })
            # 如果本次提交ac
            if sub["result"] == "Accepted":
                # 如果这道题尚未ac 记录首次ac时间 设置accepted为True
                if None == rank[sub["username"]]["problems"][sub["n"]]["first_accepted_time"]:
                    rank[sub["username"]]["problems"][sub["n"]]["first_accepted_time"] = sub["submittime"] - contest[
                        "begintime"]
            else:
                # 只有这道题尚未ac的时候才算入错误数
                if None == rank[sub["username"]]["problems"][sub["n"]]["first_accepted_time"]:
                    # 错误次数+1
                    rank[sub["username"]]["problems"][sub["n"]]["error"] += 1

        # 遍历rank
        # 计算总提交数、罚时等数据
        for user in rank.keys():
            # 遍历该用户的所有题目
            for pro in rank[user]["problems"]:
                # 总提交数加上该题的错误提交数
                rank[user]["total"] += pro["error"]
                # 如果该题ac
                if None != pro["first_accepted_time"]:
                    # 总ac数和总提交数分别+1
                    rank[user]["accepted"] += 1
                    rank[user]["total"] += 1
                    # 总罚时加上 该题首次被提交的时间+该题错误数乘20分钟
                    rank[user]["penalty"] += pro["first_accepted_time"] + pro["error"] * datetime.timedelta(minutes=20)

        # 计算每道题第一个解答出的人
        for n in range(len(contest["problems"])):
            winner = None
            for user in rank.keys():
                if winner == None:
                    if None != rank[user]["problems"][n]["first_accepted_time"]:
                        winner = user
                    continue
                if None != rank[user]["problems"][n]["first_accepted_time"]:
                    if rank[user]["problems"][n]["first_accepted_time"] < rank[winner]["problems"][n][
                        "first_accepted_time"]:
                        winner = user
            if None != winner:
                rank[winner]["problems"][n]["winner"] = True

        def cmp(x, y):
            if x["accepted"] > y["accepted"]:
                return 1
            elif x["accepted"] < y["accepted"]:
                return -1
            else:
                if x["penalty"] > y["penalty"]:
                    return -1
                elif x["penalty"] < y["penalty"]:
                    return 1
                else:
                    return 0

        return sorted(rank.values(), key=functools.cmp_to_key(cmp), reverse=True)

    def _get_cookie_username(self):
        username = self.get_secure_cookie("username")
        return username.decode()

    def _get_params(self):
        params = {}
        params["type"] = self.get_argument("type", default="")
        return params
