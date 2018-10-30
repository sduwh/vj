"""oj 基类"""

import time

import requests


class OJ:
    """oj 基类"""

    def __init__(self, account, timeout, time_interval, headers, proxy, db, print_error, print_info):
        """初始化 oj"""
        self.username = account["username"]
        self.password = account["password"]
        self.nickname = account["nickname"]
        self.timeout = timeout
        self.time_interval = time_interval
        self.headers = headers
        self.proxy = proxy
        self.db = db
        self.print_error = print_error
        self.print_info = print_info
        self.session = requests.Session()

    def judge(self, soj, sid, language, code):
        """核心判题方法"""

        # 提交代码
        self.print_info("开始提交 oj： %s, sid: %s, lang: %s" %
                        (soj, sid, language))
        while True:
            try:
                submit_response_dict = self.submit(soj, sid, language, code)
            except Exception as e:
                self.print_error("获取提交失败", e)
                continue
            if submit_response_dict.get('error'):
                if 'login' in submit_response_dict.get('error') or 'captcha' in submit_response_dict.get(
                        'error').lower():
                    # if 'login' in submit_response_dict.get('error'):
                    #     self.print_info("login in submit_response_dict")
                    # elif 'captcha' in submit_response_dict.get('error').lower():
                    #     self.print_info("captcha in submit_response_dict")
                    # self.print_info("开始登陆 user: %s, pwd: %s" %
                    #                 (self.username, self.password))
                    # self.login()
                    # continue
                    raise Exception("captcha")
                self.print_error("提交失败", str(submit_response_dict))
                runid = None
                result = "Submit Fail"
                timeused = None
                memoryused = None
                errorinfo = submit_response_dict.get('error')
                return runid, result, timeused, memoryused, errorinfo
            break
        runid = submit_response_dict.get('runId')
        self.print_info("获得 runid: %s" % runid)

        # 循环获取结果
        # 直到不是Waiting之类的结果
        while True:
            # 获取结果
            time.sleep(self.time_interval)
            result, timeused, memoryused = self.get_result(runid)
            self.print_info("状态: %s" % result)

            # 若判题结果为 Waiting / Judging / Compiling / ...
            # 继续获取
            if "ing" in result:
                time.sleep(1)
                continue
            if "Submitted" in result:
                time.sleep(1)
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

    def submit(self, soj, sid, language, code):
        """提交代码
        使用self.session提交代码等数据
        失败抛出SubmitError
        返回提交结果
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
