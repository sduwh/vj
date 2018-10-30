import datetime

from bson.objectid import ObjectId
from tornado import gen
from tornado.web import RequestHandler


class Handler(RequestHandler):
    @gen.coroutine
    def post(self, _id):
        """提交代码"""
        try:
            # if self.request.remote_ip != "219.231.164.200":
            #    raise RuntimeError("请勿在外部提交")
            contest = yield self._find_contest(_id)
            if contest["password"]:
                self._check_permission(_id)
            self._check_time(contest["begintime"], contest["endtime"])
            cookies = self._get_cookies()
            yield self._check_submit_frequency(_id, cookies["username"])
            params = self._get_params()
            problem = contest["problems"][params["n"]]
            yield self._add_submission(_id, cookies, params, problem)
        except RuntimeError as err:
            self.render("message.html", text=str(err))
        else:
            self.redirect("/contest/submission/" + _id)

    get = post

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

    def _check_time(self, begintime, endtime):
        now = datetime.datetime.now()
        if now < begintime or now > endtime:
            raise RuntimeError("Contest is not running")

    @gen.coroutine
    def _check_submit_frequency(self, contest_id, username):
        last_sm = yield self.settings["database"]["submission"].find_one({
            "username": username, "contest_id": ObjectId(contest_id),
        }, sort=[
            ("submittime", -1),
        ])
        if not last_sm:
            return
        now = datetime.datetime.now().timestamp()
        last = last_sm["submittime"].timestamp()
        if now - last < 10:
            raise RuntimeError("Please wait for at least 10s")

    def _get_cookies(self):
        cookies = {}
        cookies["username"] = self.get_secure_cookie("username")
        cookies["nickname"] = self.get_secure_cookie("nickname")
        for k, v in cookies.items():
            if not v:
                raise RuntimeError("Please login")
            cookies[k] = cookies[k].decode()
        return cookies

    def _get_params(self):
        params = {}
        try:
            params["n"] = int(self.get_argument("n", default=""))
        except ValueError:
            raise RuntimeError("Not valid 'n'")
        params["code"] = self.get_argument("code", default="")
        params["language"] = self.get_argument("language", default="")
        # n可以为0 因此这里不能用for来遍历判断所有值
        if not params["code"] or not params["language"]:
            raise RuntimeError("Empty item")
        if len(params["code"]) < 5:
            raise RuntimeError("Code too short")
        return params

    @gen.coroutine
    def _add_submission(self, contest_id, cookies, params, problem):
        # code = base64.b64decode(params["code"]).decode()
        code = params["code"]
        r = yield self.settings["database"]["submission"].insert_one({
            # Contest
            "contest_id": ObjectId(contest_id),
            # User
            "username": cookies["username"],
            "nickname": cookies["nickname"],
            "ip": self.request.remote_ip,
            # Problem
            "n": params["n"],
            "soj": problem["soj"],
            "sid": problem["sid"],
            # Request
            "code": code,
            "codesize": len(code),
            "language": params["language"],
            # Response
            "runid": 0,
            "result": "Queueing",
            "timeused": 0,
            "memoryused": 0,
            "submittime": datetime.datetime.now(),
            "errorinfo": "",
        })
        if not r.acknowledged:
            raise RuntimeError("Create submission error")
