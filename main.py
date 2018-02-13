import Uther.spider as spider

if __name__ == '__main__':
    url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'
    page = spider.get_page(url)
    time.sleep(5)
    page = spider.get_page(url)

