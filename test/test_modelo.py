import pytest

@pytest.fixture
def permisos_recurso_completo():
    permisos = [
        {
            'default': {
                'urn:sistema:recurso'
            }
        },        
        {
            '1': {
                'urn:sistema:recurso'
            },
            'default': {
            }
        },
        {
            '1': {
            },
            'default': {
                'urn:sistema:recurso'
            }
        },
        {
            '1': {
                'urn:sistema:recurso'
            },
            'default': {
                'urn:sistema:recurso'
            }
        }
    ]
    return permisos

@pytest.fixture
def permisos_recurso_solo_operacion():
    '''
        una operación para el recurso permitida. irrestricta. 
        los indices pares son los permisos en default
    '''
    permisos = []
    for op in ['create','read','update','delete']:
        p = [
            {
                'default': {
                    f'urn:sistema:recurso:{op}'
                }
            },        
            {
                '1': {
                    f'urn:sistema:recurso:{op}'
                },
                'default': {
                }
            },
            {
                '1': {
                },
                'default': {
                    f'urn:sistema:recurso:{op}'
                }
            },
            {
                '1': {
                    f'urn:sistema:recurso:{op}'
                },
                'default': {
                    f'urn:sistema:recurso:{op}'
                }
            }
        ]
        permisos.append({'operacion':op, 'permisos':p})
    return permisos

def test_operaciones_recurso(permisos_recurso_completo):
    '''
        Las operaciones permitidas sobre los recursos son:
        udpate, delete, create, read

        se pueden asignar los permisos por operación individual, o por recurso completo.
        urn:sistema:recurso ---> versión de recurso completo
        urn:sistema:recurso:create --> versión de operación individual

        cada operación tiene un alcance determinado por una estructura tipo arbol de oficinas y cargos.
        los cargos que se toman en cuenta para las operaciones de los recursos dependen de cada sistema.
        los alcances son:
        self ---> recurso propio
        one ----> misma unidad organizativa
        sub ----> unidades organizativas subordinadas. NO incluye one
        many ---> one + sub 
        any ----> es igual que comodín, *, o sea todos, no tiene restricción de alcance

        en los casos que sea requerido se puede asociar modificador de modelo.
        ej:
        urn:sistema:recurso:create:restricted
        urn:sistema:recurso:read:many:restricted

        en esos casos el modificador de modelo sirve para que el sistema pueda identificar restricciones a imponer.
        cualquier modificador de sistema SOBRE ESCRIBE el alcance sin modificador.
        ej:
        urn:sistema:recurso:read:many
        urn:sistema:recurso:read:many:restricted  <--- este sobreescribe el anterior.

        Los permisos se asocian dentro de un grupo, La sobre escritura de los permisos solo funciona dentro del mismo grupo
        Entre distintos grupos de permisos NO se sobreescriben.
        ej:

        '1': {
            'urn:sistema:recurso:read:many'
        },
        'default': {
            'urn:sistema:recurso:read:many:restricted'
        }

        todos los demas que no sean 1 tienen el read:many:restricted, el caso del 1 tiene read:many
    '''

    import warden.api.rest.permisos as perm

    '''
        Se asignan todos los permisos a un recurso en particular.
        Usado de esta forma no se aplican restricciones de modelo al alcance del recurso.
        Las restricciones de modelo solo se aplican explícitamente.
    '''

    for p in permisos_recurso_completo:
        ''' chequeo las operaciones '''
        assert perm.chequear_permisos('1',['urn:sistema:recurso'], p) == (True,{'urn:sistema:recurso'})
        assert perm.chequear_permisos('1',[
                'urn:sistema:recurso',
                'urn:sistema:recurso:create',
                'urn:sistema:recurso:delete',
                'urn:sistema:recurso:update',
                'urn:sistema:recurso:read'
            ], p) == (True,{
                'urn:sistema:recurso',
                'urn:sistema:recurso:create',
                'urn:sistema:recurso:delete',
                'urn:sistema:recurso:update',
                'urn:sistema:recurso:read'
            })

        ''' 
            chequeo el alcance de las operaciones y que no tengan aplicadas restricciones de modelo 
            las chequeo en forma individual y en forma de conjunto
        '''
        permisos_a_chequear = []
        for op in ['create','update','delete','read']:
            for alc in ['sub','one','self','many','any']:
                assert perm.chequear_permisos('1',[f'urn:sistema:recurso:{op}:{alc}'], p) == (True, {f'urn:sistema:recurso:{op}:{alc}'})
                assert perm.chequear_permisos('1',[f'urn:sistema:recurso:{op}:{alc}:restricted'], p) == (False, set())
                permisos_a_chequear.append(f'urn:sistema:recurso:{op}:{alc}')
        assert perm.chequear_permisos('1',permisos_a_chequear, p) == (True, set(permisos_a_chequear))

        ''' 
            operaciones no existentes sobre el recurso 
            chequeo en forma individual y en forma de conjunto
        '''
        permisos_a_chequear = []
        for op in ['op1','op2']:
            assert perm.chequear_permisos('1',[f'urn:sistema:recurso:{op}'], p) == (False, set())
            permisos_a_chequear.append(f'urn:sistema:recurso:{op}')
            for alc in ['sub','one','self','many','any']:
                assert perm.chequear_permisos('1',[f'urn:sistema:recurso:{op}:{alc}'], p) == (False, set())
                permisos_a_chequear.append(f'urn:sistema:recurso:{op}:{alc}')
        assert perm.chequear_permisos('1',permisos_a_chequear,p) == (False, set())

        ''' chequeo recursos inexistentes '''
        permisos_a_chequear = []
        assert perm.chequear_permisos('1',[f'urn:sistema:recurso2'], p) == (False, set())
        for op in ['create','update','delete','read']:
            for alc in ['sub','one','self','many','any']:
                permisos_a_chequear.append(f'urn:sistema:recurso2:{op}:{alc}')
                assert perm.chequear_permisos('1',[f'urn:sistema:recurso2:{op}:{alc}'], p) == (False, set())
                assert perm.chequear_permisos('1',[f'urn:sistema:recurso2:{op}:{alc}:restricted'], p) == (False, set())
        assert perm.chequear_permisos('1', permisos_a_chequear, p) == (False, set())

        assert perm.chequear_permisos('1', ['url:*'], p) == (False, set())
        assert perm.chequear_permisos('1', ['url:*:*'], p) == (False, set())
        assert perm.chequear_permisos('1', ['url:*:*:*'], p) == (False, set())
        assert perm.chequear_permisos('1', ['url:*:*:*:*'], p) == (False, set())
        assert perm.chequear_permisos('1', ['url:*:*:*:*:*'], p) == (False, set())
        assert perm.chequear_permisos('1', ['urn:sistema'], p) == (False, set())
        assert perm.chequear_permisos('1', ['urn'], p) == (False, set())
        
