from tornado.web import RequestHandler


class Handler(RequestHandler):
    def get(self):
        """首页"""
        self.render("index.html")
