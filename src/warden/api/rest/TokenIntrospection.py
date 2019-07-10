import requests
import flask
import logging
from functools import wraps


class TokenIntrospection:

    def __init__(self, oidc_url, verify=False, realm=''):
        self.logging = logging.getLogger('warden')
        self.oidc_url = oidc_url
        self.verify = verify
        self.realm = realm
        self.introspect_url = '{}/oauth2/introspect'.format(self.oidc_url)

    def _bearer_token(self, headers):
        if 'Authorization' in headers:
            auth = headers['Authorization'].split(' ')
            if auth[0].lower() == 'bearer':
                return auth[1]
        return None

    def get_token(self):
        return self._bearer_token(flask.request.headers)

    def get_valid_token(self):
        tk = self.get_token()
        return self._check_valid_token(tk)

    def introspect_token(self, token, scopes=[]):
        data = {
            'token':token
        }
        if len(scopes) > 0:
            data['scope'] = ' '.join(scopes)
        headers = {
            'X-Forwarded-Proto':'https',
            'Accept':'application/json'
        }
        self.logging.debug('data: {}'.format(data))
        r = requests.post(self.introspect_url, verify=self.verify, allow_redirects=False, headers=headers, data=data)
        if not r.ok:
            logging.debug(r)
            return None
        tk = r.json()
        self.logging.debug('tk: {}'.format(tk))
        if not tk or not tk['active']:
            return None
        return tk

    def _check_valid_token(self, token):
        return self.introspect_token(token)

    def _check_token_scopes(self, token, scopes=[]):
        tk = None
        tk = self.introspect_token(token)
        if tk and scopes and len(scopes) > 0:
            tscopes = tk['scope'].lower().split(' ')
            for s in scopes:
                if s not in tscopes:
                    self.logging.warn('scope insuficiente')
                    return None
        return tk

    def require_token_scopes(self, scopes=[]):
        def real_decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                token = self._bearer_token(flask.request.headers)
                self.logging.debug('require_token_scopes: {} {}'.format(token, scopes))
                if not token:
                    return self._invalid_token()
                tk = self._check_token_scopes(token, scopes)
                if not tk:
                    return self._insufficient_scope()
                kwargs['token'] = tk
                return f(*args, **kwargs)
            return wrapper
        return real_decorator

    def require_valid_token(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            '''
                Recupera y chequea el token por validez
            '''
            token = self._bearer_token(flask.request.headers)
            if not token:
                return self._invalid_token()
            tk = self._check_valid_token(token)
            if not tk:
                return self._invalid_request()
            kwargs['token'] = tk
            return f(*args, **kwargs)
        return decorated_function

    def func_require_valid_token(self):
            '''
                Recupera y chequea el token por validez
                usado como función dentro de los requerimientos de flask.
            '''
            token = self._bearer_token(flask.request.headers)
            if not token:
                return 401,None
            tk = self.introspect_token(token)
            if not tk:
                return 400,None
            return 200,tk


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
