class Book(object):
    title = ''
    sub_title = ''
    full_title = ''
    id = ''
    url = ''
    info = ''
    score = 0.0
    people = 0
    introduction = ''

    def __init__(self):
        pass

    def read_from_bs4_tag(self, m_tag):
        # print(m_tag.text)

        self.title = m_tag.contents[1].contents[1].attrs['title']
        self.url = m_tag.contents[1].contents[1].attrs['href']

        self.id = self.url.split('/')[-2]

        if len(m_tag.contents[1].contents[1].contents) > 1:
            self.sub_title = m_tag.contents[1].contents[1].contents[1].text
            self.full_title = self.title + self.sub_title
        else:
            self.sub_title = ''
            self.full_title = self.title

        self.info = m_tag.contents[3].text.replace('\n', '').strip()

        self.score = 0.0
        self.people = 0

        if len(m_tag.contents[5]) > 5:
            temp = m_tag.contents[5].contents[3].text
            if len(temp):
                self.score = float(temp)

            temp = m_tag.contents[5].contents[5].text.replace('\n', '').strip()
            pos = temp.index('人')
            self.people = int(temp[1:pos])

        self.introduction = m_tag.contents[7].text
        return self
