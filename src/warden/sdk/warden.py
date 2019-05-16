
import requests
from functools import wraps
import flask
from flask import Flask
from oidc.oidc import ClientCredentialsGrant

class Warden:

    def __init__(self, oidc_url, api_url, client_id, client_secret, verify=True, realm=''):
        self.verify = verify
        self.realm = realm
        self.warden_url = api_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.client_credentials = ClientCredentialsGrant(oidc_url, self.client_id, self.client_secret, self.verify)

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


    """
        esquema nuevo de permisos
        el token de consulta a warden se realiza usando el mismo token de usuario
    """
    def has_permissions(self, token, permisos=[]):
        assert token is not None
        headers = {
            'Authorization': 'Bearer {}'.format(token),
            'Accept':'application/json'
        }
        request = {
            'permissions': permisos
        }
        r = requests.post(self.warden_url + '/has_permissions', verify=self.verify, allow_redirects=False, headers=headers, json=request)
        if r.ok:
            js = r.json()
            return js['result']
        return None


    def _get_request_token(self):
        return self._bearer_token(flask.request.headers)

    """
        introspección del token
    """

    def _verify_valid_token(self, token):
        '''
            Recupera y chequea el token por validez
        '''
        if not token:
            return None
        headers = self._get_auth_headers()
        data = {
            'token':token
        }
        r = requests.post(self.warden_url + '/introspect', verify=self.verify, allow_redirects=False, headers=headers, json=data)
        if r.ok:
            js = r.json()
            if js['token']:
                return js['token']

        return None

    def _require_valid_token(self):
        original_token = self._get_request_token()
        tk = self._verify_valid_token(original_token)
        if not tk:
            return original_token, None
        return original_token, tk

    def require_valid_token(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            original_token, tk = self._require_valid_token()
            if not tk:
                return self._invalid_request()
            kwargs['token'] = tk
            #kwargs['original_token'] = original_token
            return f(*args, **kwargs)
        return decorated_function

    def require_valid_token2(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            original_token, tk = self._require_valid_token()
            if not tk:
                return self._invalid_request()
            kwargs['token'] = tk
            kwargs['original_token'] = original_token
            return f(*args, **kwargs)
        return decorated_function


    def _bearer_token(self, headers):
        if 'Authorization' in headers:
            auth = headers['Authorization'].split(' ')
            if auth[0].lower() == 'bearer':
                return auth[1]
        return None

    def _invalid_request(self):
        return self._require_auth(text='Bad Request', error='invalid_request', status=400)

    def _invalid_token(self):
        return self._require_auth(text='Unauthorized', error='invalid_token', status=401)

    def _insufficient_scope(self):
        return self._require_auth(text='Forbidden', error='insufficient_scope', status=403)

    def _require_auth(self, text='Unauthorized', error=None, status=401, error_description=''):
        headers = None
        if error:
            headers = {
                'WWW-Authenticate': 'Basic realm=\"{}\", error=\"{}\", error_description:\"{}\"'.format(self.realm, error, error_description)
            }
        else:
            headers = {
                'WWW-Authenticate': 'Basic realm=\"{}\"'.format(self.realm)
            }
        return (text, status, headers)