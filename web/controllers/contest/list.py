import datetime

from tornado import gen
from tornado.web import RequestHandler


class Handler(RequestHandler):
    @gen.coroutine
    def get(self):
        """比赛列表"""
        try:
            params = self._get_params()
            filters = self._make_filters(params)
            totalpage = yield self._find_totalpage(filters)
            if params["page"] < 1 or params["page"] > totalpage:
                raise RuntimeError("Incorrect page")
            contests = yield self._find_contests(filters, params["page"])
        except RuntimeError as err:
            self.render("message.html", text=str(err))
        else:
            cursor = self.settings["database"]["OJ"].find()
            ojs = []
            for document in (yield cursor.to_list(length=100)):
                ojs.append({"oj": document['soj']})
            self.render("contest/list.html", contests=contests, params=params, totalpage=totalpage,
                        now=datetime.datetime.now(), ojs=ojs)

    def _get_params(self):
        params = {}
        try:
            params["page"] = int(self.get_argument("page", default=1))
        except ValueError:
            params["page"] = 1
        params["title"] = self.get_argument("title", default="")
        params["nickname"] = self.get_argument("nickname", default="")
        return params

    def _make_filters(self, params):
        return {
            "title": {"$regex": params["title"]} if params["title"] else {"$regex": r".*"},
            "nickname": {"$regex": params["nickname"]} if params["nickname"] else {"$regex": r".*"},
        }

    @gen.coroutine
    def _find_totalpage(self, filters):
        totalcount = yield self.settings["database"]["contest"].find(filters).count()
        totalpage = totalcount // self.settings["rows_per_page"] + 1
        return totalpage

    @gen.coroutine
    def _find_contests(self, filters, page):
        contests = yield self.settings["database"]["contest"].find(filters, {
            "title": 1, "begintime": 1, "endtime": 1, "password": 1, "username": 1, "nickname": 1,
        }).sort([("_id", -1)]).skip((page - 1) * self.settings["rows_per_page"]).limit(
            self.settings["rows_per_page"]).to_list(self.settings["rows_per_page"])
        return contests
