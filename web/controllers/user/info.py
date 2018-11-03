from tornado.web import RequestHandler
from tornado import gen

class Handler(RequestHandler):
    @gen.coroutine
    def get(self):
        """用户信息页面"""
        try:
            username = self._get_cookie_username()
            user = yield self._find_user_info(username)
            data = yield self._find_user_data(username)
        except RuntimeError as err:
            self.render("message.html", text=str(err))
        else:
            self.render("user/info.html", user=user, data=data)

    def _get_cookie_username(self):
        username = self.get_secure_cookie("username")
        if not username:
            raise RuntimeError("Please login")
        return username.decode()

    @gen.coroutine
    def _find_user_info(self, username):
        user = yield self.settings["database"]["user"].find_one({
            "username": username,
        })
        if not user:
            raise RuntimeError("Username not exists")
        return user

    @gen.coroutine
    def _find_user_data(self, username):
        data = {}
        data["totalsm"] = yield self.settings["database"]["submission"].find({
            "username": username,
        }).count()
        data["totalac"] = yield self.settings["database"]["submission"].find({
            "username": username, "result": "Accepted",
        }).count()
        return data