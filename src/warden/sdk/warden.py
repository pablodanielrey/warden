
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

    def _has_profiles(self, token, profiles, op):
        headers = self._get_auth_headers()
        data = {
            'token':token,
            'profiles':profiles,
            'op':op
        }
        r = requests.post(self.warden_url + '/profile', verify=self.verify, allow_redirects=False, headers=headers, json=data)
        if r.ok:
            js = r.json()
            return js
        return None

    def has_one_profile(self, token, profiles=[]):
        return self._has_profiles(token, profiles, op='OR')

    def has_all_profiles(self, token, profiles=[]):
        return self._has_profiles(token, profiles, op='AND')
