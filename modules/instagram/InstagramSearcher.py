from authorize.InstagramAuthorizer import InstagramAuthorizer
import requests
CODE = '4d9243a18b5e47ffa0bb1bae018a2a51'
CLIENT_ID = '0ce8dffab6a44627a46180de9196b7a9'
REDIRECT_URL = 'http://google.com'
CLIENT_SECRET = '2621838516bf4bc48ec15d16fd32bae2'


class InstagramSearcher:

    def __init__(self, client_id, redirect_url, code, secret):
        self.__authorizer = InstagramAuthorizer(client_id, redirect_url, code, secret)


    def access_token(self):
        if self.__authorizer.check_if_token_exists():
            return self.__authorizer.token()
        else:
            self.__authorizer.authorize()
            return self.__authorizer.token()

    def recent_posts(self, user):
        response = requests.get('https://api.instagram.com/v1/users/self/media/recent/?access_token=' + self.access_token())
        print(response.json())
        recent_posts = response.json()
        return recent_posts


if __name__ == '__main__':
    igs = InstagramSearcher(CLIENT_ID, REDIRECT_URL, CODE, CLIENT_SECRET)
    print(igs.recent_posts('wojciech.padala'))



