import datetime

from bson.objectid import ObjectId
from tornado import gen
from tornado.web import RequestHandler


class Handler(RequestHandler):
    @gen.coroutine
    def get(self, _id):
        """比赛题目"""
        try:
            contest = yield self._find_contest(_id)
            if contest["password"]:
                self._check_permission(_id)
            username = self._get_cookie_username()
            now = datetime.datetime.now()
            if now < contest["begintime"] and username != contest["username"]:
                self.redirect("/contest/overview/" + _id)
            params = self._get_params()
            problem = contest["problems"][params["n"]]
            problem_detail = yield self._find_problem(problem["soj"], problem["sid"])
            problem.update(problem_detail)
            remotes = []
            cursor = self.settings["database"]["remoteOJs"].find({'soj': problem['soj']})
            for document in (yield cursor.to_list(length=100)):
                remotes.append({"language": document['language'], "remote": document['remote']})
        except RuntimeError as err:
            self.render("message.html", text=str(err))
        else:
            self.render("contest/problem.html", contest=contest, problem=problem, n=params["n"],
                        now=datetime.datetime.now(), username=username, remotes=remotes)

    @gen.coroutine
    def _find_contest(self, _id):
        contest = yield self.settings["database"]["contest"].find_one({
            "_id": ObjectId(_id),
        })
        if not contest:
            raise RuntimeError("No record")
        return contest

    def _check_permission(self, _id):
        contest_id = self.get_secure_cookie("contest")
        if not contest_id or _id != contest_id.decode():
            raise RuntimeError("Please enter password")

    def _get_params(self):
        params = {}
        try:
            params["n"] = int(self.get_argument("n", default=0))
        except ValueError:
            params["n"] = 0
        return params

    @gen.coroutine
    def _find_problem(self, soj, sid):
        print(soj, sid)
        problem = yield self.settings["database"]["problem"].find_one({
            "soj": str(soj), "sid": str(sid),
        })
        print(problem)
        if not problem:
            raise RuntimeError("No record")
        return problem

    def _get_cookie_username(self):
        username = self.get_secure_cookie("username")
        if not username:
            return None
        return username.decode()
