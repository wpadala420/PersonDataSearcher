class Person(object):

    def __init__(self):
        self.name = ''
        self.names = []
        self.surname = ''
        self.title = ''
        self.branches = []
        self.dateOfBirth = ''
        self.registries = []
        self.rejestrUrl = ''
        self.twitter = {}
        self.instagram = {}
        self.photosNumber = 0
        self.photos = []
        self.linkedin = {}
        self.facebook = {}
        self.imdb = {}
        self.wiki = {}
        self.vindicat_data = []
        self.keywords = []
        self.fb_username_related_accounts = []
        self.twitter_username_connected_profiles = []
        self.instagram_username_related_profiles = []
        self.articles = []

    def setName(self, name):
        self.name=name

    def setSurname(self,surname):
        self.surname=surname

    def setTitle(self,title):
        self.title=title

    def setBranch(self,branch):
        self.branches=branch

    def setDateOfBirth(self,date):
        self.dateOfBirth=date

    def addName(self,name):
        self.names.append(name)

    def addRegistryData(self,data):
        self.registries.append(data)

    def setUrl(self,url):
        self.rejestrUrl=url

    def printData(self):
        print('Imie: {}\n'.format(self.name))
        print('Nazwisko: {}\n'.format(self.surname))
        print('Imiona:')
        for i in self.names:
            print('\t {}'.format(i))
        print('\n')
        print('Data urodzenia: {}\n'.format(self.dateOfBirth))
        if self.title != '':
            print('Tytuł: {}\n'.format(self.title))
        if len(self.branches) is not 0:
            print('Dziedziny: ')
            for d in self.branches:
                print('\t {}'.format(d))
        print('Dane z rejestrów : \n')
        print(self.registries)
        print(self.rejestrUrl)

    def makeKeywords(self):
        if len(self.facebook) > 0:
            for friend in self.facebook['friends']:
                self.keywords.append(friend)
            if len(self.facebook['living_places']) > 0:
                for place in self.facebook['living_places']:
                    for key in place:
                        self.keywords.append(place[key])
            if len(self.facebook['education']) > 0:
                for ed in self.facebook['education']:
                    self.keywords.append(str(ed))
        if len(self.twitter) > 0:
            if 'role' in self.twitter:
                if len(self.twitter['role'].split(' ')) < 4:
                    self.keywords.append(self.twitter['role'])
                for elem in self.twitter['role'].split(' '):
                    if len(elem) > 4:
                        self.keywords.append(elem)



        pass

    def fuze(self, person):
        pass

