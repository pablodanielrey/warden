
def test_permisos_comodin_1():
    import warden.api.rest.permisos as p
    permisos = {
        'default': [
            'urn:*:*:*'
        ]
    }
    assert p.chequear_permisos('1', ['urn:sistema:recurso:*'], permisos) == (True,set(['urn:sistema:recurso:*']))
    assert p.chequear_permisos('1', ['urn:sistema:recurso:create'], permisos) == (True,set(['urn:sistema:recurso:create']))
    assert p.chequear_permisos('1', ['urn:sistema:recurso'], permisos) == (True,set(['urn:sistema:recurso']))
    assert p.chequear_permisos('1', ['urn:sistema:recurso:update'], permisos) == (True,set(['urn:sistema:recurso:update']))
    assert p.chequear_permisos('1', ['urn:sistema2:recurso2:update'], permisos) == (True,set(['urn:sistema2:recurso2:update']))
    assert p.chequear_permisos('1', ['urn:sistema2:recurso1:update'], permisos) == (True,set(['urn:sistema2:recurso1:update']))

    assert p.chequear_permisos('1', [
                                        'urn:sistema:recurso:create',
                                        'urn:sistema:recurso:delete',
                                        'urn:sistema:recurso:delete:many',
                                        'urn:sistema:recurso:delete:many:algo'
                                    ], permisos) == (False,
                                    {
                                        'urn:sistema:recurso:create',
                                        'urn:sistema:recurso:delete',
                                        'urn:sistema:recurso:delete:many'
                                    })

    assert p.chequear_permisos('1', [
                                        'urn:sistema:recurso:create',
                                        'urn:sistema:recurso:delete',
                                        'urn:sistema:recurso:delete:many'
                                    ], permisos) == (True,
                                    set([
                                        'urn:sistema:recurso:create',
                                        'urn:sistema:recurso:delete',
                                        'urn:sistema:recurso:delete:many'
                                    ]))                                       

def _test_permisos_usuario_default_comodin():
    import warden.api.rest.permisos as p
    permisos = {
        '1': [
            'urn:sistema:recurso:update',
        ],        
        '2': [
            'urn:sistema:recurso:delete',
            'urn:sistema:recurso:update',
        ],        
        'default': [
            'urn:sistema:recurso:create',
            'urn:*:*:*',
            'urn:sistema:recurso:delete:many',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update:many:restricted'
        ]
    }
    assert p.chequear_permisos('1', [
                                        'urn:sistema:recurso:create',
                                        'urn:sistema:recurso:delete',
                                        'urn:sistema:recurso:delete:many',
                                        'urn:sistema:recurso:update:many:restricted'
                                    ], permisos) == (True,
                                    set([
                                        'urn:sistema:recurso:create',
                                        'urn:sistema:recurso:delete',
                                        'urn:sistema:recurso:delete:many',
                                        'urn:sistema:recurso:update:many:restricted'
                                    ]))

    assert p.chequear_permisos('1', [
                                        'urn:sistema:recurso:create',
                                        'urn:sistema:recurso:delete',
                                        'urn:sistema:recurso:delete:many',
                                        'urn:sistema:recurso:update:many'
                                    ], permisos) == (True,
                                    set([
                                        'urn:sistema:recurso:create',
                                        'urn:sistema:recurso:delete',
                                        'urn:sistema:recurso:delete:many',
                                        'urn:sistema:recurso:update:many'
                                    ]))                                    
    
    assert p.chequear_permisos('1', [
                                        'urn:sistema:recurso:update',
                                        'urn:sistema:recurso:delete:many:algo'
                                    ], permisos) == (False,
                                    set([
                                        'urn:sistema:recurso:update'
                                    ]))  

def test_permisos_especificos_default_falsos():
    import warden.api.rest.permisos as p
    permisos = {
        'default': [
            'urn:sistema:recurso:update'
        ]
    }
    assert p.chequear_permisos('1', ['urn:sistema:recurso2:delete'], permisos) == (False,set())
    assert p.chequear_permisos('1', ['urn:sistema:recurso2:create'], permisos) == (False,set())
    assert p.chequear_permisos('1', ['urn:sistema:recurso2'], permisos) == (False,set())
    assert p.chequear_permisos('1', ['urn:sistema:recurso'], permisos) == (False,set())

def _test_permisos_especificos_default_verdaderos():
    import warden.api.rest.permisos as p
    permisos = {
        '1': [
            'urn:sistema:recurso:update'
        ],
        'default': [
            'urn:sistema:recurso:create',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update:self',
            'urn:sistema:recurso:update:many:restricted',
            'urn:sistema:recurso:delete:many'
        ]
    }
    assert p.chequear_permisos('1', ['urn:sistema:recurso:create'], permisos) == (True,{'urn:sistema:recurso:create'})

    assert p.chequear_permisos('1', ['urn:sistema:recurso:update:self'], permisos) == (True,{'urn:sistema:recurso:update:self'})
    assert p.chequear_permisos('1', ['urn:sistema:recurso:update'], permisos) == (True,{'urn:sistema:recurso:update'})
    assert p.chequear_permisos('1', ['urn:sistema:recurso:update:many'], permisos) == (True,{'urn:sistema:recurso:update:many'})
    assert p.chequear_permisos('2', ['urn:sistema:recurso:update'], permisos) == (False,set())
    assert p.chequear_permisos('1', ['urn:sistema:recurso:update:many:restricted'], permisos) == (True,{'urn:sistema:recurso:update:many:restricted'})

    assert p.chequear_permisos('1', ['urn:sistema:recurso:delete:many'], permisos) == (True,{'urn:sistema:recurso:delete:many'})
    assert p.chequear_permisos('1', ['urn:sistema:recurso:delete:many:restricted'], permisos) == (False,set())
    assert p.chequear_permisos('1', ['urn:sistema:recurso:delete:many:algo'], permisos) == (False,set())

