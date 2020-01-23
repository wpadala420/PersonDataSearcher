import bs4
import requests
import re

class FacebookPublicAccountParser:

    def __init__(self):
        self.data = {}
        self.divregex = '<\s*div[^>]*>(.*?)<\s*/\s*div>'
        self.aregex = '<\s*a[^>]*>(.*?)<\s*/\s*a>'
        self.spantag = '<\s*span[^>]*>(.*?)<\s*/\s*span>'


    def search(self, name):
        url = 'https://facebook.com/public/'
        nameAndSurname = name.split(' ')
        firstName = nameAndSurname[0]
        lastName = nameAndSurname[1]
        url = url + firstName + '+' + lastName
        content = requests.get(url).text
        soup = bs4.BeautifulSoup(content, "html.parser")
        linesWithData = []
        with open('fbcontent.txt','wb') as file:
            file.write(bytes(content, encoding='utf-8'))
        with open('fbcontent.txt', 'rb') as file:
            for line in file:
                line = str(line,encoding='utf-8')
                if line.find('hidden_elem') != -1 and line.startswith('<div class="hidden_elem">'):
                    linesWithData.append(line)
        tags = []
        for elem in linesWithData:
            tags.append(re.findall(self.aregex,elem))
            tags.append(re.findall(self.spantag,elem))
            tags.append(re.findall(self.divregex,elem))
        # regex = "[href]=\".*\""
        regex = '<[^>]+?href=["\']([^>]*?)["\']([^>]*?)>(.*?)'
        quotes = []
        for elem in linesWithData:
            quotes.append(re.findall(regex,elem))
        print(quotes)
        # for elem in linesWithData:
        #     for i in range(len(elem)):
        #         if elem[i] == '<':
        #             tag = ''
        #             tag = tag + elem[i]
        #             j = i
        #             while elem[j] != '>':
        #                 tag = tag + elem[j]
        #                 j = j + 1
        #             if elem[j] == '>':
        #                 tag = tag + elem[j]
        #                 tags.append(tag)
        # for tag in tags:
        #     print(tag + '\n')
        # for t in tags:
        #     print(t)

if __name__ == '__main__':
    fb = FacebookPublicAccountParser()
    fb.search('Emil Wrobel')