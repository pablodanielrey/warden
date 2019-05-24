import pytest

"""
TEST ---> Se van a chequear permisos obtenidos al consultar UIDS ficticias:
        Equivalencias:
        1 == AssistanceSuperAdmin
        2 == AssistanceAdmin
        3 == AssistanceOperator
        4 == AssistanceUser
        5 == Default
"""

prefijos = ['urn']
sistemas = ['assistance']
recursos = ['users','places','assistance-report','schedule','justifications','justifications-date','justifications-report','general-assistance-report','devices','logs','*']
operaciones = ['create','read','update','delete','*']
alcances = ['any','many', 'sub', 'one', 'self','*']
modelos = ['restricted']

permisos = {
        "sadm": [
            "urn:assistance:*"
        ],
        "1": [
            "urn:assistance:users:read",
            "urn:assistance:places:read",
            "urn:assistance:schedule:delete",
            "urn:assistance:schedule:create",
            "urn:assistance:logs:create",
            "urn:assistance:logs:read",
            "urn:assistance:devices:read",
            "urn:assistance:justifications:read",
            "urn:assistance:justifications:create",
            "urn:assistance:justifications:delete",
            "urn:assistance:justifications:update",
            "urn:assistance:justification-date:create",
            "urn:assistance:justification-date:delete"
        ],
        "2": [
            "urn:assistance:users:read",
            "urn:assistance:places:read",
            "urn:assistance:schedule:delete"
        ],
        "3": [
            "urn:assistance:users:read",
            "urn:assistance:places:read"
        ],
        "4": [
            "urn:assistance:users:read",
            "urn:assistance:places:read"
        ],
        "default": [
            "urn:assistance:*:*:*",
            "urn:assistance:users:read:self",
            "urn:assistance:users:read:many:restricted",
            "urn:assistance:places:read:many",
            "urn:assistance:assistance-report:read:many:restricted",
            "urn:assistance:justifications-report:read:many:restricted",
            "urn:assistance:general-assistance-report:read:many:restricted",
            "urn:assistance:schedule:read:self",
            "urn:assistance:schedule:read:many:restricted",
            "urn:assistance:justifications:read:many:restricted",
            "urn:assistance:justifications-date:read:self",
            "urn:assistance:justifications-date:create:many:restricted",
            "urn:assistance:justifications-date:delete:many:restricted",
                        
        ]
    }


def test_default():
    import warden.api.rest.permisos as p

    ''' Comprobacion permisos de usuario default
    Permisos de un usuario default:
    "urn:assistance:users:read:self",
    "urn:assistance:users:read:many:restricted",
    "urn:assistance:places:read:many",
    "urn:assistance:assistance-report:read:many:restricted",
    "urn:assistance:justifications-report:read:many:restricted",
    "urn:assistance:general-assistance-report:read:many:restricted",
    "urn:assistance:schedule:read:self",
    "urn:assistance:schedule:read:many:restricted",
    "urn:assistance:justifications:read:many:restricted",
    "urn:assistance:justification-date:create:many:restricted",
    "urn:assistance:justification-date:delete:many:restricted",
    "urn:assistance:justification-date:read:self"  

    OJO CON EL ORDEN DE ASIGNACION DE PERMISOS PARA UN USUARIO
    '''
    
    ''' Accesos permitidos ''' 
    assert p.chequear_permisos('default', [
                                            "urn:assistance:users:read:many:restricted",
                                            "urn:assistance:users:read:self",
                                            "urn:assistance:places:read:many",
                                            "urn:assistance:assistance-report:read:many:restricted",
                                            "urn:assistance:justifications-report:read:many:restricted",
                                            "urn:assistance:general-assistance-report:read:many:restricted",
                                            "urn:assistance:schedule:read:many:restricted",
                                            "urn:assistance:schedule:read:self",
                                            "urn:assistance:justifications:read:many:restricted",
                                            "urn:assistance:justification-date:create:many:restricted",
                                            "urn:assistance:justification-date:delete:many:restricted",
                                            "urn:assistance:justification-date:read:self"
                                            ], permisos) == (True, {
                                                "urn:assistance:users:read:many:restricted",
                                                "urn:assistance:users:read:self",
                                                "urn:assistance:places:read:many",
                                                "urn:assistance:assistance-report:read:many:restricted",
                                                "urn:assistance:justifications-report:read:many:restricted",
                                                "urn:assistance:general-assistance-report:read:many:restricted",
                                                "urn:assistance:schedule:read:many:restricted",
                                                "urn:assistance:schedule:read:self",
                                                "urn:assistance:justifications:read:many:restricted",
                                                "urn:assistance:justification-date:create:many:restricted",
                                                "urn:assistance:justification-date:delete:many:restricted",
                                                "urn:assistance:justification-date:read:self"
                                                })    
    
    ''' Permisos denegados '''
    #TODO Realziar un for de las combinaciones posibles de permisos que deberian ser falsos
    """
    sistemas = ['assistance']
    recursos = ['users','places','assistance-report','schedule','justifications','justifications-date','devices','logs','*']
    operaciones = ['create','read','update','delete','*']
    alcances = ['any','many', 'sub', 'one', 'self','*']
    modelo = ['restricted']
    """
    #Recursos denegados para el perfil determinado
    recursosDenegados = ['logs','devices','*']
    operacionesDenegadas = ['update','*']
    alcancesDenegados = ['any','one','sub','*']

    for s in sistemas:
        for r in recursosDenegados:
            for o in operacionesDenegadas:
                for a in alcancesDenegados:
                    assert p.chequear_permisos('default', [f"urn:{s}:{r}:{o}:{a}"], permisos) == (False, set())

    #Combinaciones que deberian ser denegadas para el perfil determinado
    denegados = {
        'users': {
            'read': {
                'any' : ['*','restricted',''],
                'many': ['*',''],
                'sub' : ['*','restricted',''],
                'one' : ['*','restricted',''],
                'self': ['*','restricted'],
                '*'   : ['*','restricted','']
            },
            'delete': {
                'any' : ['*','restricted',''],
                'many': ['*','restricted',''],
                'sub' : ['*','restricted',''],
                'one' : ['*','restricted',''],
                'self': ['*','restricted',''],
                '*'   : ['*','restricted','']
            }
        }
    }

