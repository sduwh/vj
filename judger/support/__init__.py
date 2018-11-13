"""OJ判题"""

import time
import requests
from .utils import log

class OJ:
    """判题基类"""

    def __init__(self, account, timeout, time_interval, proxy=None):
        """初始化登录会话"""
        self.username = account["username"]
        self.password = account["password"]
        self.nickname = account["nickname"]
        self.timeout = timeout
        self.time_interval = time_interval
        self.proxy = proxy
        self.session = requests.session()

    def judge(self, sid, language, code):
        """核心判题方法"""

        # 登录
        time.sleep(self.time_interval)
        self.login()
        log("username: {}, session: {}".format(self.username, self.session))

        # 提交代码前先获取一下最后一次提交的runid
        time.sleep(self.time_interval)
        runid_old = self.get_last_runid()
        log("获得上一次的runid: {}".format(runid_old))

        # 提交代码
        time.sleep(self.time_interval)
        self.submit(sid, language, code)
        log("提交 sid: {}, lang: {}".format(sid, language))

        # 循环获取最新runid
        # 直到与提交之前最新的runid不同
        n = 0
        while True:
            # 获取最新的runid
            time.sleep(self.time_interval)
            runid = self.get_last_runid()

            # 如果和runid_old不同 说明提交成功 该runid即本次提交的runid
            if runid != runid_old:
                break

            # 记录获取runid的次数
            n += 1

            # 如果获取n次仍没有发现有新的提交记录出现
            # 说明提交失败
            if n == 20:
                raise SubmitError("重试超过{}次".format(n))

        log("获得最新的runid: {}".format(runid))

        # 循环获取结果
        # 直到不是Waiting之类的结果
        while True:
            # 获取结果
            time.sleep(self.time_interval)
            result, timeused, memoryused = self.get_result(runid)
            log("获得结果: {}".format(result))

            # 若判题结果为 Waiting / Judging / Compiling / ...
            # 继续获取
            if "ing" in result:
                continue

            errorinfo = None
            # 如果是编译错误
            # 获取编译错误信息
            if "compil" in result.lower() and "error" in result.lower():
                time.sleep(self.time_interval)
                errorinfo = self.get_compile_error_info(runid)

            # 返回各项结果
            return runid, result, timeused, memoryused, errorinfo

    def login(self):
        """登录
        使用self.ssession登录维持登录状态
        失败抛出LoginError
        """
        raise NotImplementedError

    def submit(self, sid, language, code):
        """提交代码
        使用self.session提交代码等数据
        失败抛出SubmitError
        """
        raise NotImplementedError

    def get_last_runid(self):
        """获取本账号最近一次提交记录的runid
        成功返回runid
        失败抛出NoMatchError
        """
        raise NotImplementedError

    def get_result(self, runid):
        """判题结果
        使用runid获取并匹配判题结果
        返回 result timeused memoryused
        匹配不到结果时抛出NoMatchError
        """
        raise NotImplementedError

    def get_compile_error_info(self, runid):
        """编译错误信息
        发生编译错误时 调用该方法使用runid获取并返回远程编译错误信息
        匹配不到信息时抛出NoMatchError
        """
        raise NotImplementedError


class NoMatchError(Exception):
    """没有匹配到数据"""
    pass


class LoginError(Exception):
    """登录失败"""
    pass


class SubmitError(Exception):
    """提交失败"""
    pass
