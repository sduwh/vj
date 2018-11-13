"""杭州电子科技大学"""

import re

from . import OJ, NoMatchError, LoginError

class Runner(OJ):
    encoding = "gbk"

    def login(self):
        self.session.post("http://acm.hdu.edu.cn/userloginex.php?action=login", {
            "username": self.username,
            "userpass": self.password,
        }, timeout=self.timeout)
        r = self.session.get("http://acm.hdu.edu.cn", timeout=self.timeout)
        r.encoding = self.encoding
        if self.nickname not in r.text:
            raise LoginError

    def submit(self, sid, language, code):
        self.session.post("http://acm.hdu.edu.cn/submit.php?action=submit", data={
            "problemid": sid,
            "usercode": code,
            "language": language,
            "check": 0,
        }, timeout=self.timeout, proxies=self.proxy)

    def get_last_runid(self):
        r = self.session.get("http://acm.hdu.edu.cn/status.php?user=%s" % self.username, timeout=self.timeout)
        r.encoding = self.encoding
        match = re.findall(r"<td height=22px>(\d+?)</td>", r.text)
        if not match:
            raise NoMatchError("runid")
        return int(match[0])

    def get_result(self, runid):
        r = self.session.get("http://acm.hdu.edu.cn/status.php?user=%s" % self.username, timeout=self.timeout)
        r.encoding = self.encoding
        match = re.findall(r"<td height=22px>" + str(runid) + r'</td><td>[.\s\S]+?</td><td>[.\s\S]*?<font color=.+?>(.+?)</font>[.\s\S]*?</td><td><a href="/showproblem.php\?pid=\d+?">\d+?</a></td><td>(\d+?)MS</td><td>(\d+?)K</td>', r.text)
        if not match:
            raise NoMatchError("result")
        status = match[0][0]
        timeused = int(match[0][1])
        memoryused = int(match[0][2])
        return status, timeused, memoryused

    def get_compile_error_info(self, runid):
        r = self.session.get("http://acm.hdu.edu.cn/viewerror.php?rid=" + str(runid), timeout=self.timeout)
        r.encoding = self.encoding
        match = re.findall(r"<pre>([.\s\S]+?)</pre>", r.text)
        if not match:
            raise NoMatchError("errorinfo")
        return match[0]
