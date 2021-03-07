from twitter import *
import requests
import Person
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
            osoba.setSurname(i['name'].split(' ')[1])
            osoba.twitter['nickname']=i['screen_name']
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
                osoba.twitter['profile_image_url']=i['profile_image_url_https']
            self.found.append(osoba)
        for person in self.found:
            if 'profile_image_url' in person.twitter:
                print(person.twitter['profile_image_url'])
                try:
                    functions.image_functions.download_image(person.twitter['profile_image_url'], person.twitter['nickname'] + '.jpg')
                    print(functions.image_functions.get_location_info(person.twitter['nickname'] + '.jpg'))
                except:
                    pass
            print(person)


ts =TwitterSearch()
ts.search('Damian Rusinek')
