from tornado.web import RequestHandler
from tornado import gen

class Handler(RequestHandler):
    @gen.coroutine
    def get(self):
        """用户信息页面"""
        try:
            self._get_cookie_username()
        except RuntimeError as err:
            self.render('message.html', text=str(err))
        else:
            self.render('user/record.html')

    def _get_cookie_username(self):
        username = self.get_secure_cookie("username")
        if not username:
            raise RuntimeError("Please login")
        return username.decode()