def generarPermisosDenegados(usuario):
    """
    Genera un arbol de los permisos denegados para el usuario solicitado
    """
    arbolPermisos = {}
    #Creo arbol de permisos completo
    for p in prefijos:
        arbolPermisos[p] = {}
        for s in sistemas:
            print(p,s)
            arbolPermisos[p][s] = {}
            for r in recursos:
                arbolPermisos[p][s][r] = {}
                for o in operaciones:
                    arbolPermisos[p][s][r][o] = {}
                    for a in alcances:
                        arbolPermisos[p][s][r][o][a] = ['restricted']

    for c in permisos[usuario]:
        parseado = c.split(':')
        urn      = parseado[0] if len(parseado) >= 1 else None
        sistema  = parseado[1] if len(parseado) >= 2 else None
        recurso  = parseado[2] if len(parseado) >= 3 else None
        operacion= parseado[3] if len(parseado) >= 4 else None
        alcance  = parseado[4] if len(parseado) >= 5 else None
        modelo   = parseado[5] if len(parseado) == 6 else None

        print(urn, sistema, recurso, operacion,alcance,modelo)

        if urn in arbolPermisos.keys():    
            if sistema in arbolPermisos[urn].keys():
                if (not recurso or recurso == '*') and (not operacion or operacion == '*') and (not alcance or alcance == '*') and (not modelo):
                    print(f'Eliminando SISTEMA ----> {sistema}')
                    arbolPermisos[urn].pop(sistema)
                elif recurso in arbolPermisos[urn][sistema].keys():
                    if (not operacion or operacion == '*') and (not alcance or alcance == '*') and (not modelo):
                        print(f'Eliminando RECURSO ----> {recurso}')
                        arbolPermisos[urn][sistema].pop(recurso)
                    elif operacion in arbolPermisos[urn][sistema][recurso].keys():
                        if (not alcance or alcance == '*') and (not modelo):
                            print(f'Eliminando OPERACION ----> {operacion}')
                            arbolPermisos[urn][sistema][recurso].pop(operacion)
                        elif alcance in arbolPermisos[urn][sistema][recurso][operacion].keys():
                            if (not modelo):
                                print(f'Eliminando ALCANCE ----> {alcance}')
                                arbolPermisos[urn][sistema][recurso][operacion].pop(alcance)
                            elif modelo in arbolPermisos[urn][sistema][recurso][operacion][alcance]:
                                print(f'Eliminando MODELO ----> {modelo}')
                                arbolPermisos[urn][sistema][recurso][operacion][alcance].remove(modelo)

    print(arbolPermisos)
    return arbolPermisos

if __name__ == "__main__":
    usuario = 'default'
    generarPermisosDenegados(usuario)