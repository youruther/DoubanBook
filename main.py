import Uther.spider as spider
from bs4 import BeautifulSoup
import urllib.parse
import re

__DEBUG__ = True


def find_pattern(pattern, text):
    str_re = re.compile(pattern, re.S)
    result_list = re.findall(str_re, text)
    return result_list


def get_tags_from_main_page(m_page):
    soup = BeautifulSoup(m_page, "lxml")

    m_tags = []
    for m_tag in soup.find_all('a', {'class': 'tag-title-wrapper'}):
        p_text = m_tag.text.replace('·', '').strip()
        if __DEBUG__ and p_text != '科技':
            continue

        c_text = m_tag.next_sibling.next_sibling.text
        pattern = r'\n(.+?)\((.+?)\)\n'
        detail_list = find_pattern(pattern, c_text)

        for detail in detail_list:
            text = detail[0].strip('\n')
            num = int(detail[1])
            m_tags.append([text, num])
    return m_tags


def tag_page_url(m_tag=None, m_page_count=1, m_type='S'):
    __base_url__ = 'https://book.douban.com/tag/'

    if m_tag is None:
        return __base_url__ + '?view=type&icn=index-sorttags-all'
    elif m_page_count == 1:
        tag_url = urllib.parse.quote(m_tag)
        return __base_url__ + tag_url + '?type=' + m_type
    else:
        tag_url = urllib.parse.quote(m_tag)
        return __base_url__ + tag_url + '?start=' + str((m_page_count - 1) * 20) + '&type=' + m_type


if __name__ == '__main__':
    main_url = tag_page_url()
    page = spider.get_page(main_url)
    tags = get_tags_from_main_page(page)

    n_tags = []
    for tag in tags:
        page_count = int(tag[1]) // 20 + 1
        if page_count > 50:
            page_count = 50

        for i in range(1, page_count + 1):
            sub_url = tag_page_url(m_tag=tag[0], m_page_count=i)
            page = spider.get_page(sub_url)
