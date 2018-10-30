import hashlib

from tornado import gen
from tornado.web import RequestHandler


class Handler(RequestHandler):
    @gen.coroutine
    def post(self):
        """注册"""
        try:
            params = self._get_params()
            yield self._check_user_exist(params["username"])
            yield self._add_user(params)
        except RuntimeError as err:
            self.render("message.html", text=str(err))
        else:
            self._set_cookies(params["username"], params["nickname"])
            referer = self.request.headers["referer"]
            if "/contest/create" in referer:
                self.redirect("/contest")
            elif "/login" in referer or "/register" in referer:
                self.redirect("/")
            else:
                self.redirect(referer)

    def _get_params(self):
        params = {}
        params["usertype"] = self.get_argument("usertype", default="user")
        params["username"] = self.get_argument("username", default="")
        params["nickname"] = self.get_argument("nickname", default="")
        params["password"] = self.get_argument("password", default="")
        for v in params.values():
            if not v:
                raise RuntimeError("Empty item")
        return params

    @gen.coroutine
    def _check_user_exist(self, username):
        count = yield self.settings["database"]["user"].find({
            "username": username,
        }).count()
        if count != 0:
            raise RuntimeError("Username existed")

    @gen.coroutine
    def _add_user(self, params):
        m = hashlib.md5()
        m.update(params["password"].encode("utf8"))
        r = yield self.settings["database"]["user"].insert_one({
            "usertype": params["usertype"],
            "username": params["username"],
            "nickname": params["nickname"],
            "password": m.hexdigest(),
        })
        if not r.acknowledged:
            raise RuntimeError("Add user error")

    def _set_cookies(self, username, nickname):
        self.set_secure_cookie("username", username)
        self.set_secure_cookie("nickname", nickname)
