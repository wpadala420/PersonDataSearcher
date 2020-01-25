import bs4
import requests
import re
from modules.functions.detail import check_if_link_exist

class FacebookPublicAccountParser:

    def __init__(self):
        self.data = {}
        self.divregex = '<\s*div[^>]*>(.*?)<\s*/\s*div>'
        self.aregex = '<\s*a[^>]*>(.*?)<\s*/\s*a>'
        self.spantag = '<\s*span[^>]*>(.*?)<\s*/\s*span>'


    def __get_profile_links(self, name):
        url = 'https://facebook.com/public/'
        nameAndSurname = name.split(' ')
        firstName = nameAndSurname[0]
        lastName = nameAndSurname[1]
        url = url + firstName + '+' + lastName
        content = requests.get(url).text
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
        regex = '<[^>]+?href=["\']([^>]*?)["\']([^>]*?)>(.*?)'
        quotes = []
        for elem in linesWithData:
            quotes.append(re.findall(regex,elem))
        links = []
        url_regex = '^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&\'\(\)\*\+,;=.]+$'
        for quote in quotes:
            for elem in quote:
                for var in elem:
                    if links.count(var) == 0 and check_if_link_exist(links, var) and re.match(url_regex, var):
                        links.append(var)
        return links


if __name__ == '__main__':
    fb = FacebookPublicAccountParser()
