class TokenIntrospection:

    def __init__(self, oidc_url, verify=False):
        self.oidc_url = oidc_url
        self.verify = verify
        self.introspect_url = '{}/oauth2/introspect'.format(self.oidc_url)

    def _bearer_token(self, headers):
        if 'Authorization' in headers:
            auth = headers['Authorization'].split(' ')
            if auth[0].lower() == 'bearer':
                return auth[1]
        return None

    def introspect_token(self, token, scopes=[]):
        data = {
            'token':token
        }
        if len(scopes) > 0:
            data['scope'] = ' '.join(scopes)
        headers = {
            'Accept':'application/json'
        }
        r = requests.post(self.introspect_url, verify=self.verify, allow_redirects=False, headers=headers, data=data)
        if not r.ok:
            return None
        tk = r.json()
        if not tk or not tk['active']:
            return None
        return tk

    def require_token_scopes(self, scopes=[]):
        def real_decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                token = self._bearer_token(flask.request.headers)
                if not token:
                    return self._invalid_token()
                tk = self.introspect_token(token)
                if not tk:
                    return self._invalid_request()
                if scopes and len(scopes) > 0:
                    tscopes = tk['scope'].lower().split(' ')
                    for s in scopes:
                        if s not in tscopes:
                            return self.insufficient_scope()
                kwargs['token'] = tk
                #kwargs['access'] = acc
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
            tk = self.introspect_token(token)
            if not tk:
                return self._invalid_request()
            kwargs['token'] = tk
            return f(*args, **kwargs)
        return decorated_function

    def _invalid_request(self):
        return self.require_auth(text='Bad Request', error='invalid_request', status=400)

    def _invalid_token(self):
        return self.require_auth(text='Unauthorized', error='invalid_token', status=401)

    def _insufficient_scope(self):
        return self.require_auth(text='Forbidden', error='insufficient_scope', status=403)

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
