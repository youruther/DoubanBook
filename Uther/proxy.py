import sqlite3


class Proxy(object):

    def __init__(self):
        print('start proxy')

    def __del__(self):
        print('end proxy')

    def get_proxy(self):
        print('get proxy')


g_proxy = Proxy()
