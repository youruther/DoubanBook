import sqlite3
import os


class Proxy(object):
    cx = None
    cur = None

    def __init__(self):
        proxy_file = "..\\proxy.sqlite"
        if not os.path.isfile(proxy_file):
            print(proxy_file, '不存在')
            raise AssertionError

        self.cx = sqlite3.connect(proxy_file)
        self.cur = self.cx.cursor()

    def __del__(self):
        self.cx.commit()
        self.cur.close()
        self.cx.close()

    def get_proxy(self):
        url = 'SELECT t.IP FROM T_Proxy t WHERE t.Available = \'Y\' ORDER BY RANDOM() LIMIT 1'
        self.cur.execute(url)
        rows = self.cur.fetchall()
        return rows[0][0]


g_proxy = Proxy()
