import datetime

DEBUG = True
PORXY_POOL_HOST = "http://192.168.75.111:5010"

def log(msg):
    if DEBUG:
        print("{} {}".format(datetime.datetime.now(), str(msg)))


def main():
    pass

if __name__ == '__main__':
    main()
