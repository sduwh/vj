from tornado.web import RequestHandler
from tornado import gen


class Handler(RequestHandler):
    @gen.coroutine
    def get(self):
        params = self._get_params()
        username = self._get_cookie_username()
        user = yield self._find_user_info(username)

        if params['type'] == 'index':
            self.write({
                'username': user.get('username'),
                'nickname': user.get('nickname'),
                'total_sub': user.get('total_sub'),
                'total_ac': user.get('total_ac'),
                'total_wa': user.get('total_wa'),
                'last_submit_time': str(user.get('last_submit_time').timestamp() * 1000)
                                    if user.get('last_submit_time') else None,
            })
        elif params['type'] == 'others':
            self.write({'test': 'working on'})
        else:
            self.send_error(500)

    @gen.coroutine
    def _find_user_info(self, username):
        user = yield self.settings["database"]["user"].find_one({
            "username": username,
        })
        return user

    def _get_cookie_username(self):
        username = self.get_secure_cookie("username")
        return username.decode()

    def _get_params(self):
        params = {}
        params["type"] = self.get_argument("type", default="")
        return params
