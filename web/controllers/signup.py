from tornado import gen
from tornado.web import RequestHandler


class Handler(RequestHandler):
    @gen.coroutine
    def get(self):
        return self.render("board.htm")
        try:
            sups = yield self.settings["database"]["sup"].find().sort([("school", 1)]).to_list(None)
        except RuntimeError as err:
            self.render("message.html", text=str(err))
        else:
            self.render("signup.html", sups=sups)

    @gen.coroutine
    def post(self):
        data = {}
        data["school"] = self.get_argument("school")
        data["teamname"] = self.get_argument("teamname")
        data["status"] = "待审核"
        data["user1"] = {
            "name": self.get_argument("name1"),
            "number": self.get_argument("number1"),
            "major": self.get_argument("major1"),
            "phone": self.get_argument("phone1"),
            "email": self.get_argument("email1"),
        }
        data["user2"] = {
            "name": self.get_argument("name2"),
            "number": self.get_argument("number2"),
            "major": self.get_argument("major2"),
            "phone": self.get_argument("phone2"),
            "email": self.get_argument("email2"),
        }
        data["user3"] = {
            "name": self.get_argument("name3"),
            "number": self.get_argument("number3"),
            "major": self.get_argument("major3"),
            "phone": self.get_argument("phone3"),
            "email": self.get_argument("email3"),
        }
        teamname = yield self.settings["database"]["sup"].find_one({
            "teamname": data["teamname"],
        })
        if teamname:
            return self.render("message.html", text="队名已存在")
        yield self.settings["database"]["sup"].insert_one(data)
        return self.render("message.html", text="报名成功")
