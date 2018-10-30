import datetime

from bson.objectid import ObjectId
from tornado import gen
from tornado.web import RequestHandler


class Handler(RequestHandler):
    @gen.coroutine
    def get(self, _id):
        """比赛介绍"""
        try:
            contest = yield self._find_contest(_id)
            if contest["password"]:
                self._check_permission(_id)
        except RuntimeError as err:
            self.render("message.html", text=str(err))
        else:
            username = self._get_cookie_username()
            self.render("contest/overview.html", contest=contest, now=datetime.datetime.now(), username=username)

    def _check_permission(self, _id):
        contest_id = self.get_secure_cookie("contest")
        if not contest_id or _id != contest_id.decode():
            raise RuntimeError("Please enter password")

    @gen.coroutine
    def _find_contest(self, _id):
        contest = yield self.settings["database"]["contest"].find_one({
            "_id": ObjectId(_id),
        })
        if not contest:
            raise RuntimeError("No record")
        return contest

    def _get_cookie_username(self):
        username = self.get_secure_cookie("username")
        if not username:
            return None
        return username.decode()
