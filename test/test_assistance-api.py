import pytest

"""
TEST ---> Se van a chequear permisos obtenidos al consultar UIDS ficticias:
        Equivalencias:
        1 == AssistanceSuperAdmin
        2 == AssistanceAdmin
        3 == AssistanceOperator
        4 == AssistanceUser
        5 == Default

Para ello se establecen "permisos" que los usuarios tienen

"""
#Permisos existentes utilizados para crear casos de prueba
prefijos = ['urn']
sistemas = ['assistance']
recursos = ['users','places','schedule','justifications','justification-date','assistance-report','justification-report','general-assistance-report','devices','logs']
operaciones = ['create','read','update','delete']
alcances = ['any','many', 'sub', 'one', 'self']
modelos = ['restricted','']

#Permisos efectivos de cada usuario
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
            "urn:assistance:assistance-report:read:many:restricted",
            "urn:assistance:justification-report:read:many:restricted",
            "urn:assistance:general-assistance-report:read:many:restricted",
            "urn:assistance:schedule:read:self",
            "urn:assistance:schedule:read:many:restricted",
            "urn:assistance:justifications:read:many:restricted",
            "urn:assistance:justification-date:read:self",
            "urn:assistance:justification-date:create:many:restricted",
            "urn:assistance:justification-date:delete:many:restricted"           
        ]
    }


def test_default():
    ''' Comprobacion permisos de usuario default
    Se crean 3 tests diferentes para usuario default.
    1 --> Permisos que tiene y que deben retornar --> VERDADERO
    2 --> Permisos sobre recursos que NO tiene debe retornar --> FALSO
    3 --> Permisos DENEGADOS generados automaticamente en base al permiso de la persona que deben retornar --> FALSO

    Permisos de un usuario default:
    "urn:assistance:users:read:self",
    "urn:assistance:users:read:many:restricted",
    "urn:assistance:places:read:many",
    "urn:assistance:assistance-report:read:many:restricted",
    "urn:assistance:justification-report:read:many:restricted",
    "urn:assistance:general-assistance-report:read:many:restricted",
    "urn:assistance:schedule:read:self",
    "urn:assistance:schedule:read:many:restricted",
    "urn:assistance:justifications:read:many:restricted",
    "urn:assistance:justification-date:create:many:restricted",
    "urn:assistance:justification-date:delete:many:restricted",
    "urn:assistance:justification-date:read:self"  
    '''
    import warden.api.rest.permisos as p
    
    ''' Accesos permitidos ''' 
    assert p.chequear_permisos('default', [
                                            "urn:assistance:users:read:many:restricted",
                                            "urn:assistance:users:read:self",
                                            "urn:assistance:places:read:many",
                                            "urn:assistance:assistance-report:read:many:restricted",
                                            "urn:assistance:justification-report:read:many:restricted",
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
                                                "urn:assistance:justification-report:read:many:restricted",
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

    ''' Permisos denegados generados automaticamente en base al perfil enviado '''
    #Combinaciones que deberian ser denegadas para el perfil determinado
    denegados = generarPermisosDenegados('default')
    for urn in denegados:
        for s in denegados[urn]:
            for r in denegados[urn][s]:
                for o in denegados[urn][s][r]:
                    for a in denegados[urn][s][r][o]:
                        for m in denegados[urn][s][r][o][a]:
                            if m == 'restricted':
                                print(f'Probando permiso --> {urn}:{s}:{r}:{o}:{a}:{m}')
                                assert p.chequear_permisos('default',[f'{urn}:{s}:{r}:{o}:{a}:{m}'], permisos) == (False, set())
                            else:
                                print(f'Probando permiso --> {urn}:{s}:{r}:{o}:{a}')
                                assert p.chequear_permisos('default',[f'{urn}:{s}:{r}:{o}:{a}'], permisos) == (False, set())

def generarPermisosDenegados(usuario):
    """
    Genera un arbol de los permisos denegados para el usuario solicitado
    """
    
    equivalencias_alcance = {
        'self': ['self'],
        'one': ['one','self'],
        'sub': ['sub','self'],
        'many': ['many','sub','one','self'],
        'any': ['any','many', 'sub', 'one', 'self'],
        '*': ['any','many', 'sub', 'one', 'self']
    }

    equivalencias_operaciones = {
        'delete': ['delete'],
        'update': ['update'],
        'read': ['read'],
        'create': ['create','read','update'],
        '*': ['create','read','update','delete']
    }

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
        alcance  = parseado[4] if len(parseado) >= 5 else '*'
        modelo   = parseado[5] if len(parseado) == 6 else None
        
        print(f'Permiso del usuario ----->{urn}:{sistema}:{recurso}:{operacion}:{alcance}:{modelo}')

        #Voy consultando por alcence del permiso, si existe lo elimino de la lista de no permitidos
        if urn in arbolPermisos.keys():
            #Si es * son todos los sistemas entonces creo un arreglo de los sistemas existentes para recorrerlo 
            if sistema == '*':
                sistemasTmp = arbolPermisos[urn].keys()
            #Sino creo un arreglo del sistema actual
            else:
                sistemasTmp = [sistema]
            #Recorro el o los sistemas dependiendo el caso
            for si in sistemasTmp:
                #Si existe en el arbol de permisos entro
                if si in arbolPermisos[urn].keys():
                    #Si es * son todos los recursos entonces creo un arreglo de los recursos existentes para recorrerlo
                    if recurso == '*':
                        recursosTmp = arbolPermisos[urn][si].keys()
                    #Sino creo un arreglo del recurso actual
                    else:
                        recursosTmp = [recurso]
                    #Recorro todos los recursos dependiendo el caso
                    for re in recursosTmp:
                        #Si existe en el arbol entro
                        if re in arbolPermisos[urn][si].keys():
                            #Por cada equivalencia de operacion entro
                            for op in equivalencias_operaciones[operacion]:
                                #Si existe la operacion para el recurso entro
                                if op in arbolPermisos[urn][si][re].keys():
                                    #Por cada equivalencia de alcance entro
                                    for al in equivalencias_alcance[alcance]:
                                        #Si existe el alcance para para la operacion
                                        if al in arbolPermisos[urn][si][re][op].keys():    
                                            #Si no esta definido el modelo entonces son todos los alcances elimino todo si existe
                                            if not modelo:
                                                print(f'Eliminando ALCANCE ----> {urn}:{si}:{re}:{op}:{al}:{modelo}')
                                                arbolPermisos[urn][si][re][op].pop(al)
                                            #Si es any o * y es restricted entonces elimino los restricted de todos los alcances
                                            else:
                                                if modelo in arbolPermisos[urn][si][re][op][al]:
                                                    print(f'Eliminando MODELO ----> {urn}:{si}:{re}:{op}:{al}:{modelo}')
                                                    arbolPermisos[urn][si][re][op][al].remove(modelo)
    return arbolPermisos

#if __name__ == "__main__":
#    usuario = 'default'
#    denegados = generarPermisosDenegados(usuario)
#    contador = 0
#    for urn in denegados:
#        for s in denegados[urn]:
#            for r in denegados[urn][s]:
#                for o in denegados[urn][s][r]:
#                    for a in denegados[urn][s][r][o]:
#                        for m in denegados[urn][s][r][o][a]:
#                            #print(f'{urn}:{s}:{r}:{o}:{a}:{m}')
#                            contador += 1
#    print(f'Permisos totales denegados para el usuario: {contador}')        