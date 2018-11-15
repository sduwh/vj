from tornado.web import RequestHandler
from tornado import gen

class Handler(RequestHandler):
    @gen.coroutine
    def get(self):
        """提交列表"""
        try:
            params = self._get_params()
            filters = self._make_filters(params)
            totalpage = yield self._find_totalpage(filters)
            if params["page"] < 1 or params["page"] > totalpage:
                raise RuntimeError("Incorrect page")
            submissions = yield self._find_submissions(filters, params["page"])
        except RuntimeError as err:
            self.render("message.html", text=str(err))
        else:
            username = self._get_cookie_username()
            # cursor = self.settings["database"]["OJ"].find()
            ojs = [
                {'oj': 'HDU'},
                {'oj': 'POJ'},
            ]
            # for document in (yield cursor.to_list(length=100)):
            #     ojs.append({"oj": document['soj']})
            self.render("submission/list.html", submissions=submissions, params=params, totalpage=totalpage, username=username, ojs=ojs)

    def _get_params(self):
        params = {}
        try:
            params["page"] = int(self.get_argument("page", default=1))
        except ValueError:
            params["page"] = 1
        try:
            params["sid"] = int(self.get_argument("sid", default=""))
        except ValueError:
            params["sid"] = ""
        params["soj"] = self.get_argument("soj", default="")
        params["result"] = self.get_argument("result", default="")
        params["nickname"] = self.get_argument("nickname", default="")
        return params

    def _make_filters(self, params):
        return {
            "contest_id": {"$exists": False},
            "soj": params["soj"] if params["soj"] else {"$regex": r".*"},
            "sid": params["sid"] if params["sid"] else {"$ne": 0},
            "result": {"$regex": params["result"]} if params["result"] else {"$regex": r".*"},
            "nickname": {"$regex": params["nickname"]} if params["nickname"] else {"$regex": r".*"},
        }

    @gen.coroutine
    def _find_totalpage(self, filters):
        totalcount = yield self.settings["database"]["submission"].find(filters).count()
        totalpage = totalcount // self.settings["rows_per_page"] + 1
        return totalpage

    @gen.coroutine
    def _find_submissions(self, filters, page):
        submissions = yield self.settings["database"]["submission"].find(filters, {
            "username": 1,
            "nickname": 1,
            "soj": 1,
            "sid": 1,
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
