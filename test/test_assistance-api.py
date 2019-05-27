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
recursos = ['users','places','assistance-report','schedule','justifications','justification-date','justification-report','general-assistance-report','devices','logs','*']
operaciones = ['create','read','update','delete','*']
alcances = ['any','many', 'sub', 'one', 'self','*']
modelos = ['restricted','']

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
            "urn:assistance:users:read:self",
            "urn:assistance:users:read:many:restricted",
            "urn:assistance:places:read:many",
            #"urn:assistance:places:read:self",
            "urn:assistance:assistance-report:read:many:restricted",
            "urn:assistance:justifications-report:read:many:restricted",
            "urn:assistance:general-assistance-report:read:many:restricted",
            "urn:assistance:schedule:read:self",
            "urn:assistance:schedule:read:many:restricted",
            "urn:assistance:justifications:read:many:restricted",
            "urn:assistance:justification-date:read:self",
            "urn:assistance:justification-date:create:many:restricted",
            "urn:assistance:justification-date:delete:many:restricted",
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
    denegados = generarPermisosDenegados('default')
    for urn in denegados:
        for s in denegados[urn]:
            for r in denegados[urn][s]:
                for o in denegados[urn][s][r]:
                    for a in denegados[urn][s][r][o]:
                        for m in denegados[urn][s][r][o][a]:
                            print(f'{urn}:{s}:{r}:{o}:{a}:{m}')
                            assert p.chequear_permisos('default',[f'{urn}:{s}:{r}:{o}:{a}'], permisos) == (False, set())    

