
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


class OperacionCliente:
    
    def __init__(self, o=None, a=None, m=None):
        self.op = [o] if o and o != '*' else equivalencias_operaciones['*']
        self.alcance = [a] if a and a != '*' else equivalencias_alcance['*']
        self.modelo = m if m else ''

    ''' chequea si la operación esta permitida dentro del recurso '''
    def chequear_operacion(self, arbol_recurso):
        permitido = True
        for _op in self.op:
            if _op not in arbol_recurso:
                permitido = False
                break
            arbol_alcances = arbol_recurso[_op]
            for _al in self.alcance:
                if _al not in arbol_alcances:
                    permitido = False
                    break
                if arbol_alcances[_al] != self.modelo:
                    permitido = False
                    break
        return permitido
                

def cargar_permisos(fp):
    import json
    with open(fp,'r') as f:
        permissions = json.loads(f.read())
        return permissions

def _generar_ejemplo(fp):
    import json
    with open(fp, 'w') as f:
        permissions = {
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


"""
    retorna una lista de dict que definen los permisos para configurar dentro del arbol, dado un permiso en string.
"""
def _parsear_permiso_arbol(perm):
    arr = perm.split(':')

    sistema = arr[1]
    recurso = arr[2]
    operacion = arr[3] if len(arr) > 3 else '*'
    alcance = arr[4] if len(arr) > 4 else '*'
    modelo = arr[5] if len(arr) > 5 else ''
    
    if alcance not in equivalencias_alcance:
        raise Exception(f'formato de permiso {perm} incorrecto')

    permisos = []
    for _op in equivalencias_operaciones[operacion]:
        for _al in equivalencias_alcance[alcance]:
            op = {
                'sistema': sistema,
                'recurso': recurso,
                'operacion': _op,
                'alcance': _al,
                'modelo': ''
            }
            """
                la restricción del modelo solo se aplica al alcance específico asociado al permiso indicado del cliente 
                no se replica a todos los alcances equivalentes
            """
            if _al == alcance:
                op['modelo'] = modelo
            permisos.append(op)
    return permisos

def _obtener_arbol_permisos(uid, permissions):
    """
        Genera el arbol de permisos para el uid.
        El arbol tiene el siguiente formato:
        arbol = {
            'sistema':{
                'recurso':{
                    'operacion':{
                        'alcance': 'modelo'
                    }
                }
            }
        }

    """    
    if uid not in permissions:
        return None
    arbol = {}
    for p in permissions[uid]:
        for perm in _parsear_permiso_arbol(p):
            m = perm['modelo']

            s = perm['sistema']
            if s not in arbol:
                arbol[s] = {}

            r = perm['recurso']
            if r not in arbol[s]:
                arbol[s][r] = {}

            o = perm['operacion']
            if o not in equivalencias_operaciones:
                raise Exception(f'formato incorrecto de {p}')
            
            for op in equivalencias_operaciones[o]:
                if op not in arbol[s][r]:
                    arbol[s][r][op] = {}

            a = perm['alcance']
            if a not in equivalencias_alcance:
                raise Exception(f'formato incorrecto de {p}')
            
            for al in equivalencias_alcance[a]:
                if al not in arbol[s][r][o]:
                    arbol[s][r][o][al] = m
            
    return arbol


"""
    parsea el string definido del permiso y retora un diccionario que lo define
    el permiso consultado por el cliente tiene que ser específico y no puede tener *
    los * se generan solo para alcance y modelo en el caso de que no sean especificados (esos modificadores si son opcionales)
"""
def _parsear_permiso_cliente(perm):
    arr = perm.split(':')
    sistema = arr[1] if len(arr) > 1 else '*'
    recurso = arr[2] if len(arr) > 2 else '*'

    operacion = arr[3] if len(arr) > 3 else None
    alcance = arr[4] if len(arr) > 4 else None
    modelo = arr[5] if len(arr) > 5 else None
    op = OperacionCliente(operacion, alcance, modelo)

    ret = {
        'sistema': sistema,
        'recurso': recurso,
        'operacion': op
    }
    return ret



def _chequear_operacion(permiso, arbol_operaciones):
    op = permiso['operacion']
    return op.chequear_operacion(arbol_operaciones)

def _chequear_recurso(permiso, arbol_recursos):
    retorno = False
    r = permiso['recurso']
    if r in arbol_recursos:
        arbol_operaciones = arbol_recursos[r]
        retorno = _chequear_operacion(permiso, arbol_operaciones)
    if not retorno and '*' in arbol_recursos:
        arbol_operaciones = arbol_recursos['*']
        retorno = _chequear_operacion(permiso, arbol_operaciones)
    return retorno

def _chequear_sistema(perm, arbol_permisos):
    try:
        retorno = False
        permiso = _parsear_permiso_cliente(perm)
        s = permiso['sistema']
        if s in arbol_permisos:
            arbol_recursos = arbol_permisos[s]
            retorno = _chequear_recurso(permiso, arbol_recursos)
        if not retorno and '*' in arbol_permisos:
            arbol_recursos = arbol_permisos['*']
            retorno = _chequear_recurso(permiso, arbol_recursos)
        return retorno
    except AssertionError:
        return False

def chequear_permisos(uid, permisos_a_chequear=[], lista_permisos={}):
    """
        chequea que todos los permisos requeridos estén permitidos para el usuario uid.
    """
    if len(permisos_a_chequear) <= 0:
        return True, set()

    resultado = set()
    permitido_usuario = False

    arbol = _obtener_arbol_permisos(uid, lista_permisos)
    if arbol:
        permitido_usuario = True
        for p in permisos_a_chequear:
            ok = _chequear_sistema(p, arbol)
            if ok:
                resultado.add(p)
            permitido_usuario = permitido_usuario and ok

    permitido_default = False
    permisos_faltantes = set(permisos_a_chequear) - resultado
    arbol = _obtener_arbol_permisos('default', lista_permisos)
    if arbol:
        permitido_default = True
        for p in permisos_faltantes:
            ok = _chequear_sistema(p, arbol)
            if ok:
                resultado.add(p)
            permitido_default = permitido_default and ok

    permitido = permitido_usuario or permitido_default
    return permitido, resultado

