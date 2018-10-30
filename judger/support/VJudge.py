"""Virtual Judge"""

import json

from .OJBase import OJ, LoginError, NoMatchError

form_data = {
    'draw': 2,
    'columns[0][data]': 0,
    'columns[0][name]': '',
    'columns[0][searchable]': 'true',
    'columns[0][orderable]': 'false',
    'columns[0][search][value]': '',
    'columns[0][search][regex]': 'false',
    'columns[1][data]': 1,
    'columns[1][name]': '',
    'columns[1][searchable]': 'true',
    'columns[1][orderable]': 'false',
    'columns[1][search][value]': '',
    'columns[1][search][regex]': 'false',
    'columns[2][data]': 2,
    'columns[2][name]': '',
    'columns[2][searchable]': 'true',
    'columns[2][orderable]': 'false',
    'columns[2][search][value]': '',
    'columns[2][search][regex]': 'false',
    'columns[3][data]': 3,
    'columns[3][name]': '',
    'columns[3][searchable]': 'true',
    'columns[3][orderable]': 'false',
    'columns[3][search][value]': '',
    'columns[3][search][regex]': 'false',
    'columns[4][data]': 4,
    'columns[4][name]': '',
    'columns[4][searchable]': 'true',
    'columns[4][orderable]': 'false',
    'columns[4][search][value]': '',
    'columns[4][search][regex]': 'false',
    'columns[5][data]': 5,
    'columns[5][name]': '',
    'columns[5][searchable]': 'true',
    'columns[5][orderable]': 'false',
    'columns[5][search][value]': '',
    'columns[5][search][regex]': 'false',
    'columns[6][data]': 6,
    'columns[6][name]': '',
    'columns[6][searchable]': 'true',
    'columns[6][orderable]': 'false',
    'columns[6][search][value]': '',
    'columns[6][search][regex]': 'false',
    'columns[7][data]': 7,
    'columns[7][name]': '',
    'columns[7][searchable]': 'true',
    'columns[7][orderable]': 'false',
    'columns[7][search][value]': '',
    'columns[7][search][regex]': 'false',
    'columns[8][data]': 8,
    'columns[8][name]': '',
    'columns[8][searchable]': 'true',
    'columns[8][orderable]': 'false',
    'columns[8][search][value]': '',
    'columns[8][search][regex]': 'false',
    'columns[9][data]': 9,
    'columns[9][name]': '',
    'columns[9][searchable]': 'true',
    'columns[9][orderable]': 'false',
    'columns[9][search][value]': '',
    'columns[9][search][regex]': 'false',
    'start': 0,
    'length': 20,
    'search[value]': '',
    'search[regex]': 'false',
    'un': 'sduwhvj',
    'OJId': 'All',
    'probNum': '',
    'res': 0,
    'language': '',
    'onlyFollowee': 'false',
    'orderBy': 'run_id'
}


class VJudge(OJ):

    def login(self):
        self.session.post("https://vjudge.net/user/login", {
            "username": self.username,
            "password": self.password,
        }, headers=self.headers, proxies=self.proxy, timeout=self.timeout)
        r = self.session.get("https://vjudge.net",
                             proxies=self.proxy, timeout=self.timeout)
        r.encoding = r.apparent_encoding
        if self.nickname not in r.text:
            raise LoginError

    def submit(self, soj, sid, language, code):
        r = self.session.post("https://vjudge.net/problem/submit", data={
            "source": code,
            "language": language,
            "share": 0,
            "captcha": "",
            "oj": soj,
            "probNum": sid
        }, headers=self.headers, proxies=self.proxy, timeout=self.timeout)
        return json.loads(r.text)

    def get_last_runid(self):
        r = self.session.post("https://vjudge.net/status/data/", headers=self.headers,
                              proxies=self.proxy, data=form_data, timeout=self.timeout)
        r.encoding = r.apparent_encoding
        match = json.loads(r.text).get('data')
        if not match:
            raise NoMatchError("runid")
        return int(match[0].get('runId'))

    def get_result(self, runid):
        while True:
            try:
                r = self.session.post("https://vjudge.net/solution/data/" + str(
                    runid), headers=self.headers, proxies=self.proxy, data=form_data, timeout=self.timeout)
            except Exception as e:
                self.print_error("获取结果错误", e)
                continue
            r.encoding = r.apparent_encoding
            match = json.loads(r.text)
            if not match:
                raise NoMatchError("result")
            status = match.get('status')
            timeused = match.get('runtime')
            memoryused = match.get('memory')

            return status, timeused, memoryused

    def get_compile_error_info(self, runid):
        while True:
            try:
                r = self.session.post("https://vjudge.net/solution/data/%s" %
                                      str(runid), headers=self.headers, proxies=self.proxy, timeout=self.timeout)

            except Exception as e:
                self.print_error("获得编译信息错误", e)
                continue
            else:
                break
        errorinfo = json.loads(r.text).get('additionalInfo')
        return errorinfo
