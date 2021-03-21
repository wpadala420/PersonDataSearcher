import requests
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import json
from modules.Person import Person
import os
import urllib3
from instagramPictures import *
from instaloader import *
import time
import functions.image_functions
#from facebookHandler import Account
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import credentials
import bs4


class InstagramSearcher:

    def __init__(self):
        self.peopleFound = []

    def seleniumSearch(self, username, password, url):
        try:
            options = Options()
            # options.headless = True
            options.set_preference('devtools.jsonview.enabled', False)
            # options.add_preference('devtools.jsonview.enabled', False)
            browser = webdriver.Firefox(options=options)
            browser.get(url)
            time.sleep(5)
            elem = browser.find_element_by_xpath("//*[contains(text(), 'Akceptuję')]")
            if elem is not None:
                elem.click()
                time.sleep(3)
                username_field = browser.find_element_by_name('username')
                password_field = browser.find_element_by_name('password')
                username_field.send_keys(username)
                time.sleep(1)
                password_field.send_keys(password)
                time.sleep(3)
                submit = browser.find_element_by_xpath("//button[@type='submit']")
                time.sleep(1)
                submit.click()
                time.sleep(5)
                browser.get(url)
                data = browser.page_source


                soup = bs4.BeautifulSoup(browser.page_source)
                json_elem = soup.find('pre').text
                dict_json = json.loads(json_elem)
                browser.close()
                return dict_json
        except:
            print(Exception.args)
            try:
                soup = bs4.BeautifulSoup(browser.page_source)
                json_elem = soup.find('pre').text
                dict_json = json.loads(json_elem)
                return dict_json
            except:
                return {}

    def search(self, name):
        session = requests.session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:39.0) Gecko/20100101 Firefox/39.0'
        })
        url = 'https://www.instagram.com/web/search/topsearch/?context=blended&query={}-{}&rank_token=0.6093586799873352&include_reel=true'.format(name.split(' ')[0], name.split(' ')[1])
        data = self.seleniumSearch(credentials.instagram_login, credentials.instagram_password,url)
        # data = session.get(url).json()
        j = 0
        for i in data['users']:
            osoba = Person()
            osoba.setName(i['user']['full_name'].split(' ')[0])
            if len(i['user']['full_name'].split(' ')) > 1:
                osoba.setSurname(i['user']['full_name'].split(' ')[1])
            osoba.instagram['login'] = i['user']['username']
            osoba.instagram['url'] = 'https://www.instagram.com/{}'.format(osoba.instagram['login'])
            osoba.instagram['profile_photo']=i['user']['profile_pic_url']
            base_path = 'tmp/instagram/' + osoba.instagram['login']
            if osoba.instagram['profile_photo'] is not None and osoba.instagram['profile_photo'] != '':
                profile_photo_path = functions.image_functions.download_photo(base_path, osoba.instagram['profile_photo'], 'profile.jpg')
                osoba.instagram['profile_photo_path'] = profile_photo_path
            else:
                osoba.instagram['profile_photo_path'] = ''
            osoba.photosNumber += 1
            # if len(profile.get_posts()) >0:
            #     print('wieksze')
            osoba.instagram['posts'] = []
            if i['user']['is_private'] is False:
                try:
                    ip = Instaloader()
                    profile = Profile.from_username(ip.context, osoba.instagram['login'])
                    for p in profile.get_posts():
                        post = {}
                        post['date'] = str(p.date)
                        post['url'] = str(p.url)
                        post['users tagged'] = str(p.tagged_users)
                        post['hashtags'] = str(p.caption_hashtags)
                        if p.location:
                            post['localization'] = str(p.location)
                        if p.location:
                            post['localization'] = str(p.location.name)
                        if p.url is not None:
                            post_path = functions.image_functions.download_photo(base_path, post['url'], post['date'].replace(' ', '') + '.jpg')
                            post['path'] = post_path
                        else:
                            post['path'] = ''
                        osoba.instagram['posts'].append(post)
                        osoba.photosNumber += 1
                except:
                    pass
                time.sleep(2)
            self.peopleFound.append(osoba)
            j += 1

