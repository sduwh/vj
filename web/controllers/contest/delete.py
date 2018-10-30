from bson.objectid import ObjectId
from tornado import gen
from tornado.web import RequestHandler


class Handler(RequestHandler):
    @gen.coroutine
    def get(self, _id):
        """删除比赛"""
        try:
            username = self._get_cookie_username()
            manager = yield self._find_contest_manager(_id)
            if username != manager:
                raise RuntimeError("Not allowed")
            yield self._delete_contest(_id)
            yield self._delete_submissions(_id)
        except RuntimeError as err:
            self.render("message.html", text=str(err))
        else:
            self.redirect("/contest")

    def _get_cookie_username(self):
        username = self.get_secure_cookie("username")
        if not username:
            raise RuntimeError("Please login")
        return username.decode()

    @gen.coroutine
    def _find_contest_manager(self, _id):
        contest = yield self.settings["database"]["contest"].find_one({
            "_id": ObjectId(_id),
        }, {
            "username": 1,
        })
        if not contest:
            raise RuntimeError("No record")
        return contest["username"]

    @gen.coroutine
    def _delete_contest(self, _id):
        r = yield self.settings["database"]["contest"].delete_one({
            "_id": ObjectId(_id),
        })
        if r.deleted_count != 1:
            raise RuntimeError("Delete contest error")

    @gen.coroutine
    def _delete_submissions(self, _id):
        r = yield self.settings["database"]["submission"].delete_many({
            "contest_id": ObjectId(_id),
        })
        if not r.deleted_count:
            raise RuntimeError("Delete contest-submissions error")
