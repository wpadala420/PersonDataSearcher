import requests

def search_articles(name):
    session = requests.session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:39.0) Gecko/20100101 Firefox/39.0'
    })
    url = 'https://www.etools.ch/partnerSearch.do?partner=Carrot2Json&query={}&dataSourceResults=400&maxRecords=200&safeSearch=true&dataSources=all&language=all&country=web'.format(name)
    data = session.get(url).json()
    return data

