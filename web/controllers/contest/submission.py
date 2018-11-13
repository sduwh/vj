from tornado.web import RequestHandler
from tornado import gen
from bson.objectid import ObjectId

class Handler(RequestHandler):
    @gen.coroutine
    def get(self, _id):
        """比赛内提交列表"""
        try:
            contest = yield self._find_contest(_id)
            if contest["password"]:
                self._check_permission(_id)
            params = self._get_params()
            filters = self._make_filters(_id, params)
            totalpage = yield self._find_totalpage(filters)
            if params["page"] < 1 or params["page"] > totalpage:
                raise RuntimeError("Incorrect page")
            submissions = yield self._find_submissions(filters, params["page"])
        except RuntimeError as err:
            self.render("message.html", text=str(err))
        else:
            username = self._get_cookie_username()
            self.render("contest/submission.html", contest=contest, submissions=submissions, params=params, totalpage=totalpage, username=username)

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
            params["page"] = int(self.get_argument("page", default=""))
        except ValueError:
            params["page"] = 1
        params["nickname"] = self.get_argument("nickname", default="")
        params["result"] = self.get_argument("result", default="")
        return params

    def _make_filters(self, _id, params):
        return {
            "contest_id": ObjectId(_id),
            "nickname": {"$regex": params["nickname"]} if params["nickname"] else {"$regex": r".*"},
            "result": {"$regex": params["result"]} if params["result"] else {"$regex": r".*"},
        }

    @gen.coroutine
    def _find_totalpage(self, filters):
        totalcount = yield self.settings["database"]["submission"].find(filters).count()
        totalpage = totalcount // self.settings["rows_per_page"] + 1
        return totalpage

    @gen.coroutine
    def _find_submissions(self, filters, page):
        submissions = yield self.settings["database"]["submission"].find(filters, {
            "n": 1,
            "soj": 1,
            "username": 1,
            "nickname": 1,
            "result": 1,
            "timeused": 1,
            "memoryused": 1,
            "remote": 1,
            "codesize": 1,
            "submittime": 1,
        }).sort([("submittime", -1)]).skip((page - 1) * self.settings["rows_per_page"]).limit(self.settings["rows_per_page"]).to_list(self.settings["rows_per_page"])
        return submissions

    def _get_cookie_username(self):
        username = self.get_secure_cookie("username")
        if not username:
            return None
        return username.decode()
