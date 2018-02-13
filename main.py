import Uther.spider as spider

if __name__ == '__main__':
    main_url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'
    page = spider.get_page(main_url)


