import hashlib

from tornado.web import RequestHandler
from tornado import gen

class Handler(RequestHandler):
    @gen.coroutine
    def post(self):
        """登录"""
        try:
            params = self._get_params()
            user = yield self._find_user(params["username"])
            self._check_password(params["password"], user["password"])
        except RuntimeError as err:
            self.render("message.html", text=str(err))
        else:
            self._set_cookies(params["username"], user["nickname"])
            referer = self.request.headers["referer"]
            # 如果是创建contest的时候发现没有登录 就不能redirect(referer)
            # 因为/contest/create不支持GET方法
            if "/contest/create" in referer:
                self.redirect("/contest")
            elif "/login" in referer or "/register" in referer:
                self.redirect("/")
            else:
                self.redirect(referer)

    def _get_params(self):
        params = {}
        params["username"] = self.get_argument("username", default="")
        params["password"] = self.get_argument("password", default="")
        for v in params.values():
            if not v:
                raise RuntimeError("Empty item")
        return params

    @gen.coroutine
    def _find_user(self, username):
        user = yield self.settings["database"]["user"].find_one({
            "username": username,
        }, {
            "_id": 0, "password": 1, "nickname": 1,
        })
        if not user:
            raise RuntimeError("Username not exists")
        return user

    def _check_password(self, password_post, password_indb):
        m = hashlib.md5()
        m.update(password_post.encode("utf8"))
        if m.hexdigest() != password_indb:
            raise RuntimeError("Incorrect password")

    def _set_cookies(self, username, nickname):
        self.set_secure_cookie("username", username)
        self.set_secure_cookie("nickname", nickname)