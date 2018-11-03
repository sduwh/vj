from tornado.web import RequestHandler

class Handler(RequestHandler):
    def get(self):
        """注销"""
        self.clear_cookie("username")
        self.clear_cookie("nickname")
        self.redirect(self.request.headers["referer"])