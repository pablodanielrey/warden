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
            any (es el por defecto)
            self (recurso propio)
            one (dentro de la misma unidad organizativa)
            sub (sub unidades organizatibas)
            many (sub + one)
            
        restriciones:        
            restricted (restringido por el modelo del sistema)
    """
    logging.debug('cargando permisos')
    r = os.environ['WARDEN_VOLUME_ROOT']
    try:
        with open(r + '/permissions.json','r') as f:
            global permissions
            permissions = json.loads(f.read())
            logging.debug('permisos: {}'.format(permissions))
    except FileNotFoundError as e:
        logger.warn('archivo de permisos no encontrado')
        with open(r + '/permissions.json', 'w') as f:
            permissions = {
                'uid-1': [
                    'urn:sistema:recurso:permiso:scope:restriccion',
                    'urn:assistance:reporte-marcaciones:read',
                    'urn:assistance:reporte-horarios:*',
                    'urn:assistance:reporte-horarios:read:restricted'
                ],
                'assistance-super-admin': [
                    'urn:assistance:users:read',
                    'urn:assistance:schedule:delete',
                    'urn:assistance:schedule:create',
                    'urn:assistance:logs:create',
                    'urn:assistance:logs:read',
                    'urn:assistance:devices:read',
                    'urn:assistance:justifications:read',
                    'urn:assistance:justifications:create',
                    'urn:assistance:justifications:delete',
                    'urn:assistance:justifications:update',
                    'urn:assistance:justification-date:create',
                    'urn:assistance:justification-date:delete'
                ],
                'default': [
                    'urn:*:*:read:self',
                    'urn:*:*:read:many:restricted',
                    'urn:assistance:users:read:self',
                    'urn:assistance:places:read:many',
                    'urn:assistance:assistance-report:read:many:restricted',
                    'urn:assistance:justifications-report:read:many:restricted',
                    'urn:assistance:general-assistance-report:read:many:restricted',
                    'urn:assistance:schedule:read:many:restricted',
                    'urn:assistance:schedule:read:self',
                    'urn:assistance:justifications:read:many:restricted',
                    'urn:assistance:justification-date:create:many:restricted',
                    'urn:assistance:justification-date:delete:many:restricted',
                    'urn:assistance:justification-date:read:self'                    
                ]
            }
            rs = json.dumps(permissions)
            f.write(rs)
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
        if uid in permissions:
            resp['granted'] = permissions[uid]
        else:
            resp['granted'] = permissions['default']
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


"""
    Obtiene la lista de permisos asociados al usuario identificado por el token.
"""
@app.route(API_BASE + '/all_permissions', methods=['GET'])
@rs.require_valid_token
@jsonapi
def all_permissions(token=None):
    assert token is not None
    uid = token['sub']
    perms = []
    if uid in permissions:
        perms.extend(permissions[uid])
    perms.extend(permissions['default'])
    return perms

"""
    chequea que la el usuario identificado por el token tenga los permisos pasados en el requerimineto:
    {'permissions':[perm1, perm2, perm3]}
"""
@app.route(API_BASE + '/has_permissions', methods=['POST'])
@rs.require_valid_token
@jsonapi
def has_permissions(token=None):
    assert token is not None
    uid = token['sub']
    perms = request.json
    if 'permissions' in perms:
        for perm in perms['permissions']:
            params = perm.split(':')
            
            sistema = params[1]
            recurso = params[2]
            operacion = params[3]
            if len(params) > 4:
                alcance = params[4]
            if len(params) > 5:
                modelo = params[6]
            


    return {'status':500, 'Invalid'}

    perms = []
    if uid in permissions:
        perms.extend(permissions[uid])
    perms.extend(permissions['default'])
    return perms

"""
    parsea el string definido del permiso y retora un diccionario que lo define
"""
def _parsear_permiso(perm):
    arr = perm.split(':')
    ret = {
        'sistema': arr[1],
        'recurso': arr[2],
        'operacion': arr[3],
        'alcance': '*',
        'modelo': '*'
    }
    if len(arr) > 4:
        ret['alcance'] = arr[4]
    if len(arr) > 5:
        ret['modelo'] = arr[5]
    return ret

def _obtener_arbol_permisos(uid):
    if uid not in permissions:
        return None
    for p in permissions[uid]:
        arr = p.split(':')
        sistema = arr[1]
        recurso = arr[2]





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
