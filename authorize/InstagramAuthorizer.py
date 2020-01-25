from authorize.interface.Authorizer import Authorizer
import requests
from selenium import webdriver
import os


class InstagramAuthorizer(Authorizer):

    def __init__(self, client_id, redirect_url, code, secret):
        self.__base_url = 'https://api.instagram.com/oauth/authorize/'
        self.__client_id = client_id
        self.__redirect_url = redirect_url
        self.__code = code
        self.__client_secret = secret
        self.__auth_dict = {}
        self.__token = ''

    def generate_code(self):
        url = '{0}?client_id={1}&redirect_uri={2}&response_type=code'.format(self.__base_url, self.__client_id, self.__redirect_url)
        driver = webdriver.Firefox(executable_path='C:\\Users\\wpadala\\PycharmProjects\\PersonDataSearcher\\geckodriver.exe')
        driver.get(url)
        elem = driver.current_url
        response = requests.get(url)
        print(elem)

    def check_if_token_exists(self):
        if os.path.exists('token.txt') and os.stat('token.txt').st_size > 0:
            with open('token.txt', 'rb') as file:
                lines = file.readlines()
                for line in lines:
                    if line is not '':
                        self.__token = str(line, encoding='utf-8')
                        return True
        return False

    def authorize(self):
        self.__auth_dict['client_id'] = self.__client_id
        self.__auth_dict['client_secret'] = self.__client_secret
        self.__auth_dict['grant_type'] = 'authorization_code'
        self.__auth_dict['redirect_uri'] = self.__redirect_url
        self.__auth_dict['code'] = self.__code
        response = requests.post('https://api.instagram.com/oauth/access_token', data=self.__auth_dict)
        #print(response.json())
        self.__token = response.json()['access_token']
        with open('token.txt', 'wb') as file:
            file.write(bytes(self.__token, encoding='utf-8'))

    def token(self):
        return self.__token

