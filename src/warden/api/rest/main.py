import sys
import os
import logging
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().propagate = True

import json
import flask
from flask import Flask, request, send_from_directory, jsonify, redirect, session, url_for, make_response, render_template
from flask_jsontools import jsonapi
from werkzeug.contrib.fixers import ProxyFix

VERIFY_SSL = bool(int(os.environ.get('VERIFY_SSL',0)))
OIDC_ADMIN_URL = os.environ['OIDC_ADMIN_URL']

from .TokenIntrospection import TokenIntrospection
rs = TokenIntrospection(OIDC_ADMIN_URL, verify=VERIFY_SSL)

app = Flask(__name__)
app.debug = False
app.wsgi_app = ProxyFix(app.wsgi_app)

API_BASE = os.environ['API_BASE']

roles = {}
def load_roles():
    r = os.environ['WARDEN_VOLUME_ROOT']
    try:
        with open(r + '/roles.json','r') as f:
            global roles
            roles = json.loads(f.read())
    except FileNotFoundError:
        with open(r + '/roles.json','w') as f:
            roles =  {
                'ej-rol': [
                    { 
                        'id': 'ejemplo-id',
                        'dni': 'ejemplo-dni'
                    }
                ]
            }
            rs = json.dumps(roles)
            f.write(rs)
load_roles()

def find_in_roles(uid, role):
    logging.debug('chequeando uid {} en rol {}'.format(uid, role))
    if role not in roles:
        return False
    uids = (u['id'] for u in roles[role])
    return uid in uids


@app.route(API_BASE + '/allowed', methods=['POST'])
@rs.require_token_scopes(scopes=['warden'])
@jsonapi
def allowed(token=None):
    return {'allowed':False, 'description':'Not implemented'}

@app.route(API_BASE + '/profile', methods=['POST'])
@rs.require_token_scopes(scopes=['warden'])
@jsonapi
def profile(token=None):
    data = request.json
    uid = data['token']['sub']
    one = data['op'] == 'OR'
    ok = False
    if one:
        ''' solo uno tiene que matchear '''
        for p in data['profiles']:
            if find_in_roles(uid, p):
                ok = True
                break
    else:
        ''' todos tienen que matchear '''
        ok = True
        for p in data['profiles']:
            ok = ok & find_in_roles(uid, p)
            if not ok:
                break

    return {
        'profile': ok
    }

@app.route(API_BASE + '/introspect', methods=['POST'])
@rs.require_token_scopes(scopes=['warden'])
@jsonapi
def introspect(token=None):
    data = request.get_json()
    token = data['token']
    scopes = []
    if 'scopes' in data:
        scopes = data['scopes']

    tk = rs.introspect_token(token, scopes)
    return {
        'token': tk
    }


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'

    '''
        para autorizar el CORS
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS
    '''
    """
    o = request.headers.get('Origin', None)
    rm = request.headers.get('Access-Control-Request-Method', None)
    rh = request.headers.get('Access-Control-Request-Headers', None)

    r.headers['Access-Control-Allow-Methods'] = 'PUT,POST,GET,HEAD,DELETE'
    r.headers['Access-Control-Allow-Origin'] = '*'
    if rh:
        r.headers['Access-Control-Allow-Headers'] = rh
    r.headers['Access-Control-Max-Age'] = 1
    """

    return r

def main():
    app.run(host='0.0.0.0', port=10502, debug=False)

if __name__ == "__main__":
    main()
