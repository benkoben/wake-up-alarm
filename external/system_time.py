import time


def current():
    return time.ctime()[11:13] + time.ctime()[14:16]
