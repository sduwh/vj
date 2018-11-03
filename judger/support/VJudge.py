"""Virtual Judge"""

import json
import time
import datetime
from .OJBase import *


class VJudge(OJ):
    """适配VJudge"""

    def __init__(self, account, timeout=3, time_interval=1, headers=None, proxy_ip=None, proxy_host=None):
        """
        初始化VJudge
        :param account: 账号
        :param timeout: 超时
        :param time_interval: 轮询间隔
        :param headers: 标头
        :param proxy_ip: 代理ip
        :param proxy_host: 代理服务地址（proxy_pool)
        """
        OJ.__init__(self, account, timeout, time_interval, headers, proxy_ip)
        self.proxy_host = proxy_host
        self.encoding = 'utf-8'
        self.url = "https://vjudge.net/"

    def _login(self) -> None:
        """
        登陆，获取sessionid
        :return: None
        """
        r = self.session.post('{}user/login'.format(self.url), {
            'username': self.username,
            'password': self.password,
        }, headers=self.headers, timeout=self.timeout)
        r.encoding = self.encoding
        if r.text != 'success':
            raise LoginException('username:{}, password:{}\n响应信息: {}'.format(self.username, self.password, r.text))

    def _submit(self, soj, sid, language, code) -> str:
        """
        提交, 响应字典 {'runId': ''} 或 {'error': ''}
        :param soj: 题目oj名
        :param sid: 题目编号
        :param language: 题目语言
        :param code: 提交代码
        :return: runid
        """
        proxy = {'http': self.proxy_ip} if self.proxy_ip else None
        r = self.session.post("{}problem/submit".format(self.url), data={
            "source": code,
            "language": language,
            "share": 0,
            "captcha": "",
            "oj": soj,
            "probNum": sid
        }, headers=self.headers, proxies=proxy, timeout=self.timeout)
        r.encoding = self.encoding
        res_dict = json.loads(r.text)
        if res_dict.get('runId'):
            runId = res_dict.get('runId')
            return str(runId)
        else:
            raise SubmitException('提交响应错误, 当前代理ip: {}\nres_dict: {}'.format(proxy, res_dict))

    def _get_result(self, runid) -> (str, str, str, str):
        """
        获得结果
        :param runid: 运行id
        :return: 结果信息
        """
        r = requests.get("{}solution/data/{}".format(self.url, str(runid)), headers=self.headers,
                         timeout=self.timeout)
        r.encoding = self.encoding
        match = json.loads(r.text)
        if not match:
            raise NoMatchException("获得结果信息没有匹配")
        else:
            status = match.get('status')
            timeused = match.get('runtime')
            memoryused = match.get('memory')
            errorinfo = match.get('additionalInfo')
            return status, timeused, memoryused, errorinfo

    def judge(self, soj, sid, language, code) -> (str, str, str, str, str):
        """
        核心判题
        :param soj: oj名
        :param sid: 编号
        :param language: 语言
        :param code: 代码
        :return: 结果信息
        """

        # 登陆
        while True:
            time.sleep(self.time_interval)
            try:
                self._login()
            except LoginException as e:
                log(e)
                continue
            except Exception as e:
                log(e)
                self._change_proxy()
                continue
            else:
                log("username: {}, password: {}, 获得sessionid: {}".format(self.username, self.password,
                                                                         self.session.cookies))
                break

        # 提交
        while True:
            time.sleep(self.time_interval)
            try:
                runid = self._submit(soj, sid, language, code)
            except SubmitException as e:
                log(e)
            except Exception as e:
                log(e)
                self._change_proxy()
                continue
            else:
                log("username: {}, oj: {}, id: {}, 获得runid: {}".format(self.username, soj, sid, runid))
                break

        # 获取结果
        while True:
            time.sleep(self.time_interval)
            try:
                result, timeused, memoryused, errorinfo = self._get_result(runid)
            except NoMatchException as e:
                log(e)
                continue
            except Exception as e:
                log(e)
                self._change_proxy()
                continue
            else:
                # 若判题结果为 Waiting / Judging / Compiling / ...
                log('username: {}, oj: {}, id: {}, runid: {}, 当前状态: {}'.format(self.username, soj, sid, runid, result))
                if 'ing' in result or 'Submitted' in result:
                    continue
                else:
                    break

        return runid, result, timeused, memoryused, errorinfo

    def _change_proxy(self):
        """
        更换代理
        :return: None
        """
        if self.proxy_host:
            if self.proxy_ip:
                self._delete_proxy_ip()
            self.proxy_ip = self._get_proxy_ip()

    def _get_proxy_ip(self):
        """
        从proxy_pool获得一个proxy ip
        :return: proxy ip
        """
        return requests.get('http://{}:5010/get/'.format(self.proxy_host)).text

    def _delete_proxy_ip(self):
        """
        让proxy_pool删除一个proxy ip
        :return: None
        """
        requests.get('http://{}:5010/delete/?proxy={}'.format(self.proxy_host, self.proxy_ip))


# 日志
def log(message):
    """
    日志
    :param message: 日志信息
    :return: None
    """
    print("{} {}".format(datetime.datetime.now(), message))
