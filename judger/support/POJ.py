"""北京大学"""

import re

from . import OJ, NoMatchError, LoginError

class Runner(OJ):
    encoding = "utf8"

    def login(self):
        self.session.post("http://poj.org/login", data={
            "user_id1": self.username,
            "password1": self.password,
        }, timeout=self.timeout)
        r = self.session.get("http://poj.org/", timeout=self.timeout)
        r.encoding = self.encoding
        if self.nickname not in r.text:
            raise LoginError

    def submit(self, sid, language, code):
        self.session.post("http://poj.org/submit", data={
            "problem_id": sid,
            "language": language,
            "source": code,
            "encoded": 0,
        }, timeout=self.timeout, proxies=self.proxy)

    def get_last_runid(self):
        r = self.session.get("http://poj.org/status?user_id=%s" % self.username, timeout=self.timeout)
        r.encoding = self.encoding
        match = re.findall(r"<tr align=center><td>(\d+?)</td><td><a href=userstatus\?user_id=", r.text)
        if not match:
            raise NoMatchError("runid")
        return int(match[0])

    def get_result(self, runid):
        r = self.session.get("http://poj.org/status?user_id=%s" % self.username, timeout=self.timeout)
        r.encoding = self.encoding
        match = re.findall(r"<tr align=center><td>" + str(runid) + r"</td><td><a href=userstatus\?user_id=.+?>.+?</a></td><td><a href=problem\?id=\d+?>\d+?</a></td><td>(.+?)</td><td>(.*?)</td><td>(.*?)</td>", r.text)
        if not match:
            raise NoMatchError("result")
        raw_result = match[0][0]
        raw_memoryused = match[0][1]
        raw_timeused = match[0][2]
        match = re.findall(r"<font color=.+?>(.+?)</font>", raw_result)
        if not match:
            raise NoMatchError("result")
        result = match[0]
        match = re.findall(r"(\d+?)K", raw_memoryused)
        if not match:
            memoryused = 0
        else:
            memoryused = int(match[0])
        match = re.findall(r"(\d+?)MS", raw_timeused)
        if not match:
            timeused = 0
        else:
            timeused = int(match[0])
        return result, timeused, memoryused

    def get_compile_error_info(self, runid):
        r = self.session.get("http://poj.org/showcompileinfo?solution_id=" + str(runid), timeout=self.timeout)
        r.encoding = self.encoding
        match = re.findall(r"<pre>([.\s\S]+?)</pre>", r.text)
        if not match:
            raise NoMatchError("errorinfo")
        return match[0]
