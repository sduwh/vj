from tornado.web import RequestHandler
from tornado import gen
import os
import hashlib
import json

class Handler(RequestHandler):
    def get(self):
        self.render("problem/create.html")

    @gen.coroutine
    def post(self):
        """创建题目"""
        try:
            cookies = self._get_cookies()
            if cookies["username"] != "manager":
                raise RuntimeError("没有权限")
            params = self._get_params()

            path = "/root/qdu-judger/volume/test_case/"+str(params["sid"])
            if not os.path.exists(path):
                os.makedirs(path)
            testcaseinput = self.get_argument("testcaseinput", default="")
            testcaseoutput = self.get_argument("testcaseoutput", default="")
            print(testcaseinput)
            with open(path+"/1.in", "w+") as f:
                f.write(testcaseinput)
            with open(path+"/1.out", "w+") as f:
                f.write(testcaseoutput)
            with open(path+"/info", "w+") as f:
                f.write(json.dumps({
                    "spj": False,
                    "test_cases": {
                        "1": {
                            "input_name": "1.in",
                            "input_size": len(testcaseinput),
                            "output_name": "1.out",
                            "output_size": len(testcaseoutput),
                            "striped_output_md5": hashlib.md5(testcaseoutput.encode()).hexdigest(),
                        },
                    },
                }))

            yield self._add_problem(params)
        except Exception as err:
            return self.render("message.html", text=str(err))
        else:
            self.redirect("/problem/VCode/"+str(params["sid"]))

    def _get_cookies(self):
        cookies = {}
        cookies["username"] = self.get_secure_cookie("username")
        cookies["nickname"] = self.get_secure_cookie("nickname")
        for k, v in cookies.items():
            if not v:
                raise RuntimeError("Please login")
            cookies[k] = cookies[k].decode()
        return cookies

    def _get_params(self):
        params = {}
        try:
            params["sid"] = int(self.get_argument("sid", default=""))
            params["timelimit"] = int(self.get_argument("timelimit", default=""))
            params["memorylimit"] = int(self.get_argument("memorylimit", default=""))
        except ValueError:
            raise RuntimeError("Not valid sid")
        params["title"] = self.get_argument("title", default="")
        params["description"] = self.get_argument("description", default="")
        params["input"] = self.get_argument("input", default="")
        params["output"] = self.get_argument("output", default="")
        params["sampleinput"] = self.get_argument("sampleinput", default="")
        params["sampleoutput"] = self.get_argument("sampleoutput", default="")
        params["source"] = self.get_argument("source", default="")
        return params

    @gen.coroutine
    def _add_problem(self, params):
        r = yield self.settings["database"]["problem"].insert_one({
            "soj": "VCode",
            "sid": params["sid"],
            "title": params["title"],
            "timelimit": params["timelimit"],
            "memorylimit": params["memorylimit"],
            "description": params["description"],
            "input": params["input"],
            "output": params["output"],
            "sampleinput": params["sampleinput"],
            "sampleoutput": params["sampleoutput"],
            "source": params["source"],
        })
        if not r.acknowledged:
            raise RuntimeError("Create problem error")
