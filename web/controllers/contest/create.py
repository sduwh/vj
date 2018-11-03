import re
import datetime

from tornado.web import RequestHandler
from tornado import gen

class Handler(RequestHandler):
    @gen.coroutine
    def post(self):
        """创建比赛"""
        try:
            cookies = self._get_cookies()
            params = self._get_params()
            problems = self._parse_problems(params["problem"])
            yield self._add_contest(params, cookies, problems)
        except RuntimeError as err:
            self.render("message.html", text=str(err))
        else:
            self.redirect("/contest")

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
        params["title"] = self.get_argument("title", default="")
        params["begintime"] = self.get_argument("begintime", default="")
        params["endtime"] = self.get_argument("endtime", default="")
        params["problem"] = self.get_argument("problem", default="")
        for v in params.values():
            if not v:
                raise RuntimeError("Empty item")
        params["password"] = self.get_argument("password", default="")
        params["description"] = self.get_argument("description", default="")
        return params

    def _parse_problems(self, problems_str):
        problems = []
        for p in problems_str.split('\t\r\n'):
            match = re.findall(r"([A-Z]+)\-(\d+)\s\|(.*)", p)
            if not match:
                raise RuntimeError("Problem format error")
            problems.append({
                "soj": match[0][0],
                "sid": int(match[0][1]),
                "alias": match[0][2],
            })
        return problems

    @gen.coroutine
    def _add_contest(self, params, cookies, problems):
        try:
            begintime = datetime.datetime.strptime(params["begintime"], "%Y-%m-%d %H:%M:%S")
            endtime = datetime.datetime.strptime(params["endtime"], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise RuntimeError("Time format error")
        if begintime >= endtime:
            raise RuntimeError("BeginTime later than EndTime")
        r = yield self.settings["database"]["contest"].insert_one({
            "username": cookies["username"],
            "nickname": cookies["nickname"],
            "title": params["title"],
            "password": params["password"],
            "description": params["description"],
            "begintime": begintime,
            "endtime": endtime,
            "problems": problems,
        })
        if not r.acknowledged:
            raise RuntimeError("Create contest error")