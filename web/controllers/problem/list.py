from tornado import gen
from tornado.web import RequestHandler


class Handler(RequestHandler):
    @gen.coroutine
    def get(self):
        """é¢˜ç›®åˆ—è¡¨"""
        try:
            params = self._get_params()
            filters = self._make_filters(params)
            totalpage = yield self._find_totalpage(filters)
            if params["page"] < 1 or params["page"] > totalpage:
                raise RuntimeError("Incorrect page")
            problems = yield self._find_problems(filters, params["page"])

        except RuntimeError as err:
            self.render("message.html", text=str(err))
        else:
            cursor = self.settings["database"]["OJ"].find()
            ojs = []
            for document in (yield cursor.to_list(length=100)):
                ojs.append({"oj": document['soj']})
            self.render("problem/list.html", problems=problems, params=params, totalpage=totalpage, ojs=ojs)

    def _get_params(self):
        params = {}
        try:
            params["page"] = int(self.get_argument("page", default=1))
        except ValueError:
            params["page"] = 1
        try:
            params["sid"] = self.get_argument("sid", default="")
        except ValueError:
            params["sid"] = ""
        params["soj"] = self.get_argument("soj", default="")
        params["title"] = self.get_argument("title", default="")
        params["source"] = self.get_argument("source", default="")
        return params

    def _make_filters(self, params):
        return {
            "soj": params["soj"] if params["soj"] else {"$regex": r".*"},
            "sid": params["sid"] if params["sid"] else {"$ne": 0},
            "title": {"$regex": params["title"]} if params["title"] else {"$regex": r".*"},
            "source": {"$regex": params["source"]} if params["source"] else {"$regex": r".*"},
        }

    @gen.coroutine
    def _find_totalpage(self, filters):
        totalcount = yield self.settings["database"]["problem"].find(filters).count()
        totalpage = totalcount // self.settings["rows_per_page"] + 1
        return totalpage

    @gen.coroutine
    def _find_problems(self, filters, page):
        problems = yield self.settings["database"]["problem"].find(filters, {
            "soj": 1, "sid": 1, "title": 1, "source": 1
        }).sort([("sid", 1)]).skip((page - 1) * self.settings["rows_per_page"]).limit(
            self.settings["rows_per_page"]).to_list(self.settings["rows_per_page"])
        return problems

    @gen.coroutine
    def _find_oj(self):
        oj = yield self.settings["database"]["OJ"].find()
        return oj
