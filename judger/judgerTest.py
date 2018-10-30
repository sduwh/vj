import datetime

import pymongo

ip = "192.168.75.129"

client = pymongo.MongoClient('mongodb://{}:27017/'.format(ip))
db = client["vj"]
submission = db["submission"]


def insertDict(sid, code, lang):
    data = {'username': 'judgerTest',
            'nickname': 'judgerTest',
            'soj': 'HDU',
            'sid': '1000',
            'code': '',
            'codesize': 198,
            'language': '0',  # 0 1 2 3 4 5 6
            'runid': None,
            'result': 'Queueing',
            'timeused': None,
            'memoryused': None,
            'submittime': None,
            'errorinfo': ''
            }
    data["sid"] = str(sid)
    data["code"] = code
    data["codesize"] = len(code)
    data["language"] = str(lang)
    data["submittime"] = datetime.datetime.now()
    submission.insert(data)


def addTestDate(num):
    for i in range(num):
        sid = 1000 + (i % 10)
        code = "%" * (1000 + i)
        lang = 0 + (i % 7)
        insertDict(sid, code, lang)


def delTestData():
    db.submission.delete_many({'username': 'judgerTest'})


def main():
    addTestDate(100)
    delTestData()


if __name__ == '__main__':
    main()
