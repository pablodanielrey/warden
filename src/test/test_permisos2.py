 """
        comodines:
            * = cualquiera
        permisos disponibles:
            delete (eliminar)
            read (lectura) 
            update (actualización) 
            create (creación)
        scopes:
            any (es el por defecto) = *
            self (recurso propio)
            one (dentro de la misma unidad organizativa)
            sub (sub unidades organizatibas)
            many (sub + one)
            
        restriciones:        
            restricted (restringido por el modelo del sistema)
    """

def comodines():
    """
    #TODO Test comodines
    """
    import warden.api.rest.permisos as p
    permisos = {
        '1': [
            'urn:sistema:recurso:update',
            'urn:sistema:*:update',
            'urn:sistema:recurso:*',
            'urn:sistema2:recurso:*',
            'urn:sistema2:*:update',
            'urn:sistema2:recurso2:update:many',
            'urn:sistema2:recurso2:self'
        ],        
        '2': [
            'urn:sistema:recurso:delete',
            'urn:sistema:recurso2:update',
            'urn:sistema2:*:*',
        ],        
        'default': [
            'urn:sistema:recurso:create',
            'urn:sistema:recurso:delete:self',
            'urn:sistema:recurso:read:*',
            'urn:sistema:recurso:update:many:restricted'
        ]
    }
    assert p.chequear_permisos('1', ['urn:sistema:recurso:*'], permisos) == (True,set(['urn:sistema:recurso:*']))
    assert p.chequear_permisos('1', ['urn:sistema:recurso:create'], permisos) == (True,set(['urn:sistema:recurso:create']))
    assert p.chequear_permisos('1', ['urn:sistema:recurso'], permisos) == (True,set(['urn:sistema:recurso']))
    assert p.chequear_permisos('1', ['urn:sistema:recurso:update'], permisos) == (True,set(['urn:sistema:recurso:update']))

    assert p.chequear_permisos('1', ['urn:sistema2:recurso2:update'], permisos) == (False,set())
    assert p.chequear_permisos('1', ['urn:sistema2:recurso1:update'], permisos) == (False,set())

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
                                        'urn:sistema:recurso:delete:many:restricted:asd'
                                    ]))                                       

def sistemas():
    """
    #TODO Tests Sistemas
    """
    import warden.api.rest.permisos as p
    permisos = {
        '1': [
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
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

def recursos():
    """
    #TODO 
    # """
    import warden.api.rest.permisos as p
    permisos = {
        '1': [
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
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

    assert p.chequear_permisos('1', ['urn:sistema:recurso2:delete'], permisos) == (False,set())
    assert p.chequear_permisos('1', ['urn:sistema:recurso2:create'], permisos) == (False,set())
    assert p.chequear_permisos('1', ['urn:sistema:recurso2'], permisos) == (False,set())
    assert p.chequear_permisos('1', ['urn:sistema:recurso'], permisos) == (False,set())

def permisos():
    """
    #TODO Test permisos
    """
    import warden.api.rest.permisos as p
    permisos = {
        '1': [
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
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

    assert p.chequear_permisos('1', ['urn:sistema:recurso:create'], permisos) == (True,{'urn:sistema:recurso:create'})

    assert p.chequear_permisos('1', ['urn:sistema:recurso:update:self'], permisos) == (True,{'urn:sistema:recurso:update:self'})
    assert p.chequear_permisos('1', ['urn:sistema:recurso:update'], permisos) == (True,{'urn:sistema:recurso:update'})
    assert p.chequear_permisos('1', ['urn:sistema:recurso:update:many'], permisos) == (True,{'urn:sistema:recurso:update:many'})
    assert p.chequear_permisos('2', ['urn:sistema:recurso:update'], permisos) == (False,set())
    assert p.chequear_permisos('1', ['urn:sistema:recurso:update:many:restricted'], permisos) == (True,{'urn:sistema:recurso:update:many:restricted'})

    assert p.chequear_permisos('1', ['urn:sistema:recurso:delete:many'], permisos) == (True,{'urn:sistema:recurso:delete:many'})
    assert p.chequear_permisos('1', ['urn:sistema:recurso:delete:many:restricted'], permisos) == (False,set())
    assert p.chequear_permisos('1', ['urn:sistema:recurso:delete:many:algo'], permisos) == (False,set())

def scopes():
     """
    #TODO 
    # """
    import warden.api.rest.permisos as p
    permisos = {
        '1': [
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
            'urn:sistema:recurso:update',
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
