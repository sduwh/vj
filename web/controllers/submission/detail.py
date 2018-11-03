from tornado.web import RequestHandler
from tornado import gen
from bson.objectid import ObjectId

class Handler(RequestHandler):
    @gen.coroutine
    def get(self, _id):
        """提交详情"""
        try:
            username = self._get_cookie_username()
            submission = yield self._find_submission(_id)
            if username != "admin" and username != submission["username"]:
                contest_id = self.get_argument("contest_id", default=None)
                if contest_id == None:
                    raise RuntimeError("Not allowed")
                contest = yield self._find_contest(contest_id)
                if contest["username"] != username:
                    raise RuntimeError("Not allowed")
        except RuntimeError as err:
            self.render("message.html", text=str(err))
        else:
            self.render("submission/detail.html", submission=submission)

    def _get_cookie_username(self):
        username = self.get_secure_cookie("username")
        if not username:
            raise RuntimeError("Please login")
        return username.decode()

    @gen.coroutine
    def _find_submission(self, _id):
        submission = yield self.settings["database"]["submission"].find_one({
            "_id": ObjectId(_id),
        })
        if not submission:
            raise RuntimeError("Submission not exists")
        return submission

    @gen.coroutine
    def _find_contest(self, _id):
        contest = yield self.settings["database"]["contest"].find_one({
            "_id": ObjectId(_id),
        })
        if not contest:
            raise RuntimeError("No record")
        return contest
