from gazpacho import get
from gazpacho import Soup
import bs4
import requests
import argparse
import pyquery
import time
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
import os
from functions import image_functions
import pickle

class FacebookPublicAccountParser:

    def __init__(self, email=None, password=None):
        self.data = {}
        self.email = email
        self.password = password
        self.people = []

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
        cont = get(url, headers={':authority:': 'www.facebook.com', ':method:': 'GET',
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

    def getFriendsList(self, content):
        friends = []
        friends_soup = bs4.BeautifulSoup(content, 'html.parser')
        elems = friends_soup.find_all('div', {'data-sigil': 'undoable-action'})
        for elem in elems:
            if elem.text.find('Request sent') != -1:
                friends.append(elem.text.split('Request sent')[0])
            else:
                friends.append(elem.text.split('Zaproszenie wysłane')[0])
        return friends

    def getUserNameFromLink(self, link):
        if link.find('.com/') != -1:
            username = ''
            stop = ''
            start = link.find('.com/') + 5
            if link.find('?') != -1:
                stop = link.find('?')
            else:
                stop = len(link) - 1
            for i in range(start, stop):
                username = username + link[i]
            return username
        elif link.find('.pl/') != -1:
            username = ''
            stop = ''
            start = link.find('.pl/') + 4
            if link.find('?') != -1:
                stop = link.find('?')
            else:
                stop = len(link) - 1
            for i in range(start, stop):
                username = username + link[i]
            return username
        else:
            return ''

    def loggingSearch(self, name):
        people = []
        name_val = name.split(' ')[0]
        surname_val = name.split(' ')[1]
        year_regex = '[0-9][0-9][0-9][0-9]'
        session = requests.session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:39.0) Gecko/20100101 Firefox/39.0'
        })
        webdriver_logging = False
        try:
            a, b, c = self.login(session, self.email, self.password)
        except TypeError:
            print('Nieprawidłowe dane do logowania lub niepowodzenie logowania, próba logowania przez webdriver\n')
            webdriver_logging = True
            b = None
        time.sleep(3)
        links = self.nonLoggingSearch(name)
        count = 0
        for link in links:
            person = {}
            person['name'] = name_val
            person['surname'] = surname_val
            person['facebook'] = {}

            if link.find('people') == -1:
                print(link.replace('www.', 'm.'))
                search_query = link.replace('www.', 'm.')
                if b:
                    print(a + ':' + b + ':' + c)
                    new_sess = session.get(search_query)
                    var = new_sess.content
                    var_t = new_sess.text
                    str_var = str(var, encoding='utf-8')
                    with open('main_page.txt', 'wb') as tmp_file:
                        tmp_file.write(bytes(str_var, encoding='utf-8'))
                elif webdriver_logging:
                    str_var = self.getProfileContent(search_query)
                    with open('main_page.txt', 'wb') as tmp_file:
                        tmp_file.write(bytes(str_var, encoding='utf-8'))
                # ----------------------------------------------------------------------
                # friends
                friends_url = self.getFriendsUrl('main_page.txt')
                friends_content = self.getFriendsContent(friends_url)
                person['facebook']['friends'] = self.getFriendsList(friends_content)

                # ---------------------------------------------------------------------
                about = self.getAboutUrl('main_page.txt')
                # print(about)
                time.sleep(2)
                cont = None
                if b:
                    cont = session.get(about).content
                elif webdriver_logging:
                    cont = self.getAboutContent(about)
                soup2 = bs4.BeautifulSoup(cont, 'html.parser')
                edu = soup2.find_all('div', {'id': 'education'})
                # --------------------------------------------------------------------
                # education
                edu_names = []
                durations = []
                texts = soup2.a.contents
                for edu_tag in edu:
                    tags_ = edu_tag.find_all('div', {'class': 'experience'})
                    for t in tags_:
                        name = ()
                        a_tags = t.find_all('a')
                        spans = t.find_all('span')
                        for txts in a_tags:
                            if txts.text is not None and txts.text != '' and not re.search(year_regex, txts.text):
                                edu_names.append(txts.text)
                                # for span in spans:
                                #     if re.search(year_regex, span.text):
                                #         durations.append(span.text)
                                #         break

                    tags_ = edu_tag.find_all('span')
                    for span in tags_:
                        if span.text != 'High School' and span.text != 'College' and not re.search(year_regex,
                                                                                                   span.text):
                            edu_names.append(span.text)
                    # for span in tags_:
                    #     if re.search(year_regex, span.text):
                    #         durations.append(span.text)
                edu_names = set(edu_names)
                person['facebook']['education'] = edu_names
                # for dur in durations:
                #     print(dur)
                # ----------------------------------------------------------------------------
                # living
                living_places = []
                living = soup2.find_all('div', {'id': 'living'})
                for living_elem in living:
                    data_elems = living_elem.find_all('div', {'class': '_2swz _2lcw'})
                    for data_elem in data_elems:
                        if data_elem.text.find('Hometown') != -1:
                            living_dict = {'Hometown': data_elem.text.split('Hometown')[0]}
                            living_places.append(living_dict)
                        elif data_elem.text.find('Current City') != -1:
                            living_dict = {'Current City': data_elem.text.split('Current City')[0]}
                            living_places.append(living_dict)

                person['facebook']['living_places'] = living_places
                # ------------------------------------------------------------------------------
                # relationship
                relationship = []
                relationship_elem = soup2.find_all('div', {'id': 'relationship'})
                for r_elem in relationship_elem:
                    relat_elem = r_elem.find_all('div', {'class': '_4g34'})
                    for elem in relat_elem:
                        if elem.text.find('In a relationship') != -1:
                            relathionship_dict = {'with': elem.text.split('In a relationship')[0],
                                                  'date': elem.text.split('In a relationship')[1]}
                            relationship.append(relathionship_dict)
                person['facebook']['relationship'] = relationship
                # ---------------------------------------------------------------------------------
                # family
                family = []
                family_elem = soup2.find_all('div', {'id': 'family'})
                for f_elem in family_elem:
                    members = f_elem.find_all('div', {'data-sigil': 'touchable'})
                    for member in members:
                        names = member.find_all('span')
                        roles = member.find_all('h3')
                        name_val = ''
                        role_val = ''
                        for name in names:
                            if name.text != '':
                                name_val = name.text
                        for role in roles:
                            if role.text != '' and role.text != name_val:
                                role_val = role.text
                        family_member = {'name': name_val, 'role': role_val}
                        family.append(family_member)
                # -----------------------------------------------------------------------------
                # friends url

                print(person)
                people.append(person)
        return people
                # about_content = str(cont, encoding='utf-8')
                # with open('about.txt', 'wb') as about_file:
                #     about_file.write(bytes(about_content, encoding='utf-8'))
                #
                # print(self.getAboutData())
                # time.sleep(5)

    def loggingSearchNew(self, name):
        people = []
        name_val = name.split(' ')[0]
        surname_val = name.split(' ')[1]
        year_regex = '[0-9][0-9][0-9][0-9]'
        session = requests.session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:39.0) Gecko/20100101 Firefox/39.0'
        })
        webdriver_logging = False
        parse_data = []
        try:
            a, b, c = self.login(session, self.email, self.password)
        except TypeError:
            print('Nieprawidłowe dane do logowania lub niepowodzenie logowania, próba logowania przez webdriver\n')
            webdriver_logging = True
            b = None
        time.sleep(5)
        links = self.nonLoggingSearch(name)
        new_links = []
        for link in links:
            if link.find('people') == -1:
                link = link.replace('www.', 'm.')
                new_links.append(link)
        links = new_links
        count = 0
        usernames = []
        browser = self.loginSelenium()
        if b is None:
            b = ''
        if b:
            general_contents = []
            about_contents = []
            friends_contents = []
            profile_photos_urls = []
            profile_photos_direct_urls = []
            if a is None:
                a = ''
            if b is None:
                b = ''
            if c is None:
                c = ''


            for link in links:
                time.sleep(10)
                str_var = self.getProfileContent(browser, link)
                general_contents.append(str_var)
                with open('main_page.txt', 'wb') as tmp_file:
                    tmp_file.write(bytes(str_var, encoding='utf-8'))
                username = self.getUserNameFromLink(link)
                usernames.append(username)
                # if link.find('emil.wrobel.90') != -1:
                #     print('tak')
                profile_photo_url = self.getProfilePhotoUrl('main_page.txt')
                profile_photos_urls.append(profile_photo_url)
                time.sleep(5)
                profile_photo_content = self.getProfilePhotoContent(browser, profile_photo_url)
                direct_url = self.getProfilePhotoDirectUrl(profile_photo_content)
                profile_photos_direct_urls.append(direct_url)
                friends_url = self.getFriendsUrl('main_page.txt')
                time.sleep(5)
                friends_content = self.getFriendsContent(browser, friends_url)
                friends_contents.append(friends_content)
                about_url = self.getAboutUrl('main_page.txt')
                if(about_url is not None):
                    time.sleep(5)
                    about_content = self.getAboutContent(browser, about_url)
                    about_contents.append(about_content)
                time.sleep(15)

            for i in range(0, len(general_contents)):
                general = None
                about = None
                friends = None
                if i < len(general_contents):
                    general = general_contents[i]
                else:
                    general = None
                if i < len(about_contents):
                    about = about_contents[i]
                else:
                    about = None
                if i < len(friends_contents):
                    friends = friends_contents[i]
                else:
                    friends = None
                profile_photo_url = ''
                profile_photo_direct_url = ''
                if profile_photo_url is None:
                    profile_photo_url = ''
                else:
                    if i < len(profile_photos_urls):
                        profile_photo_url = profile_photos_urls[i]
                if i < len(profile_photos_direct_urls):
                    profile_photo_direct_url = profile_photos_direct_urls[i]
                data = {'general': general, 'about': about, 'friends': friends, 'profile_photo_url': profile_photo_url, 'profile_photo_direct_url': profile_photo_direct_url}
                parse_data.append(data)
        else:
            general_contents, about_contents, friends_contents, profile_photo_urls = self.getAllContentsByWebdriver(browser, links)
            for link in links:
                usernames.append(self.getUserNameFromLink(link))
            for i in range(0, len(general_contents)):
                profile_photo_direct_url = ''
                if profile_photo_urls[i] is not None and profile_photo_urls[i] != '':
                    profile_photo_content = self.getProfilePhotoContent(browser, profile_photo_urls[i])
                    direct_url = self.getProfilePhotoDirectUrl(profile_photo_content)
                    profile_photo_direct_url = direct_url
                data = {'general': general_contents[i], 'about': about_contents[i], 'friends': friends_contents[i], 'profile_photo_url': profile_photo_urls[i], 'profile_photo_direct_url': direct_url}
                parse_data.append(data)
        with open('parse_data2.dump', 'wb') as parse_data_dump:
            pickle.dump(parse_data, parse_data_dump)

        # with open('parse_data2.dump', 'rb') as dump:
        #     parse_data = pickle.load(dump)
        user_iter = 0
        for link in parse_data:
            person = {}

            person['facebook'] = {}
            person['facebook']['name'] = name_val
            person['facebook']['surname'] = surname_val
            person['facebook']['friends'] = self.getFriendsList(link['friends'])
            if user_iter < len(usernames):
                person['facebook']['username'] = usernames[user_iter]

            else:
                person['facebook']['username'] = ''
            directory_name = ''
            if person['facebook']['username'] != '':
                directory_name = person['facebook']['username']
            else:
                directory_name = person['facebook']['name'] + '_' + person['facebook']['surname'] + str(user_iter)
            user_iter += 1
            person['facebook']['photos_directory'] = 'tmp/facebook/' + directory_name

            if 'profile_photo_direct_url' in link:
                person['facebook']['profile_photo_direct_url'] = link['profile_photo_direct_url']
            else:
                person['facebook']['profile_photo_direct_url'] = ''

            if person['facebook']['profile_photo_direct_url'] != '':
                person['facebook']['profile_photo_path'] = image_functions.download_photo(person['facebook']['photos_directory'], person['facebook']['profile_photo_direct_url'], 'profile_photo.jpg' )
            # ---------------------------------------------------------------------
            about = self.getAboutUrl('main_page.txt')
            # print(about)
            time.sleep(2)
            cont = None
            if 'about' in link and link['about'] is None:
                link['about'] = ''
            photos_url = self.getPhotosUrls(link['about'])
            person['facebook']['photos'] = []
            person['facebook']['photos_direct'] = []
            for photo_url in photos_url:
                person['facebook']['photos'].append(photo_url)
                photo_content = self.getProfileContent(browser, photo_url)
                person['facebook']['photos_direct'].append(self.getPhotoDirectUrl(photo_content))
                time.sleep(3)
            person['facebook']['photos_paths'] = []
            it = 0
            for photo in person['facebook']['photos_direct']:
                person['facebook']['photos_paths'].append(image_functions.download_photo(person['facebook']['photos_directory'], photo, str(it) + '.jpg'))
                it += 1




            soup2 = bs4.BeautifulSoup(link['about'], 'html.parser')
            edu = soup2.find_all('div', {'id': 'education'})
            # --------------------------------------------------------------------
            # education
            edu_names = []
            durations = []
            # texts = soup2.a.contents
            for edu_tag in edu:
                tags_ = edu_tag.find_all('div', {'class': 'experience'})
                for t in tags_:
                    name = ()
                    a_tags = t.find_all('a')
                    spans = t.find_all('span')
                    for txts in a_tags:
                        if txts.text is not None and txts.text != '' and not re.search(year_regex, txts.text):
                            edu_names.append(txts.text)
                            edu_found = True
                            # for span in spans:
                            #     if re.search(year_regex, span.text):
                            #         durations.append(span.text)
                            #         break

                tags_ = edu_tag.find_all('span')
                for span in tags_:
                    if span.text != 'High School' and span.text != 'College' and not re.search(year_regex,
                                                                                               span.text):
                        edu_names.append(span.text)
                # for span in tags_:
                #     if re.search(year_regex, span.text):
                #         durations.append(span.text)
            edu_names = set(edu_names)
            person['facebook']['education'] = edu_names
            # for dur in durations:
            #     print(dur)
            # ----------------------------------------------------------------------------
            # living
            living_places = []
            living = soup2.find_all('div', {'id': 'living'})
            for living_elem in living:
                data_elems = living_elem.find_all('div', {'class': '_2swz _2lcw'})
                for data_elem in data_elems:
                    if data_elem.text.find('Hometown') != -1:
                        living_dict = {'Hometown': data_elem.text.split('Hometown')[0]}
                        living_places.append(living_dict)
                    elif data_elem.text.find('Current City') != -1:
                        living_dict = {'Current City': data_elem.text.split('Current City')[0]}
                        living_places.append(living_dict)

            person['facebook']['living_places'] = living_places
            # ------------------------------------------------------------------------------
            # relationship
            relationship = []
            relationship_elem = soup2.find_all('div', {'id': 'relationship'})
            for r_elem in relationship_elem:
                relat_elem = r_elem.find_all('div', {'class': '_4g34'})
                found = False
                for elem in relat_elem:
                    if elem.text.find('In a relationship') != -1:
                        relathionship_dict = {'with': elem.text.split('In a relationship')[0],
                                              'date': elem.text.split('In a relationship')[1]}
                        relationship.append(relathionship_dict)
                        found = True
                if found is False:
                    relat_elem = r_elem.find_all('header')
                    for head in relat_elem:
                        if head.text.find('In a relationship') != -1:
                            relathionship_dict = {'with': head.text.split('In a relationship')[0],
                                                  'date': head.text.split('In a relationship')[1]}
                            relationship.append(relathionship_dict)

            person['facebook']['relationship'] = relationship
            # ---------------------------------------------------------------------------------
            # family
            family = []
            family_elem = soup2.find_all('div', {'id': 'family'})
            for f_elem in family_elem:
                members = f_elem.find_all('div', {'data-sigil': 'touchable'})
                for member in members:
                    names = member.find_all('span')
                    roles = member.find_all('h3')
                    family_name_val = ''
                    role_val = ''
                    for name in names:
                        if name.text != '':
                            family_name_val = name.text
                    for role in roles:
                        if role.text != '' and role.text != family_name_val:
                            role_val = role.text
                    family_member = {'name': family_name_val, 'role': role_val}
                    family.append(family_member)
            # -----------------------------------------------------------------------------
            # friends url

            print(person)
            people.append(person)
        browser.close()
        return people

                # about_content = str(cont, encoding='utf-8')
                # with open('about.txt', 'wb') as about_file:
                #     about_file.write(bytes(about_content, encoding='utf-8'))
                #
                # print(self.getAboutData())
                # time.sleep(5)


    def getAboutUrl(self, filename):
        base_url = 'https://m.facebook.com'
        with open(filename, 'rb') as data:
            for line in data:
                if str(line, encoding='utf-8').find('about') != -1:
                    for split_line in str(line, encoding='utf-8').split('><'):
                        if split_line.find('about') != -1 and split_line.find('href="/') != -1:
                            for selector in split_line.split(' '):
                                if selector.find('href') != -1:
                                    return base_url + self.getUrlFromHref(selector)


    def getFriendsUrl(self, filename):
        base_url = 'https://m.facebook.com'
        with open(filename, 'rb') as data:
            for line in data:
                if str(line, encoding='utf-8').find('friends') != -1:
                    for split_line in str(line, encoding='utf-8').split('><'):
                        if split_line.find('friends?') != -1 and split_line.find('href="/') != -1:
                            for selector in split_line.split(' '):
                                if selector.find('href') != -1:
                                    return base_url + self.getUrlFromHref(selector)

    def getProfilePhotoUrl(self, filename):
        base_url = 'https://m.facebook.com'
        with open(filename, 'rb') as data:
            for line in data:
                if str(line, encoding='utf-8').find('photo.php?') != -1 and str(line, encoding='utf-8').find('profile picture') != -1:
                    split = str(line, encoding='utf-8').split('><div id')
                    for split_line in split:
                        if split_line.find('photo.php?') != -1 and split_line.find('href="/') != -1 and split_line.find('profile picture') != -1:
                            selectors = split_line.split(' ')
                            previous = selectors[0]
                            for selector in selectors:
                                if selector.find('href') != -1 and previous.find('cover-photo') == -1:
                                    return base_url + self.getUrlFromHref(selector)
                                previous = selector

    def getProfilePhotoContent(self, browser, url):
        try:
            if url is not None:
                time.sleep(7)
                browser.get(url)
                time.sleep(10)
                content = browser.execute_script("return document.documentElement.outerHTML;")
                return content
            else:
                return ''
        except:
            return ''

    def getPhotosUrls(self, about_content):
        base_url = 'https://m.facebook.com'
        hrefs = []
        soup = bs4.BeautifulSoup(about_content, 'html.parser')
        cols = soup.findAll('div', {'class': 'croppedPhotoGridCol'})
        for col in cols:
            a_tags = col.find_all('a')
            for a in a_tags:
                if a['href'] is not None and a['href'].find('photo') != -1:
                    href = base_url + a['href']
                    hrefs.append(href)
        return hrefs

    def getProfilePhotoDirectUrl(self, content):
        soup = bs4.BeautifulSoup(content, 'html.parser')
        rootcontainers = soup.find_all('div', {'id': 'rootcontainer'})
        for rcontainer in rootcontainers:
            img = rcontainer.find_all('i')
            for i in img:
                try:
                    if i['data-store'] is not None and i['data-store'].find('"imgsrc":') != -1:
                        data_json = json.loads(i['data-store'])
                        raw_url = str(data_json['imgsrc'])
                        return raw_url
                except:
                    return ''
        return ''

    def getPhotoDirectUrl(self, content):
        soup = bs4.BeautifulSoup(content, 'html.parser')
        rootcontainers = soup.find_all('div', {'id': 'rootcontainer'})
        for rcontainer in rootcontainers:
            img = rcontainer.find_all('i')
            for i in img:
                try:
                    if i['data-store'] is not None and i['data-store'].find('"imgsrc":') != -1:
                        data_json = json.loads(i['data-store'])
                        raw_url = str(data_json['imgsrc'])
                        return raw_url
                except:
                    return ''
        return ''


    def getProfileContent(self, browser, url):
        try:
            time.sleep(7)
            browser.get(url)
            time.sleep(10)
            content = browser.execute_script("return document.documentElement.outerHTML;")
            return content
        except:
            print('Błąd wyszukiwania za pomocą webdrivera\n')

    def loginSelenium(self):
        try:
            options = Options()
            options.headless = True
            browser = webdriver.Firefox()
            browser.get('https://m.facebook.com/login.php')
            time.sleep(5)
            submit = browser.find_element_by_id("accept-cookie-banner-label")
            submit.click()
            time.sleep(10)
            email = browser.find_element_by_id('m_login_email')
            password = browser.find_element_by_id('m_login_password')
            email.send_keys(self.email)
            password.send_keys(self.password)
            submit = browser.find_element_by_name('login')
            submit.click()
            time.sleep(10)
            not_now = browser.find_element_by_class_name('_2pii')
            not_now.click()
            time.sleep(7)
            return browser
        except:
            return None



    def getFriendsContent(self, browser, url):
        try:
            if url is not None:
                time.sleep(7)
                browser.get(url)
                last_height = browser.execute_script('return document.body.scrollHeight')
                browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(5)
                new_height = browser.execute_script('return document.body.scrollHeight')
                while new_height != last_height:
                    last_height = new_height
                    browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    time.sleep(5)
                    new_height = browser.execute_script('return document.body.scrollHeight')

                content = browser.execute_script("return document.documentElement.outerHTML;")
                return content
            else:
                return ''
        except:
            return ''

    def getAboutContent(self, browser,  url):
        try:
            time.sleep(7)
            browser.get(url)
            last_height = browser.execute_script('return document.body.scrollHeight')
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(5)
            new_height = browser.execute_script('return document.body.scrollHeight')
            while new_height != last_height:
                last_height = new_height
                browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(5)
                new_height = browser.execute_script('return document.body.scrollHeight')

            content = browser.execute_script("return document.documentElement.outerHTML;")
            return content
        except:
            return ''

    def getAllContentsByWebdriver(self, browser, links):
        general_urls = []
        about_contents = []
        friends_contents = []
        profile_photo_urls = []
        try:
            time.sleep(7)
            for link in links:
                browser.get(link)
                time.sleep(7)
                last_height = browser.execute_script('return document.body.scrollHeight')
                browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(5)
                new_height = browser.execute_script('return document.body.scrollHeight')
                while new_height != last_height:
                    last_height = new_height
                    browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    time.sleep(5)
                    new_height = browser.execute_script('return document.body.scrollHeight')
                content = browser.execute_script("return document.documentElement.outerHTML;")
                general_urls.append(content)
                with open('main_page.txt', 'wb') as tmp_file:
                    tmp_file.write(bytes(content, encoding='utf-8'))
                profile_photo_url = self.getProfilePhotoUrl('main_page.txt')
                if profile_photo_url is None:
                    profile_photo_url = ''
                profile_photo_urls.append(profile_photo_url)
                about = self.getAboutUrl('main_page.txt')
                friends = self.getFriendsUrl('main_page.txt')
                time.sleep(10)
                browser.get(about)
                last_height = browser.execute_script('return document.body.scrollHeight')
                browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(5)
                new_height = browser.execute_script('return document.body.scrollHeight')
                while new_height != last_height:
                    last_height = new_height
                    browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    time.sleep(5)
                    new_height = browser.execute_script('return document.body.scrollHeight')
                content = browser.execute_script("return document.documentElement.outerHTML;")
                about_contents.append(about)
                time.sleep(5)
                browser.get(friends)
                last_height = browser.execute_script('return document.body.scrollHeight')
                browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(5)
                new_height = browser.execute_script('return document.body.scrollHeight')
                while new_height != last_height:
                    last_height = new_height
                    browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    time.sleep(5)
                    new_height = browser.execute_script('return document.body.scrollHeight')
                content = browser.execute_script("return document.documentElement.outerHTML;")
                friends_contents.append(content)
                time.sleep(10)
            return general_urls, about_contents, friends_contents, profile_photo_urls
        except:
            return [], [], []

    def getAboutData(self, filename):
        education = []

        with open(filename, 'rb') as data:
            for line in data:
                pass
        pass



