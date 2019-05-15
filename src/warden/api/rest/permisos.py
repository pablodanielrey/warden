
class Operacion:
    ''' 
        tabla de jerarquía de alcances 
        el indice es la jerarquía permitida y los valores son las equivalencias alcanzadas por el permiso.
    '''
    equivalencias = {
        'self': ['self'],
        'one': ['one','self'],
        'sub': ['sub','self'],
        'many': ['many','sub','one','self'],
        'any': ['*','any','many', 'sub', 'one', 'self'],
        '*': ['*','any','many', 'sub', 'one', 'self']
    }

    def __init__(self, o, a=None, m=None):
        self.op = o
        self.alcance = a if a else '*'
        self.modelo = m if m else '*'

    ''' chequea si la operación tiene un alcance y modelo permitidos '''
    def _chequear_alcance_modelo(self, arbol_operacion):
        for alcance_permitido in arbol_operacion:
            if self.alcance in self.equivalencias[alcance_permitido]:
                if arbol_operacion[alcance_permitido] == self.modelo:
                    return True
                elif arbol_operacion[alcance_permitido] == '*':
                    return True
        return False

    ''' chequea si la operación esta permitida dentro del recurso '''
    def chequear_operacion(self, arbol_recurso):
        permitido = False
        for operacion in arbol_recurso:
            if self.op == operacion or operacion == '*':
                permitido = permitido or self._chequear_alcance_modelo(arbol_recurso[operacion])
        return True

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
    parsea el string definido del permiso y retora un diccionario que lo define
"""
def _parsear_permiso(perm):
    arr = perm.split(':')
    op = arr[3]
    alcance = arr[4] if len(arr) > 4 else None
    modelo = arr[5] if len(arr) > 5 else None
    ret = {
        'sistema': arr[1],
        'recurso': arr[2],
        'operacion': Operacion(op, alcance, modelo)
    }
    return ret

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
    arbol = {}
    for indice in [uid, 'default']:
        if indice not in permissions:
            continue
        for p in permissions[indice]:
            perm = _parsear_permiso(p)

            s = perm['sistema']
            if s not in arbol:
                arbol[s] = {}

            r = perm['recurso']
            if r not in arbol[s]:
                arbol[s][r] = {}

            o = perm['operacion']
            if o not in arbol[s][r]:
                arbol[s][r][o] = {}

            a = perm['alcance']
            if a not in arbol[s][r][o]:
                arbol[s][r][o][a] = {}
            
            m = perm['modelo']
            arbol[s][r][o][a] = m 
    return arbol

def _chequear_operacion(permiso, arbol_operaciones):
    op = permiso['operacion']
    return op.chequear_operacion(arbol_operaciones)

def _chequear_recurso(permiso, arbol_recursos):
    r = permiso['recurso']
    if r in arbol_recursos:
        arbol_operaciones = arbol_recursos[r]
        return _chequear_operacion(permiso, arbol_operaciones)
    elif '*' in arbol_recursos:
        arbol_operaciones = arbol_recursos['*']
        return _chequear_operacion(permiso, arbol_operaciones)
    return False

def _chequear_sistema(perm, arbol_permisos):
    permiso = _parsear_permiso(perm)
    s = permiso['sistema']
    if s in arbol_permisos:
        arbol_recursos = arbol_permisos[s]
        return _chequear_recurso(permiso, arbol_recursos)
    elif '*' in arbol_permisos:
        arbol_recursos = arbol_permisos['*']
        return _chequear_recurso(permiso, arbol_recursos)
    return False

def chequear_permisos(uid, permisos=[], lista_permisos={}):
    arbol = _obtener_arbol_permisos(uid, lista_permisos)
    permitido = True
    for p in permisos:
        permitido = permitido and _chequear_sistema(p, arbol)
    return permitido

