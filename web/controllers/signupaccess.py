from tornado.web import RequestHandler
from tornado import gen

class Handler(RequestHandler):
    @gen.coroutine
    def get(self):
        try:
            username = self._get_cookie_username()
            if username != "adminsignup":
                raise RuntimeError("No way")
            yield self.settings["database"]["sup"].update_one({
                "teamname": self.get_argument("teamname"),
            }, {
                "$set": {"status": "报名成功"},
            })
        except Exception as err:
            self.render("message.html", text=str(err))
        else:
            self.redirect("/signup")

    def _get_cookie_username(self):
        username = self.get_secure_cookie("username")
        if not username:
            raise RuntimeError("Please login")
        return username.decode()

