from flask import Blueprint, request, jsonify

from warden.model import obtener_session
from warden.model.WardenModel import WardenModel


bp = Blueprint('warden', __name__, url_prefix='/warden/api/v2.0')

@bp.before_app_request
def antes_de_cada_requerimiento():
    pass

@bp.route('/registrar_permisos', methods=['POST'])
def registrar_permisos():
    """
    Registra en la db los permisos enviados desde un sistema
    """
    data = request.json
    assert 'system' in data
    assert 'permissions' in data
    with obtener_session() as session:
        r = WardenModel.register_permissions(session, data)
        session.commit()
        return (str(r), 200)
    


@bp.route('/permisos', methods=['GET'])
def obtener_permisos_disponibles():
    """
    Retorna una lista de todos los permisos disponibles registrados
    """
    with obtener_session() as session:
        #return jsonify(WardenModel.permissions(session))
        _p = WardenModel.permissions(session)
        s = [{'permission':p.permission, 'system':p.system} for p in _p]
        return jsonify(s)

@bp.route('/usuarios/<uid>', methods=['GET'])
def obtener_permisos_usuario(uid=None):
    """
    Retorna la lista de permisos disponibles para ese usuario
    """
    assert uid is not None        
    with obtener_session() as session:
        permisos = WardenModel.permissions_by_uid(session,uid)
        perm = [{'permission':p.permission,'system':p.system} for p in permisos]
        return jsonify(perm)

@bp.route('/usuarios/<uid>', methods=['PUT'])
def actualizar_permisos_usuario(uid=None):
    """
    Actualiza los permisos recibidos por parametro para el uid
    #TODO desarrollar metodo
    """
    data = request.json
    pass


@bp.route('/has_permissions', methods=['POST'])
def has_permissions(token=None):
    """
    Chequea que la el usuario identificado por el token tenga como mínimo los permisos pasados en el requerimineto:
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

