"""山东理工大学"""

import re

from . import OJ, NoMatchError, LoginError

BASE_URL = "http://acm.sdut.edu.cn/"

class Runner(OJ):
    encoding = "utf8"

    def login(self):
        self.session.post(BASE_URL + "onlinejudge2/index.php/Login/login", data={
            "user_name": self.username,
            "password": self.password,
        }, timeout=self.timeout)
        r = self.session.get(BASE_URL + "onlinejudge2/index.php/Home", timeout=self.timeout)
        r.encoding = self.encoding
        if self.nickname not in r.text:
            raise LoginError

    def submit(self, sid, language, code):
        self.session.post(BASE_URL + "onlinejudge2/index.php/Home/Solution/submitsolution", data={
            "pid": sid,
            "lang": language,
            "code": code,
        }, timeout=self.timeout, proxies=self.proxy)

    def get_last_runid(self):
        r = self.session.get(BASE_URL + "onlinejudge2/index.php/Home/Solution/status?username=%s" % self.username, timeout=self.timeout)
        r.encoding = self.encoding
        match = re.findall(r'>(\d+?)</td>[\s\S]+?<td class="nowrap-td"', r.text)
        if not match:
            raise NoMatchError("runid")
        return int(match[0])

    def get_result(self, runid):
        r = self.session.get(BASE_URL + "onlinejudge2/index.php/Home/Solution/status?runid=" + str(runid), timeout=self.timeout)
        r.encoding = self.encoding
        match = re.findall(r'<td class=".+?">(.+?)</td>[\s\S]+?<td>(\d+?) ms</td>[\s\S]+?<td>(\d+?) KiB<', r.text)
        if not match:
            raise NoMatchError("result")
        result = match[0][0]
        if "Compile Error" in result:
            result = "Compile Error"
        timeused = int(match[0][1])
        memoryused = int(match[0][2])
        return result, timeused, memoryused

    def get_compile_error_info(self, runid):
        r = self.session.get(BASE_URL + "onlinejudge2/index.php/Home/Compile/view/sid/" + str(runid), timeout=self.timeout)
        r.encoding = self.encoding
        match = re.findall(r"<pre>([.\s\S]+?)</pre>", r.text)
        if not match:
            raise NoMatchError("errorinfo")
        return match[0]
