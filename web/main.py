"""Web模块"""

import tornado.web
import tornado.ioloop
import motor.motor_tornado

import config
import controllers.index
import controllers.user.login
import controllers.user.logout
import controllers.user.register
import controllers.user.record
# import controllers.user.resetpassword
import controllers.problem.list
import controllers.problem.detail
import controllers.problem.submit
import controllers.problem.create
import controllers.submission.list
import controllers.submission.detail
import controllers.contest.list
import controllers.contest.create
import controllers.contest.delete
import controllers.contest.entry
import controllers.contest.overview
import controllers.contest.problem
import controllers.contest.submit
import controllers.contest.submission
import controllers.contest.rank
import controllers.rank.list
import controllers.signup
import controllers.signupaccess
import controllers.signupdelete

import controllers.api.user.record
import controllers.api.user.resetpassword

settings = {
    "static_path": config.static_path,
    "template_path": config.template_path,
    "rows_per_page": config.rows_per_page,
    "database": motor.motor_tornado.MotorClient(config.dbhost)[config.dbname],
    "cookie_secret": "____________MYSTERY____________",
}

def main():
    tornado.web.Application([
        (r"/", controllers.index.Handler),
        (r"/login", controllers.user.login.Handler),
        (r"/logout", controllers.user.logout.Handler),
        (r"/register", controllers.user.register.Handler),
        (r"/user/?", controllers.user.record.Handler),
        # (r"/user/resetpassword", controllers.user.resetpassword.Handler),
        (r"/problem", controllers.problem.list.Handler),
        (r"/problem/([a-zA-Z_]+)/([0-9a-zA-Z-/]+)", controllers.problem.detail.Handler),
        (r"/problem/submit", controllers.problem.submit.Handler),
        (r"/problem/create", controllers.problem.create.Handler),
        (r"/submission", controllers.submission.list.Handler),
        (r"/submission/(.+?)", controllers.submission.detail.Handler),
        (r"/contest", controllers.contest.list.Handler),
        (r"/contest/create", controllers.contest.create.Handler),
        (r"/contest/delete/(.+?)", controllers.contest.delete.Handler),
        (r"/contest/entry/(.+?)", controllers.contest.entry.Handler),
        (r"/contest/overview/(.+?)", controllers.contest.overview.Handler),
        (r"/contest/problem/(.+?)", controllers.contest.problem.Handler),
        (r"/contest/submit/(.+?)", controllers.contest.submit.Handler),
        (r"/contest/submission/(.+?)", controllers.contest.submission.Handler),
        (r"/contest/rank/(.+?)", controllers.contest.rank.Handler),
        (r"/rank", controllers.rank.list.Handler),
        (r"/signup", controllers.signup.Handler),
        (r"/signup/admin/access", controllers.signupaccess.Handler),
        (r"/signup/admin/delete", controllers.signupdelete.Handler),
        (r'/api/user/record', controllers.api.user.record.Handler),
        (r'/api/user/resetpassword', controllers.api.user.resetpassword.Handler),
    ],
    **settings).listen(config.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
