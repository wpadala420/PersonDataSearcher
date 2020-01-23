from twitter import *
import requests
from modules.Person import Person
import json
import prettytable

class TwitterSearch:

    def __init__(self):
        self.found=[]


    def search(self,name):

        twitter=Twitter(auth=OAuth('1107675488498184192-Y1HuSpDzYiIza9QWybO6b9cNJyVUu9',
                                   'Jn7MhT9gikbmzpGzCT5I7YUfIoRe8QYoEfB58YkcSs1Mj',
                                   '0hdalkDOqmZ2bbAV1fIPGB6G8',
                                   'lzDpsD6r6yXvPN9BNOnehmvav7BAVIAXFIrhRG9UhlFj6zJpx1'))


        results = twitter.users.search(q = '"{}"'.format(name))
        # for result in results:
        #     print(result)
        it = 0
        for i in results:
            osoba = Person()
            if len(i['name'].split(' ')) > 1:
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
            data = []
            for person in self.found:
                role = ''
                if 'role' in person.twitter:
                    role = person.twitter['role']
                else:
                    role = 'none'
                data.append((role, person.twitter['profile_image_url'], person.twitter['tweets'], person.twitter['nickname'], person.twitter['sites'],person.twitter['url']))
            # if it == len(results) - 1:
            #     pt = prettytable.PrettyTable(field_names=['role', 'img_url', 'tweets', 'nickname', 'twitter_url', 'urls'])
            #     [pt.add_row(row) for row in data]
            #     print(pt)
            it += 1
            for tweet in twitter.statuses.user_timeline(screen_name=osoba.twitter['nickname']):
                print(json.dumps(tweet, indent=1))



if __name__ == '__main__':
    ts = TwitterSearch()
    ts.search('Damian Rusinek')
