import asyncio
import json
import time

import requests

host = "localhost"


def get_all_ip():
    res = requests.get('http://{}:5010/get_all/'.format(host))
    ip_list = json.loads(res.content)
    for ip in ip_list:
        yield ip


@asyncio.coroutine
def check_ip(ip):
    """
    验证ip可用性
    :param ip: str proxy ip
    :return: boolean
    """
    headers = {
        'connection': 'close',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cache-control': "no-cache",
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Mobile Safari/537.36',
    }
    check_url = "http://httpbin.org/ip"
    proxy = {
        'http': ip,
        'https': ip,
    }
    try:
        res = requests.get(check_url, proxies=proxy,
                           headers=headers, timeout=5)
        origin = json.loads(res.content).get('origin')
        if origin is None or ',' in origin:
            raise Exception
        else:
            print('-', True, ip)
            return True
    except Exception:
        print('*', False, ip)
        del_ip(ip)
        return False


def del_ip(ip):
    try:
        requests.get("http://{}:5010/delete/?proxy={}".format(host, ip))
        return True
    except Exception:
        return False


def process():
    loop = asyncio.get_event_loop()
    task = [check_ip(ip) for ip in get_all_ip()]
    loop.run_until_complete(asyncio.wait(task))
    loop.close()


if __name__ == '__main__':
    while True:
        process()
        time.sleep(60)
