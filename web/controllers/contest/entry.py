from bson.objectid import ObjectId
from tornado import gen
from tornado.web import RequestHandler


class Handler(RequestHandler):
    @gen.coroutine
    def get(self, _id):
        """比赛入口"""
        try:
            password_indb = yield self._find_contest_password(_id)
        except RuntimeError as err:
            self.render("message.html", text=str(err))
        if password_indb:
            self.render("contest/entry.html")
        else:
            self.redirect("/contest/overview/" + _id)

    @gen.coroutine
    def post(self, _id):
        """检验密码"""
        try:
            password_indb = yield self._find_contest_password(_id)
            password = self.get_argument("password", default="")
            if password != password_indb:
                raise RuntimeError("Incorrect password")
            self.set_secure_cookie("contest", _id)
            self.redirect("/contest/overview/" + _id)
        except RuntimeError as err:
            self.render("message.html", text=str(err))

    @gen.coroutine
    def _find_contest_password(self, _id):
        contest = yield self.settings["database"]["contest"].find_one({
            "_id": ObjectId(_id),
        }, {
            "password": 1,
        })
        if not contest:
            raise RuntimeError("No record")
        return contest["password"]