def test_permisos_default_verdaderos():
    import warden.api.rest.permisos as p
    permisos = {
        'default': [
            'urn:sistema:recurso:create',
            'urn:sistema:recurso:update:self',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:delete:many',
            'urn:sistema:recurso:update:many:restricted'
        ]
    }
    assert p.chequear_permisos('1', 
        [
            'urn:sistema:recurso:create',
            'urn:sistema:recurso:update:self',
            'urn:sistema:recurso:delete:many'
        ], permisos) == (True,
        {
            'urn:sistema:recurso:create',
            'urn:sistema:recurso:update:self',
            'urn:sistema:recurso:delete:many'
        })
    

def _test_permisos_default_algunos_falsos():
    import warden.api.rest.permisos as p
    permisos = {
        'default': [
            'urn:sistema:recurso:create',
            'urn:sistema:recurso:update:self',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:delete:many',
            'urn:sistema:recurso:update:many:restricted'
        ]
    }

    assert p.chequear_permisos('1', [
                                        'urn:sistema:recurso:create',
                                        'urn:sistema:recurso:delete',
                                        'urn:sistema:recurso:delete:many:algo'
                                    ], permisos) == (False,
                                    {
                                        'urn:sistema:recurso:create'
                                    })
    
    assert p.chequear_permisos('1', [
                                        'urn:sistema:recurso:update',
                                        'urn:sistema:recurso:delete:many:algo'
                                    ], permisos) == (False,set())

def test_permisos_usuario_verdaderos():
    import warden.api.rest.permisos as p
    permisos = {
        '1': [
            'urn:sistema:recurso:delete',
            'urn:sistema:recurso:update',
        ],
        'default': [
            'urn:sistema:recurso:create',
            'urn:sistema:recurso:update:self',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:delete:many',
            'urn:sistema:recurso:update:many:restricted'
        ]
    }
    assert p.chequear_permisos('1', [
                                        'urn:sistema:recurso:create',
                                        'urn:sistema:recurso:delete',
                                        'urn:sistema:recurso:delete:many:algo'
                                    ], permisos) == (False,
                                    {
                                        'urn:sistema:recurso:create',
                                        'urn:sistema:recurso:delete'
                                    })
    
    assert p.chequear_permisos('1', [
                                        'urn:sistema:recurso:update',
                                        'urn:sistema:recurso:delete:many:algo'
                                    ], permisos) == (False,{'urn:sistema:recurso:update'})


def _test_permisos_usuario_incorrecto_algunos_falsos():
    import warden.api.rest.permisos as p
    permisos = {
        '2': [
            'urn:sistema:recurso:delete',
            'urn:sistema:recurso:update',
        ],        
        'default': [
            'urn:sistema:recurso:create',
            'urn:sistema:recurso:update:self',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:delete:many',
            'urn:sistema:recurso:update:many:restricted'
        ]
    }
    assert p.chequear_permisos('1', [
                                        'urn:sistema:recurso:create',
                                        'urn:sistema:recurso:delete',
                                        'urn:sistema:recurso:delete:many:algo'
                                    ], permisos) == (False,
                                    {
                                        'urn:sistema:recurso:create'
                                    })
    
    assert p.chequear_permisos('1', [
                                        'urn:sistema:recurso:update',
                                        'urn:sistema:recurso:delete:many'
                                    ], permisos) == (False,{'urn:sistema:recurso:delete:many'})


def test_permisos_usuario_correcto_algunos_falsos():
    import warden.api.rest.permisos as p
    permisos = {
        '1': [
            'urn:sistema:recurso:update',
        ],        
        '2': [
            'urn:sistema:recurso:delete',
            'urn:sistema:recurso:update',
        ],        
        'default': [
            'urn:sistema:recurso:create',
            'urn:sistema:recurso:update:self',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:delete:many',
            'urn:sistema:recurso:update:many:restricted'
        ]
    }
    ''' en este caso la segunda deleteación debe fallar. '''
    assert p.chequear_permisos('1', [
                                        'urn:sistema:recurso:create',
                                        'urn:sistema:recurso:delete',
                                        'urn:sistema:recurso:delete:many'
                                    ], permisos) == (False,
                                    {
                                        'urn:sistema:recurso:create',
                                        'urn:sistema:recurso:delete:many'
                                    })
    
    assert p.chequear_permisos('2', [
                                        'urn:sistema:recurso:update',
                                        'urn:sistema:recurso:delete'
                                    ], permisos) == (True,
                                    {
                                        'urn:sistema:recurso:update',
                                        'urn:sistema:recurso:delete'
                                    })                                                                        



                                    