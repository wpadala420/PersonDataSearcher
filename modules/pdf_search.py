import googlesearch
import os
import requests

def search_pdfs(name):
    query = name + ' filetype:pdf'
    results = googlesearch.search(query)
    return results


def download_pdf(directory, filename, url):
    if os.path.isdir(directory) is False:
        os.mkdir(directory)
    path = directory + '/' + filename
    response = requests.get(url)
    with open(path, 'wb') as pdf:
        pdf.write(response.content)