def test_operacion_recurso(permisos_recurso_solo_operacion):
    """
        testea que solo esté permitido una operación en el recurso, teneindo en cuenta distintos casos de usuarios y los scopes de tales operaciones.
    """
    import warden.api.rest.permisos as perm

    equivalencias_operaciones = {
        'delete': ['delete'],
        'update': ['update'],
        'read': ['read'],
        'create': ['create','read','update'],
        '*': ['create','read','update','delete']
    }

    for a, permisos in enumerate(permisos_recurso_solo_operacion):
        op = permisos['operacion']
        permisos_posibles = permisos['permisos']

        for i, p in enumerate(permisos_posibles):
            es_default = i % 2 == 0

            ''' acceso a todo el recurso esta denegado '''
            assert perm.chequear_permisos('1',[f'urn:sistema:recurso'], p) == (False, set())

            for _op in ['create','update','delete','read']:

                ''' la operación permitida por los permisos es cuando op == _op '''
                if _op in equivalencias_operaciones[op]:
                    assert perm.chequear_permisos('1',[f'urn:sistema:recurso:{_op}'], p) == (True, {f'urn:sistema:recurso:{_op}'})
                    for alc in ['sub','one','self','many','any']:
                        assert perm.chequear_permisos('1',[f'urn:sistema:recurso:{_op}:{alc}'], p) == (True, {f'urn:sistema:recurso:{_op}:{alc}'})
                        assert perm.chequear_permisos('1',[f'urn:sistema:recurso:{_op}:{alc}:restricted'], p) == (False, set())
                else:
                    assert perm.chequear_permisos('1',[f'urn:sistema:recurso:{_op}'], p) == (False,set())
                    for alc in ['sub','one','self','many','any']:
                        assert perm.chequear_permisos('1',[f'urn:sistema:recurso:_{op}:{alc}'], p) == (False, set())
                        assert perm.chequear_permisos('1',[f'urn:sistema:recurso:{_op}:{alc}:restricted'], p) == (False, set())

