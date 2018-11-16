import datetime
import functools

from tornado.web import RequestHandler
from tornado import gen
from bson.objectid import ObjectId

class Handler(RequestHandler):
    @gen.coroutine
    def get(self, _id):
        """比赛排名"""
        try:
            contest = yield self._find_contest(_id)
            if contest["password"]:
                self._check_permission(_id)
            submissions = yield self._find_submissions(_id)
            rank = self._make_rank(contest, submissions)
        except RuntimeError as err:
            self.render("message.html", text=str(err))
        else:
            self.render("contest/rank.html", contest=contest, rank=rank)

    # temp
    def _get_cookie_username(self):
        username = self.get_secure_cookie("username")
        if not username:
            return None
        return username.decode()

    @gen.coroutine
    def _find_contest(self, _id):
        contest = yield self.settings["database"]["contest"].find_one({
            "_id": ObjectId(_id),
        })
        if not contest:
            raise RuntimeError("No record")
        return contest

    def _check_permission(self, _id):
        contest_id = self.get_secure_cookie("contest")
        if not contest_id or _id != contest_id.decode():
            raise RuntimeError("Please enter password")

    @gen.coroutine
    def _find_submissions(self, _id):
        submissions = yield self.settings["database"]["submission"].find({
            "contest_id": ObjectId(_id),
        }, {
            "username": 1, "nickname": 1, "result": 1, "submittime": 1, "n": 1,
        }).to_list(None)
        return submissions

    def _make_rank(self, contest, submissions):
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
                        "error": 0, # 错误次数
                        "first_accepted_time": None, # 本人首次ac时间
                        "winner": False, # 所有人中第一个解答出该题的
                    })
            # 如果本次提交ac
            if sub["result"] == "Accepted":
                # 如果这道题尚未ac 记录首次ac时间 设置accepted为True
                if None == rank[sub["username"]]["problems"][sub["n"]]["first_accepted_time"]:
                    rank[sub["username"]]["problems"][sub["n"]]["first_accepted_time"] = sub["submittime"] - contest["begintime"]
            if sub["result"] == "Compilation Error" or sub["result"] == "Compile Error":
                continue
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
                    if rank[user]["problems"][n]["first_accepted_time"] < rank[winner]["problems"][n]["first_accepted_time"]:
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
