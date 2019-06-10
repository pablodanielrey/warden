from flask import Blueprint, request, jsonify

from warden.model import obtener_session
from warden.model.WardenModel import WardenModel


bp = Blueprint('warden', __name__, url_prefix='/warden/api/v2.0')

@bp.before_app_request
def antes_de_cada_requerimiento():
    pass

@bp.route('/registrar_permisos', methods=['POST'])
def registrar_permisos():
    data = request.json
    assert 'system' in data
    assert 'permissions' in data
    with obtener_session() as session:
        r = WardenModel.register_permissions(session, data)
        session.commit()
        return (str(r), 200)
    


@bp.route('/permisos', methods=['GET'])
def obtener_permisos_disponibles():
    with obtener_session() as session:
        return jsonify(WardenModel.permissions(session))
