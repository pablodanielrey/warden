
import requests
from flask import Flask
from oidc.oidc import ClientCredentialsGrant

class Warden:

    def __init__(self, api_url, client_id, client_secret):
        self.verify = True
        self.warden_url = api_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.client_credentials = ClientCredentialsGrant(self.client_id, self.client_secret, self.verify)

    def _get_auth_headers(self):
        r = self.client_credentials.access_token(scopes=['warden'])
        tk = self.client_credentials.get_token(r)
        headers = {
            'Authorization': 'Bearer {}'.format(tk),
            'Accept':'application/json'
        }
        return headers

    def check_access(self, token, resource, action):
        headers = self._get_auth_headers()
        data = {
            'token':token,
            'action':action,
            'resource':resource
        }
        r = requests.post(self.warden_url + '/allowed', verify=self.verify, allow_redirects=False, headers=headers, data=data)
        if r.ok:
            js = r.json()
            if js['allowed'] == True:
                return js
        return None

    def has_profile(self, token, profile):
        headers = self._get_auth_headers()
        data = {
            'token':token,
            'profile':profile
        }
        r = requests.post(self.warden_url + '/profile', verify=self.verify, allow_redirects=False, headers=headers, json=data)
        if r.ok:
            js = r.json()
            if js['profile'] == True:
                return js
        return None
