import datetime

import pymongo

host = "localhost"

client = pymongo.MongoClient('mongodb://{}:27017/'.format(host))
db = client["vj"]
submission = db["submission"]


def insertDict(sid, code, lang):
    data = {'username': 'judgerTest', 'nickname': 'judgerTest', 'soj': 'HDU',
            'runid': None, 'result': 'Queueing', 'timeused': None, 'memoryused': None,
            'errorinfo': '', "sid": str(sid), "code": code, "codesize": len(code),
            'language': str(lang), 'submittime': datetime.datetime.now()}
    submission.insert(data)


def addTestDate(num):
    for i in range(num):
        sid = 1010 + (i % 10)
        code = "-" * (50 + i)
        lang = 0 + (i % 7)
        insertDict(sid, code, lang)


def delTestData():
    db.submission.delete_many({'username': 'judgerTest'})


def main():
    delTestData()
    addTestDate(10)


if __name__ == '__main__':
    main()
