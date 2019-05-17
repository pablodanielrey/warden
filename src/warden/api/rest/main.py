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

logger = logging.getLogger('warden')

app = Flask(__name__)
app.debug = False
app.wsgi_app = ProxyFix(app.wsgi_app)

API_BASE = os.environ['API_BASE']

permissions = {}
def _load_permissions():
    """
        comodines:
            * = cualquiera
        permisos disponibles:
            delete (eliminar)
            read (lectura) 
            update (actualización) 
            create (creación)
        scopes:
            any (es el por defecto) = *
            self (recurso propio)
            one (dentro de la misma unidad organizativa)
            sub (sub unidades organizatibas)
            many (sub + one)
            
        restriciones:        
            restricted (restringido por el modelo del sistema)
    """
    logging.debug('cargando permisos')
    r = os.environ['WARDEN_VOLUME_ROOT']
    from . import permisos
    try:
        fp = r + '/permissions.json'
        global permissions
        permissions = permisos.cargar_permisos(fp)
        logging.debug('permisos: {}'.format(permissions))
    except FileNotFoundError as e:
        logger.warn('archivo de permisos no encontrado')
        fp = r + '/permissions.json'
        permisos._generar_ejemplo(fp)
_load_permissions()

roles = {}
def _load_roles():
    logger.debug('cargando roles')
    r = os.environ['WARDEN_VOLUME_ROOT']
    try:
        with open(r + '/roles.json','r') as f:
            global roles
            roles = json.loads(f.read())
            logging.debug('roles: {}'.format(roles))
    except FileNotFoundError as e:
        logger.warn('roles no encontrados, se genera un archivo de ejemplo')
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
_load_roles()

def find_in_roles(uid, role):
    logger.debug('chequeando uid {} en rol {}'.format(uid, role))
    if role not in roles:
        logger.debug('no encontrado')
        return False
    uids = (u['id'] for u in roles[role])
    logger.debug('encontrados: {}'.format(uids))
    return uid in uids

@app.route(API_BASE + '/allowed', methods=['POST'])
@rs.require_token_scopes(scopes=['warden'])
@jsonapi
def allowed(token=None):
    return {'allowed':False, 'description':'Not implemented'}

@app.route(API_BASE + '/permissions', methods=['GET'])
@rs.require_valid_token
@jsonapi
def get_permissions(token=None):
    """
        retorna toda la lista de permisos del usuario asociado con el token
    """
    if not token:
        return {
            'status':400,
            'description': 'no permitido'
        }
    uid = token['sub']
    try:
        resp = {
            'status':200
        }
        perms = []
        if uid in permissions:
            perms.extend(permissions[uid])
        perms.extend(permissions['default'])            
        resp['granted'] = perms
        return resp

    except Exception as e:
        return {
            'stauts':500,
            'description': f'error obteniendo los permisos para {uid}'
        }

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


@app.route(API_BASE + '/has_permissions', methods=['POST'])
@rs.require_valid_token
@jsonapi
def has_permissions(token=None):
    """
        chequea que la el usuario identificado por el token tenga como mínimo los permisos pasados en el requerimineto:
        el formato de la consutla es:
        {
            'permissions': [
                perm1,
                perm2,
                perm3
            ]
        }
        
        formato de respuesta es:
        {
            status: number,
            description: string,
            result: boolean,
            granted: string[]
        }
    """
    assert token is not None
    from . import permisos
    uid = token['sub']
    perms = request.json
    if 'permissions' in perms:
        granted, permissions_granted = permisos.chequear_permisos(uid, perms['permissions'], permissions)
        if granted:
            return {'status':200, 'description':'ok', 'result':granted, 'granted':list(permissions_granted)}
        else:
            return {'status':403, 'description':'forbidden', 'result':granted, 'granted':[]}
    return {'status':500, 'description':'Invalid', 'result':False, 'granted':[]}




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
    o = request.headers.get('Origin', None)
    rm = request.headers.get('Access-Control-Request-Method', None)
    rh = request.headers.get('Access-Control-Request-Headers', None)

    r.headers['Access-Control-Allow-Methods'] = 'PUT,POST,GET,HEAD,DELETE'
    r.headers['Access-Control-Allow-Origin'] = '*'
    if rh:
        r.headers['Access-Control-Allow-Headers'] = rh
    r.headers['Access-Control-Max-Age'] = 1

    return r

"""
@app.route(API_BASE + '/**', methods=['OPTIONS'])
def options():
    if request.method == 'OPTIONS':
        return 204
    return 204
"""

def main():
    app.run(host='0.0.0.0', port=10502, debug=False)

if __name__ == "__main__":
    main()
