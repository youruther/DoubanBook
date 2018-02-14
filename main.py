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
        if __DEBUG__ and p_text != '文化':
            continue

        c_text = m_tag.next_sibling.next_sibling.text
        pattern = r'\n(.+?)\((.+?)\)\n'
        detail_list = find_pattern(pattern, c_text)

        for detail in detail_list:
            text = detail[0].strip('\n')
            m_tags.append(text)
    return m_tags


def get_page_from_sub_page(m_page):
    soup = BeautifulSoup(m_page, "lxml")
    m_tag = soup.find('div', {'class': 'paginator'})
    m_text = m_tag.contents[-4].text

    m_count = int(m_text)
    if m_count > 50:
        m_count = 50

    return m_count


def get_book_from_sub_page(m_page):
    soup = BeautifulSoup(m_page, "lxml")

    m_book = []
    m_tags = soup.find_all('div', {'class': 'info'})
    for m_tag in m_tags:
        print(m_tag.text)

        title = m_tag.contents[1].contents[1].attrs['title']
        url = m_tag.contents[1].contents[1].attrs['href']
        if len(m_tag.contents[1].contents[1].contents) > 1:
            sub_title = m_tag.contents[1].contents[1].contents[1].text
        else:
            sub_title = ''

        info = m_tag.contents[3].text.replace('\n', '').strip()

        if len(m_tag.contents[5]) > 5:
            score = m_tag.contents[5].contents[3].text
            people = m_tag.contents[5].contents[5].text.replace('\n', '').strip()
        else:
            score = '?'
            people = '?'

        introduction = m_tag.contents[7].text
        m_book.append([title, sub_title, url, info, score, introduction])

    return m_book


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
        sub_url = tag_page_url(m_tag=tag)
        page = spider.get_page(sub_url)
        count = get_page_from_sub_page(page)
        n_tags.append([tag, count])
        for i in range(2, count + 1):
            sub_url = tag_page_url(m_tag=tag, m_page_count=i)
            page = spider.get_page(sub_url)

    books = []
    for tag in n_tags:
        for i in range(1, tag[1] + 1):
            sub_url = tag_page_url(m_tag=tag[0], m_page_count=i)
            page = spider.get_page(sub_url)
            books.extend(get_book_from_sub_page(page))

