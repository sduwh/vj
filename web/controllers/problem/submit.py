import datetime
import base64

from tornado.web import RequestHandler
from tornado import gen

class Handler(RequestHandler):
    @gen.coroutine
    def post(self):
        """代码提交"""
        try:
            cookies = self._get_cookies()
            params = self._get_params()
            yield self._check_submit_frequency(cookies["username"])
            yield self._add_submission(cookies, params)
        except RuntimeError as err:
            return self.render("message.html", text=str(err))
        else:
            self.redirect("/submission")

    get = head = options = delete = put = post

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
            params["sid"] = self.get_argument("sid", default="")
        except ValueError:
            raise RuntimeError("Not valid sid")
        params["soj"] = self.get_argument("soj", default="")
        params["code"] = self.get_argument("code", default="")
        params["language"] = self.get_argument("language", default="")
        for v in params.values():
            if not v:
                raise RuntimeError("Empty item")
        if len(params["code"]) < 5:
            raise RuntimeError("Code too short")
        return params

    @gen.coroutine
    def _check_submit_frequency(self, username):
        last_sm = yield self.settings["database"]["submission"].find_one({
            "username": username,
        }, sort=[
            ("submittime", -1),
        ])
        if not last_sm:
            return
        now = datetime.datetime.now().timestamp()
        last = last_sm["submittime"].timestamp()
        if now - last < 10:
            raise RuntimeError("Please wait for at least 10s")

    @gen.coroutine
    def _add_submission(self, cookies, params):
        # code = base64.b64decode(params["code"]).decode()
        code = params["code"]
        r1 = yield self.settings["database"]["submission"].insert_one({
            # User
            "username": cookies["username"],
            "nickname": cookies["nickname"],
            # Problem
            "soj": params["soj"],
            "sid": params["sid"],
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
        r2 = yield self.settings["database"]["user"].update_one(
            {'username': cookies["username"]},
            {'$set': {'last_submit_time': datetime.datetime.now()}}
        )
        if not r1.acknowledged or not r2.acknowledged:
            raise RuntimeError("Create submission error")