def generarPermisosDenegados(usuario):
    """
    Genera un arbol de los permisos denegados para el usuario solicitado
    """
    contadorTotales = 0
    arbolPermisos = {}
    #Creo arbol de permisos completo
    for p in prefijos:
        arbolPermisos[p] = {}
        for s in sistemas:
            arbolPermisos[p][s] = {}
            for r in recursos:
                arbolPermisos[p][s][r] = {}
                for o in operaciones:
                    arbolPermisos[p][s][r][o] = {}
                    for a in alcances:
                        arbolPermisos[p][s][r][o][a] = []
                        for m in modelos:
                            arbolPermisos[p][s][r][o][a].append(m)
                            contadorTotales += 1
    print(f'Se crearon {contadorTotales} permisos diferentes.')

    #Recorro los permisos que tiene el usuario y voy eliminando los que ya tiene de la lista
    for c in permisos[usuario]:
        parseado = c.split(':')
        urn      = parseado[0] if len(parseado) >= 1 else None
        sistema  = parseado[1] if len(parseado) >= 2 else None
        recurso  = parseado[2] if len(parseado) >= 3 else None
        operacion= parseado[3] if len(parseado) >= 4 else None
        alcance  = parseado[4] if len(parseado) >= 5 else None
        modelo   = parseado[5] if len(parseado) == 6 else None

        #Voy consultando por alcence del permiso, si existe lo elimino de la lista de no permitidos
        if urn in arbolPermisos.keys():    
            if sistema in arbolPermisos[urn].keys():
                if (not recurso or recurso == '*') and (not operacion or operacion == '*') and (not alcance or alcance == '*' or alcance == 'any' ) and (not modelo):
                    print(f'Eliminando SISTEMA ----> {urn}:{sistema}:{recurso}:{operacion}:{alcance}:{modelo}')
                    arbolPermisos[urn].pop(sistema)
                elif recurso in arbolPermisos[urn][sistema].keys():
                    if (not operacion or operacion == '*') and (not alcance or alcance == '*' or alcance == 'any') and (not modelo):
                        print(f'Eliminando RECURSO ----> {urn}:{sistema}:{recurso}:{operacion}:{alcance}:{modelo}')
                        arbolPermisos[urn][sistema].pop(recurso)
                    elif operacion in arbolPermisos[urn][sistema][recurso].keys():
                        if (not alcance or alcance == '*' or alcance == 'any'):
                            if not modelo:
                                print(f'Eliminando OPERACION ----> {urn}:{sistema}:{recurso}:{operacion}:{alcance}:{modelo}')
                                arbolPermisos[urn][sistema][recurso].pop(operacion)
                            #Si es any o * y es restricted entonces elimino los restricted de todos los alcances
                            elif not alcance or alcance == 'any' or alcance == '*':
                                if modelo in arbolPermisos[urn][sistema][recurso][operacion]['many']:
                                    arbolPermisos[urn][sistema][recurso][operacion]['many'].remove(modelo)
                                if modelo in arbolPermisos[urn][sistema][recurso][operacion]['sub']:
                                    arbolPermisos[urn][sistema][recurso][operacion]['sub'].remove(modelo)
                                if modelo in arbolPermisos[urn][sistema][recurso][operacion]['one']:
                                    arbolPermisos[urn][sistema][recurso][operacion]['one'].remove(modelo)
                                if modelo in arbolPermisos[urn][sistema][recurso][operacion]['self']:
                                    arbolPermisos[urn][sistema][recurso][operacion]['self'].remove(modelo)
                                if modelo in arbolPermisos[urn][sistema][recurso][operacion]['self']:
                                    arbolPermisos[urn][sistema][recurso][operacion]['self'].remove(modelo)
                        elif alcance == 'many':
                            if 'sub' in arbolPermisos[urn][sistema][recurso][operacion].keys():
                                #Si el modelo es restricted solamente elimino los restricted hijos de sub, sino elimino el alcance completo
                                if modelo == 'restricted' and modelo in arbolPermisos[urn][sistema][recurso][operacion]['sub']:
                                    print(f'Eliminando SUB -> RESTRICTED POR MANY -> RESTRICTED ----> {urn}:{sistema}:{recurso}:{operacion}:{alcance}:{modelo}')
                                    arbolPermisos[urn][sistema][recurso][operacion]['sub'].remove(modelo)        
                                else:
                                    print(f'Eliminando ALCANCE SUB POR MANY----> {urn}:{sistema}:{recurso}:{operacion}:{alcance}:{modelo}')
                                    arbolPermisos[urn][sistema][recurso][operacion].pop('sub')
                            if 'one' in arbolPermisos[urn][sistema][recurso][operacion].keys():
                                #Si el modelo es restricted solamente elimino los restricted hijos de one, sino elimino el alcance one completo
                                if modelo == 'restricted' and modelo in arbolPermisos[urn][sistema][recurso][operacion]['one']:
                                    print(f'Eliminando ONE -> RESTRICTED POR MANY -> RESTRICTED ----> {urn}:{sistema}:{recurso}:{operacion}:{alcance}:{modelo}')
                                    arbolPermisos[urn][sistema][recurso][operacion]['one'].remove(modelo)
                                else:
                                    print(f'Eliminando ALCANCE ONE POR MANY----> {urn}:{sistema}:{recurso}:{operacion}:{alcance}:{modelo}')
                                    arbolPermisos[urn][sistema][recurso][operacion].pop('one')
                            #Si existe el alcance para la operacion...
                            if alcance in arbolPermisos[urn][sistema][recurso][operacion].keys():
                                #Si no existe el modelo es para TODO entonces elimino el calcance
                                if (not modelo):
                                    print(f'Eliminando ALCANCE ----> {urn}:{sistema}:{recurso}:{operacion}:{alcance}:{modelo}')
                                    arbolPermisos[urn][sistema][recurso][operacion].pop(alcance)
                                #Sino solo elimino el modelo
                                elif modelo in arbolPermisos[urn][sistema][recurso][operacion][alcance]:
                                    print(f'Eliminando MODELO ----> {urn}:{sistema}:{recurso}:{operacion}:{alcance}:{modelo}')
                                    arbolPermisos[urn][sistema][recurso][operacion][alcance].remove(modelo)
                        elif alcance in ['one','sub','self']:
                            #Si existe el alcance para la operacion...
                            if alcance in arbolPermisos[urn][sistema][recurso][operacion].keys():
                                #Si no existe el modelo es para TODO entonces elimino el calcance
                                if (not modelo):
                                    print(f'Eliminando ALCANCE ----> {urn}:{sistema}:{recurso}:{operacion}:{alcance}:{modelo}')
                                    arbolPermisos[urn][sistema][recurso][operacion].pop(alcance)
                                #Sino solo elimino el modelo
                                elif modelo in arbolPermisos[urn][sistema][recurso][operacion][alcance]:
                                    print(f'Eliminando MODELO ----> {urn}:{sistema}:{recurso}:{operacion}:{alcance}:{modelo}')
                                    arbolPermisos[urn][sistema][recurso][operacion][alcance].remove(modelo)

    return arbolPermisos

if __name__ == "__main__":
    usuario = 'default'
    denegados = generarPermisosDenegados(usuario)
    contador = 0
    for urn in denegados:
        for s in denegados[urn]:
            for r in denegados[urn][s]:
                for o in denegados[urn][s][r]:
                    for a in denegados[urn][s][r][o]:
                        for m in denegados[urn][s][r][o][a]:
                            print(f'{urn}:{s}:{r}:{o}:{a}:{m}')
                            contador += 1
    print(f'Permisos totales denegados para el usuario: {contador}')