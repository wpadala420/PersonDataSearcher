from gazpacho import get
from gazpacho import Soup
import bs4
import requests
import argparse
import pyquery


class FacebookPublicAccountParser:

    def __init__(self):
        self.data = {}

    def __init__(self, email, password):
        self.data = {}
        self.email = email
        self.password = password

    def getUrlFromHref(self, href):
        result = ''
        found_first_equal_mark = False
        first_equal_index = -1
        for c in range(len(href)):
            if href[c] == '=' and found_first_equal_mark is False:
                found_first_equal_mark = True
                first_equal_index = c
        if first_equal_index != -1:
            for it in range(first_equal_index + 2, len(href)):
                if href[it] != '"':
                    result += href[it]
                else:
                    return result




    def login(self, session, email, password):
        response = session.get('https://m.facebook.com')
        response = session.post('https://m.facebook.com/login.php', data={
            'email': email,
            'pass': password
        }, allow_redirects=False)
        if 'c_user' in response.cookies:
            homepage_resp = session.get('https://m.facebook.com/home.php')
            dom = pyquery.PyQuery(homepage_resp.text.encode('utf8'))
            fb_dtsg = dom('input[name="fb_dtsg"]').val()

            return fb_dtsg, response.cookies['c_user'], response.cookies['xs']
        else:
            return False

    def nonLoggingSearch(self, name):
        base_url = 'https://m.facebook.com'
        nameAndSurname = name.split(' ')
        firstName = nameAndSurname[0]
        lastName = nameAndSurname[1]
        url = base_url + '/public/' + firstName + '+' + lastName
        cont = get(url, headers={':authority:': 'www.facebook.com', ':method:': 'GET', ':path:': '/public/emil+wróbel',
                                 ':scheme:': 'https',
                                 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                                 'accept-encoding': 'gzip, deflate, br',
                                 'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7', 'cache-control': 'max-age=0',
                                 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'same-origin', 'sec-fetch-user': '?1',
                                 'upgrade-insecure-requests': '1',
                                 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
                                 'viewport-width': '1536'})
        content = requests.get(url).text
        soup = bs4.BeautifulSoup(content, "html.parser")
        linesWithData = []
        hrefs = []
        links = []
        with open('fbcontent.txt', 'wb') as file:
            file.write(bytes(cont, encoding='utf-8'))
        with open('fbcontent.txt', 'rb') as file:
            for line in file:
                line = str(line, encoding='utf-8')
                if line.find('hidden_elem') != -1 and line.startswith('<div class="hidden_elem">'):
                    linesWithData.append(line)
                elif line.find('href="/') != -1:
                    linesWithData.append(line)

        tags = []
        for elem in linesWithData:
            for i in range(len(elem)):
                if elem[i] == '<':
                    tag = ''
                    tag = tag + elem[i]
                    j = i
                    while elem[j] != '>':
                        tag = tag + elem[j]
                        j = j + 1
                    if elem[j] == '>':
                        tag = tag + elem[j]
                        tags.append(tag)
        for tag in tags:
            if tag.find('href') != -1:
                hrefs.append(tag)
        for href in hrefs:
            split = href.split(' ')
            for part in split:
                if part.find('href') != -1 and part.find('https://') == -1 and part.find('=https') == -1 and (part.lower().find(nameAndSurname[0].lower()) != -1 or part.lower().find(nameAndSurname[1].lower()) != -1):
                    corrected_link = self.getUrlFromHref(part)
                    if corrected_link is not None and corrected_link.endswith('/photos') is False:
                        links.append(base_url + corrected_link)
        links = set(links)
        return links

    def loggingSearch(self, name):
        session = requests.session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:39.0) Gecko/20100101 Firefox/39.0'
        })
        a,b,c = self.login(session, self.email, self.password)
        if b:
            print(a + ':' + b + ':' + c)
            links = self.nonLoggingSearch(name)
            count = 0
            for link in links:
                if link.find('people') == -1:
                    print(link.replace('www.', 'm.'))
                    search_query = link.replace('www.', 'm.')
                    new_sess = session.get(search_query)
                    var = new_sess.content
                    var_t = new_sess.text
                    str_var = str(var, encoding='utf-8')
                    # with open( str(count) + '.txt', 'wb') as tmp_file:
                    #     tmp_file.write(bytes(str_var, encoding='utf-8'))
                    #     count += 1
                    # print(str_var)
                    soup = bs4.BeautifulSoup(str_var, 'html.parser')
                    about_tags = soup.find_all()
                    for tag in about_tags:
                        if 'href' in tag:
                            print(tag)
                    # print(about_tags)
                    about_divs = []
                    # for tag in about_tags:
                    #     about_divs.append(tag.find_all('div', {'id': 'profile_intro_card'}))
                    # print(about_divs)
                    pass




if __name__ == '__main__':
    fb = FacebookPublicAccountParser()
    fb.loggingSearch('Emil Wróbel')