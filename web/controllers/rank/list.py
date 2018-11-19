from tornado.web import RequestHandler
from tornado import gen

class Handler(RequestHandler):
    @gen.coroutine
    def get(self):
        try:
            params = self._get_params()
            filters = self._make_filters(params)
            totalpage = yield self._find_totalpage(filters)
            if params["page"] < 1 or params["page"] > totalpage:
                raise RuntimeError("Incorrect page")
            ranks = yield self._find_ranks(filters, params["page"])

        except RuntimeError as err:
            self.render("message.html", text=str(err))
        else:
            self.render("rank/list.html", ranks=ranks, params=params, totalpage=totalpage)

    def _get_params(self):
        params = {}
        try:
            params["page"] = int(self.get_argument("page", default=1))
        except ValueError:
            params["page"] = 1
        try:
            params["nickname"] = self.get_argument("nickname", default="")
        except ValueError:
            params["nickname"] = ""
        try:
            params["rank"] = self.get_argument("rank", default="")
        except ValueError:
            params["rank"] = ""
        return params

    def _make_filters(self, params):
        f = {
            "nickname": {"$regex": params["nickname"]} if params["nickname"] else {"$regex": r".*"},
        }
        try:
            f['rank'] = int(params['rank'])
        finally:
            return f

    @gen.coroutine
    def _find_totalpage(self, filters):
        totalcount = yield self.settings["database"]["user"].find(filters).count()
        totalpage = totalcount // self.settings["rows_per_page"] + 1
        return totalpage

    @gen.coroutine
    def _find_ranks(self, filters, page):
        rank = yield self.settings["database"]["user"].find(filters, {
            "nickname": 1, "total_sub": 1, "total_ac": 1, "total_wa": 1, "last_submit_time": 1,"rank": 1
        }).sort([("rank", 1)]).skip((page - 1) * self.settings["rows_per_page"]).limit(self.settings["rows_per_page"]).to_list(self.settings["rows_per_page"])
        return rank
