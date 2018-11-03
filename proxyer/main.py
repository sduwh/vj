"""利用多线程，验证代理ip有效性"""
import json
import time
import requests
import threading

# proxy_pool host
host = "localhost"

# 每个线程ip_list的大小
num = 20

# 脚本间歇时间(s)
interval = 60


class ProxyException(Exception):
    pass


def get_all_ip(num) -> list:
    res = requests.get('http://{}:5010/get_all/'.format(host))
    ip_list = json.loads(res.text)
    ip_list_len = len(ip_list)
    i = -1
    if ip_list_len >= num:
        for i in range(ip_list_len // num):
            yield ip_list[i * num:(i + 1) * num]
    yield ip_list[(i + 1) * num:ip_list_len]


def check_ip(ip):
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

    res = requests.get(check_url, proxies=proxy, headers=headers, timeout=5)
    origin = json.loads(res.content).get('origin')
    if origin is None or ',' in origin:
        raise ProxyException("非高匿代理ip")


def del_ip(ip):
    retry = 3
    while retry > 0:
        try:
            requests.get("http://{}:5010/delete/?proxy={}".format(host, ip))
            break
        except:
            retry -= 1


def check_ip_list(ip_list):
    for ip in ip_list:
        retry = 3
        while retry > 0:
            try:
                check_ip(ip)
            except ProxyException:
                retry = 0
                break
            except Exception:
                retry -= 1
            else:
                print(True, ip)
                break
        if retry == 0:
            print(False, ip)
            del_ip(ip)


def check_ip_list_multithreading(num):
    thread_list = []
    for ip_list in get_all_ip(num):
        thread_list.append(threading.Thread(target=check_ip_list, args=(ip_list,)))

    for th in thread_list:
        th.start()

    for th in thread_list:
        th.join()


def main():
    n = 1
    while True:
        print("第{}次".format(n))
        check_ip_list_multithreading(num)
        print("Waiting")
        if n > 3:
            time.sleep(interval * 2)
        else:
            time.sleep(interval)
        n += 1


if __name__ == '__main__':
    main()
