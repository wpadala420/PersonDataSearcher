from twitter import *
import requests
import modules.Person

class TwitterSearch:

    def __init__(self):
        self.found=[]


    def search(self,name):
        twitter=Twitter(auth=OAuth2(bearer_token=
                                   'AAAAAAAAAAAAAAAAAAAAABGo9gAAAAAAzl3Q%2FxIEmDUOo1i2Mp1x5mExFNU%3DZpz1s3PDGfGxG5AvZhEsgJ4Ocn5puTxsV5kTT9i8HZ8neD36dy'))

        results = twitter.users.search(q='"{}"'.format(name))
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



ts =TwitterSearch()
ts.search('Damian Rusinek')
print(ts.found)