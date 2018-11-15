import hashlib

from tornado.web import RequestHandler
from tornado import gen


class Handler(RequestHandler):
    @gen.coroutine
    def post(self):
        """修改密码"""
        try:
            username = self._get_cookie_username()
            params = self._get_params()
            password_indb = yield self._find_user_password(username)
            self._check_password(params["password_old"], password_indb)
            yield self._update_password(username, params["password_new"])
        except RuntimeError:
            self.write(str(1))
        else:
            self.write(str(0))

    def _get_cookie_username(self):
        username = self.get_secure_cookie("username")
        if not username:
            raise RuntimeError("Please login")
        return username.decode()

    def _get_params(self):
        params = {}
        params["password_old"] = self.get_argument("password_old", default="")
        params["password_new"] = self.get_argument("password_new", default="")
        for v in params.values():
            if not v:
                raise RuntimeError("Empry item")
        return params

    @gen.coroutine
    def _find_user_password(self, username):
        user = yield self.settings["database"]["user"].find_one({
            "username": username,
        }, {
            "password": 1,
        })
        if not user:
            raise RuntimeError("Username not exists")
        return user["password"]

    def _check_password(self, password_post, password_indb):
        m = hashlib.md5()
        m.update(password_post.encode("utf8"))
        if m.hexdigest() != password_indb:
            raise RuntimeError("Incorrect old password")

    @gen.coroutine
    def _update_password(self, username, password_new):
        m = hashlib.md5()
        m.update(password_new.encode("utf8"))
        r = yield self.settings["database"]["user"].update_one({
            "username": username,
        }, {
            "$set": {
                "password": m.hexdigest(),
            },
        })
        if r.modified_count != 1:
            raise RuntimeError("Update error")
