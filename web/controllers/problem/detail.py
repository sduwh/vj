from tornado.web import RequestHandler
from tornado import gen
from tornado.ioloop import IOLoop


class BaseHandler(RequestHandler):
     def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')


class Handler(BaseHandler):
    @gen.coroutine
    def get(self, soj, sid):
        """题目详情"""
        try:
            problem = yield self._find_problem(soj, int(sid))
        except RuntimeError as err:
            self.render("message.html", text=str(err))
        else:
            username = self._get_cookie_username()
            # 获取可提交的语言
            cursor = self.settings["database"]["remoteOJs"].find({'soj': problem['soj']})
            remotes = []
            for document in (yield cursor.to_list(length=100)):
                remotes.append({"language": document['language'], "remote":document['remote']})
            remotes.sort(key=lambda d: d['remote'])
            self.render("problem/detail.html", problem=problem, username=username, remotes=remotes)

    @gen.coroutine
    def _find_problem(self, soj, sid):
        problem = yield self.settings["database"]["problem"].find_one({
            "soj": soj, "sid": sid
        })
        if not problem:
            raise RuntimeError("No record")
        return problem

    def _get_cookie_username(self):
        username = self.get_secure_cookie("username")
        if not username:
            return None
        return username.decode()


