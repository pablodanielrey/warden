
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
def _obtener_arbol_permisos(uid, permissions):
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

def _cargar_permisos():
    import json
    with open('permissions.json','r') as f:
        permissions = json.loads(f.read())
        return permissions

def _generar_ejemplo():
    import json
    with open('permissions.json', 'w') as f:
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