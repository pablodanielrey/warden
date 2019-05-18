
def test_esquema_recursos():
    """
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
    """

    import warden.api.rest.permisos as perm

    p = {
        '1': {
            'urn:sistema:recurso'
        },
        'default': {
        }
    }

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

    for op in ['create','update','delete','read']:
        for alc in ['sub','one','self','many','any']:
            assert perm.chequear_permisos('1',[f'urn:sistema:recurso:{op}:{alc}'], p) == (True, {f'urn:sistema:recurso:{op}:{alc}'})
