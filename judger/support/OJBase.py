"""OJ 基类"""
import requests


class OJ:
    """OJ基类"""

    def __init__(self, account, timeout, time_interval, headers, proxy_ip):
        """初始化 oj"""
        self.username = account["username"]
        self.password = account["password"]
        self.nickname = account["nickname"]
        self.session = requests.Session()
        self.timeout = timeout
        self.time_interval = time_interval
        self.headers = headers
        self.proxy_ip = proxy_ip

    def _login(self):
        """登录
        使用self.ssession登录维持登录状态
        失败抛出LoginException
        """
        raise NotImplemented

    def _submit(self, soj, sid, language, code):
        """提交代码
        使用self.session提交代码等数据
        失败抛出SubmitException
        返回提交结果
        """
        raise NotImplemented

    def _get_last_runid(self):
        """获取本账号最近一次提交记录的runid
        成功返回runid
        失败抛出NoMatchException
        """
        raise NotImplemented

    def _get_result(self, runid):
        """判题结果
        使用runid获取并匹配判题结果
        返回 result timeused memoryused
        匹配不到结果时抛出NoMatchException
        """
        raise NotImplemented

    def _get_compile_error_info(self, runid):
        """编译错误信息
        发生编译错误时 调用该方法使用runid获取并返回远程编译错误信息
        匹配不到信息时抛出NoMatchException
        """
        raise NotImplemented

    def judge(self, soj, sid, language, code):
        """判题
        实现各oj的提交到获得返回信息的过程
        失败抛出JudgeException
        """
        raise NotImplemented


class JudgeException(Exception):
    """判题失败"""
    pass


class LoginException(Exception):
    """登录失败"""
    pass


class SubmitException(Exception):
    """提交失败"""
    pass


class NoMatchException(Exception):
    """没有匹配到数据"""
    pass
