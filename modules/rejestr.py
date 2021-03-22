import requests
from bs4 import BeautifulSoup
from modules.Person import Person

class RegistrySearcher:

    def __init__(self):
        self.peopleFound=[]

    def startSearch(self,name):
        req = requests.get('https://rejestr.io/api/search.json?page=1&perPage=100&app=&q={}'.format(name))
        dictionary = req.json()
        people = []
        # print(dictionary['total']['value'])
        pagesNumber = int(int(dictionary['total']['value']) / 100)
        if int(dictionary['total']['value']) % 100 > 0:
            pagesNumber = pagesNumber + 1

        for i in range(pagesNumber):
            req = requests.get(
                'https://rejestr.io/api/search.json?page={}&perPage=100&app=&q={}'.format(str(i + 1), name))
            if req.status_code == 200:
                dictionary = req.json()
                print(dictionary['persons'])
                for k in dictionary['persons']['items']:
                    if k['class'] == 'Person' or 'SciencePerson':
                        people.append(k)
            else:
                passed = (i - 1) * 100
                page = (passed / 50) + 1
                for j in range(2):
                    req = requests.get(
                        'https://rejestr.io/api/search.json?page={}&perPage=50&app=&q={}'.format(str(page), name))
                    dictionary = req.json()
                    page = page + 1
                    for k in dictionary['items']:
                        if k['class'] == 'Person' or 'SciencePerson':
                            people.append(k)
        ludzie = []
        for a in people:
            if a['class'] == 'Person':
                person = Person()
                person.setName(a['data']['first_name'])
                if 'birthdate' in a['data']:
                    person.setDateOfBirth(a['data']['birthdate'])
                else:
                    person.setDateOfBirth(str(a['data']['birthday_day']) + '-' + str(a['data']['birthday_month']))
                person.setSurname(a['data']['last_name'])
                krs = {}
                krs['krsId'] = a['data']['krs_id']
                person.addName(a['data']['first_name'])
                if a['data']['second_names']:
                    person.addName(a['data']['second_names'])
                if 'organizations_count' in a['data'] and a['data']['organizations_count'] > 0 :
                    if 'krs' in a['items']['registries'] and 'organizations_shortlist' in  a['data']:
                        organizations = a['data']['organizations_shortlist']
                        orgList = []
                        for o in organizations:
                            orgList.append(o['name_short'])
                        krs['organizations'] = orgList


                        person.addRegistryData(krs)
                        person.setUrl('https://rejestr.io/osoby/{}/{}'.format(a['data']['id'], a['slug']))
                    elif a['data']['registries'].count('ipn') > 0:
                        if 'ipn' in a['items']['registries'] and 'data' in a['items']['registries']['ipn']:
                            ipn={}
                            ipn['birthplace']=a['items']['registries']['ipn']['data']['birthplace']
                            ipn['birthday']=a['items']['registries']['ipn']['data']['birthdate']
                            ipn['father_name']=a['items']['registries']['ipn']['data']['fathers_name']
                            person.addRegistryData(ipn)
                            url='https://rejestr.io/osoby/{}/{}'.format(a['data']['id'],a['slug'])
                            person.setUrl(url)
                for org in person.registries:
                    data = []
                    for name in org['organizations']:
                        found = None
                        if len(dictionary['organizations']['items']) > 0:
                            for it in dictionary['organizations']['items']:
                                if len(it['data']) > 0:
                                    if name == it['data']['name_short']:
                                        found = it['data']
                            data.append(found)
                    org['organizations_data'] = data

                ludzie.append(person)



            elif a['class'] == 'SciencePerson':
                dataDict = a['data']
                person = Person()
                fullName = dataDict['name'].split(' ')
                person.setName(fullName[0])
                person.setSurname(fullName[len(fullName) - 1])
                person.setTitle(dataDict['titles'])
                person.setBranch(dataDict['branches'])
                for i in range(len(fullName)):
                    if i is not len(fullName) - 1:
                        person.addName(fullName[i])
                url = 'https://rejestr.io/nauka/{}/{}'.format(a['data']['id'], a['slug'])
                person.setUrl(url)
                ludzie.append(person)

        return ludzie

    def searchAdditionalData(self):
        for i in self.peopleFound:
            if i.rejestrUrl:
                reg=requests.get(i.rejestrUrl)
                content=reg.content
                soup=BeautifulSoup(content,'html.parser')
                body=soup.body
                addData={}
                elemsKrs=body.find_all('div',{'class' : 'chapter krs mt-2'})
                elemsIpn=body.find_all('div',{'class' : 'chapter ipn mt-2'})

    def searchData(self,name):
        self.peopleFound = self.startSearch(name)
        return self.peopleFound





