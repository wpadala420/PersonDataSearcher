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



class InstagramSearcher:

    def __init__(self):
        self.peopleFound = []

    def search(self, name):
        session = requests.session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:39.0) Gecko/20100101 Firefox/39.0'
        })
        data = session.get(
            'https://www.instagram.com/web/search/topsearch/?context=blended&query={}-{}&rank_token=0.6093586799873352&include_reel=true'.format(name.split(' ')[0], name.split(' ')[1])).json()
        j = 0
        for i in data['users']:
            print('GOT IT\n')
            osoba = Person()
            osoba.setName(i['user']['full_name'].split(' ')[0])
            if len(i['user']['full_name'].split(' ')) > 1:
                osoba.setSurname(i['user']['full_name'].split(' ')[1])
            osoba.instagram['login'] = i['user']['username']
            osoba.instagram['url'] = 'https://www.instagram.com/{}'.format(osoba.instagram['login'])

            # if os.path.exists('images/' + osoba.name + ' ' + osoba.surname + ' ' + str(j)) is False:
            #     os.mkdir('images/' + osoba.name + ' ' + osoba.surname + ' ' + str(j))

            # photo = open('images/{} {} {}/{}.jpg'.format(osoba.name, osoba.surname, str(j), str(osoba.photosNumber)),
            #              'wb')
            osoba.instagram['profile_photo']=i['user']['profile_pic_url']
            # photo.write(requests.get(i['user']['profile_pic_url']).content)
            # photo.close()
            # osoba.photos.append(photo)
            osoba.photosNumber += 1
            # if len(profile.get_posts()) >0:
            #     print('wieksze')
            osoba.instagram['posts'] = []
            if i['user']['is_private'] is False:
                ip = Instaloader()
                profile = Profile.from_username(ip.context, osoba.instagram['login'])
                for p in profile.get_posts():
                    post = {}
                    post['date'] = str(p.date)
                    post['url'] = str(p.url)
                    post['users tagged'] = str(p.tagged_users)
                    post['hashtags'] =str(p.caption_hashtags)
                    if p.location:
                        post['localization'] =str(p.location)
                    if p.location:
                        post['localization'] = str(p.location.name)

                    osoba.instagram['posts'].append(post)
                    functions.image_functions.download_image(p.url, '{}.jpg'.format(osoba.instagram['login'] + str(osoba.photosNumber)))
                    print(functions.image_functions.get_location_info('{}.jpg'.format(osoba.instagram['login'] + str(osoba.photosNumber))))
                    # photo2 = open(
                    #      '{} {} {}/{}.jpg'.format(osoba.name, osoba.surname, str(j), str(osoba.photosNumber)), 'wb')
                    # photo2.write(requests.get(p.url).content)
                    # photo2.close()
                    # osoba.photos.append(str(photo2))
                    osoba.photosNumber += 1
                time.sleep(2)
            self.peopleFound.append(osoba)
            j += 1

