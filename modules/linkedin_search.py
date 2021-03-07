from linkedin_v2 import linkedin
import requests, secrets

class LinkedInSearch:

    def __init__(self):
        self.RETURN_URL = 'http://localhost:8000'
        self.ID = '78089tqwivmp7p'
        self.secret = '2BFAmePySISPl6qz'


        url = requests.Request(
            'GET',
            'https://www.linkedin.com/oauth/v2/authorization',
            params={
                'response_type': 'code',
                'client_id': self.ID,
                'redirect_uri': self.RETURN_URL,
                'state': secrets.token_hex(8).upper(),
                'scope': '%20'.join(['r_liteprofile', 'r_emailaddress', 'w_member_social']),
            },
        ).prepare().url

        self.auth = linkedin.LinkedInAuthentication(self.ID, self.secret, self.RETURN_URL, linkedin.PERMISSIONS.enums.values())
        self.app = linkedin.LinkedInApplication(self.auth)
        print(url)
        resp = requests.get(url).content


        if url.find('code=') != -1:
            code_str = url[url.find('code=') + 5 : url.find('&state=')]
            self.auth.authorization_code = code_str
            self.token = self.auth.get_access_token()
            self.app = linkedin.LinkedInApplication(token=self.token.access_token)
            print(self.app.search_profile(params={'keywords': 'Damian Rusinek'}))




linkedin_ = LinkedInSearch()