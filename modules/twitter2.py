from twitter import *
import requests
from modules import Person
import shutil
import functions.image_functions


class TwitterSearch:

    def __init__(self):
        self.found=[]


    def search(self,name):
        twitter=Twitter(auth=OAuth( '1107675488498184192-KEyVW29WFdnn16NDeuypy0qUHAog82',
                                   'oFq0J7hHRSkJFpbRWajJE806gZ9jabxH0Cl2En3xKaQRn',
                                    '9ysGguQkraLB0ZGeDb5xPDUQb',
                                   'sLGTfM0dZd2nIcjwzZEXtmhDzOmErr7mcVe9G8V4kxl0qporTM'
                                  ))

         
        results = twitter.users.search(q = '"{}"'.format(name))

        for i in results:
            osoba=Person.Person()
            osoba.setName(i['name'].split(' ')[0])
            if len(i['name'].split(' ')) > 1:
                osoba.setSurname(i['name'].split(' ')[1])

            osoba.twitter['nickname']=i['screen_name']
            osoba.twitter['report']=''
            if i['description'] is not '':
                osoba.twitter['role']=i['description']
            osoba.twitter['url']='https://twitter.com/{}'.format(i['screen_name'])
            osoba.twitter['sites']=[]
            if 'url' in i['entities']:
                for j in i['entities']['url']['urls']:
                    osoba.twitter['sites'].append(j['expanded_url'])
            osoba.twitter['tweets']=[]
            if 'status' in i:
                tweet={}
                if 'created_at' in i['status']:
                    tweet['utworzono']=i['created_at']
                tweet['zawartosc']=i['status']['text']
                if 'user_mentions' in i:
                    tweet['wspomniane_osoby']=[c['screen_name'] for c in i['user_mentions']]
                osoba.twitter['tweets'].append(tweet)
            if 'profile_image_url_https' in i:
                osoba.twitter['profile_image_url'] = i['profile_image_url_https']
            if 'profile_image_url' in osoba.twitter:
                print(osoba.twitter['profile_image_url'])
                try:
                    url = 'tmp/twitter/' + osoba.twitter['nickname']
                    path = functions.image_functions.download_photo(url, osoba.twitter['profile_image_url'], 'profile.jpg')
                    osoba.twitter['profile_img_path'] = path

                except:
                    pass
            self.found.append(osoba)





