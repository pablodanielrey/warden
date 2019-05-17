
def test_permisos_comodin_1():
    import warden.api.rest.permisos as p
    permisos = {
        'default': [
            'urn:*:*:*'
        ]
    }
    assert p.chequear_permisos('1', ['urn:sistema:recurso:operacion1'], permisos) == (True,['urn:sistema:recurso:operacion1'])
    assert p.chequear_permisos('1', ['urn:sistema:recurso'], permisos) == (False,[])
    assert p.chequear_permisos('1', ['urn:sistema:recurso:*'], permisos) == (True,['urn:sistema:recurso:*'])
    assert p.chequear_permisos('1', ['urn:sistema:recurso:operacion2'], permisos) == (True,['urn:sistema:recurso:operacion2'])
    assert p.chequear_permisos('1', ['urn:sistema2:recurso2:operacion2'], permisos) == (True,['urn:sistema2:recurso2:operacion2'])
    assert p.chequear_permisos('1', ['urn:sistema2:recurso1:operacion2'], permisos) == (True,['urn:sistema2:recurso1:operacion2'])

    assert p.chequear_permisos('1', [
                                        'urn:sistema:recurso:operacion1',
                                        'urn:sistema:recurso:oper',
                                        'urn:sistema:recurso:operacion3:many:algo'
                                    ], permisos) == (True,
                                    [
                                        'urn:sistema:recurso:operacion1',
                                        'urn:sistema:recurso:oper',
                                        'urn:sistema:recurso:operacion3:many:algo'
                                    ])  

def test_permisos_usuario_default_comodin():
    import warden.api.rest.permisos as p
    permisos = {
        '1': [
            'urn:sistema:recurso:operacion',
        ],        
        '2': [
            'urn:sistema:recurso:oper',
            'urn:sistema:recurso:operacion',
        ],        
        'default': [
            'urn:sistema:recurso:operacion1',
            'urn:*:*:*',
            'urn:sistema:recurso:operacion2',
            'urn:sistema:recurso:operacion3:many',
            'urn:sistema:recurso:operacion4:many:restricted'
        ]
    }
    assert p.chequear_permisos('1', [
                                        'urn:sistema:recurso:operacion1',
                                        'urn:sistema:recurso:oper',
                                        'urn:sistema:recurso:operacion3:many:algo'
                                    ], permisos) == (True,
                                    [
                                        'urn:sistema:recurso:operacion1',
                                        'urn:sistema:recurso:oper',
                                        'urn:sistema:recurso:operacion3:many:algo'
                                    ])
    
    assert p.chequear_permisos('1', [
                                        'urn:sistema:recurso:operacion',
                                        'urn:sistema:recurso:operacion3:many:algo'
                                    ], permisos) == (True,
                                    [
                                        'urn:sistema:recurso:operacion',
                                        'urn:sistema:recurso:operacion3:many:algo'
                                    ])  

def test_permisos_especificos_default_falsos():
    import warden.api.rest.permisos as p
    permisos = {
        'default': [
            'urn:sistema:recurso:permiso'
        ]
    }
    assert p.chequear_permisos('1', ['urn:sistema:recurso2:permiso'], permisos) == (False,[])
    assert p.chequear_permisos('1', ['urn:sistema:recurso2:p'], permisos) == (False,[])
    assert p.chequear_permisos('1', ['urn:sistema:recurso2'], permisos) == (False,[])
    assert p.chequear_permisos('1', ['urn:sistema:recurso'], permisos) == (False,[])

def test_permisos_especificos_default_verdaderos():
    import warden.api.rest.permisos as p
    permisos = {
        'default': [
            'urn:sistema:recurso:operacion1',
            'urn:sistema:recurso:operacion2:self',
            'urn:sistema:recurso:operacion2',
            'urn:sistema:recurso:operacion3:many',
            'urn:sistema:recurso:operacion4:many:restricted'
        ]
    }
    assert p.chequear_permisos('1', ['urn:sistema:recurso:operacion1'], permisos) == (True,['urn:sistema:recurso:operacion1'])

    assert p.chequear_permisos('1', ['urn:sistema:recurso:operacion2:self'], permisos) == (True,['urn:sistema:recurso:operacion2:self'])
    assert p.chequear_permisos('1', ['urn:sistema:recurso:operacion2'], permisos) == (True,['urn:sistema:recurso:operacion2'])
    assert p.chequear_permisos('1', ['urn:sistema:recurso:operacion2:many'], permisos) == (True,['urn:sistema:recurso:operacion2:many'])
    assert p.chequear_permisos('1', ['urn:sistema:recurso:operacion2:many:restricted'], permisos) == (True,['urn:sistema:recurso:operacion2:many:restricted'])

    assert p.chequear_permisos('1', ['urn:sistema:recurso:operacion3:many'], permisos) == (True,['urn:sistema:recurso:operacion3:many'])
    assert p.chequear_permisos('1', ['urn:sistema:recurso:operacion3:many:restricted'], permisos) == (True,['urn:sistema:recurso:operacion3:many:restricted'])
    assert p.chequear_permisos('1', ['urn:sistema:recurso:operacion3:many:algo'], permisos) == (True,['urn:sistema:recurso:operacion3:many:algo'])

def test_permisos_default_verdaderos():
    import warden.api.rest.permisos as p
    permisos = {
        'default': [
            'urn:sistema:recurso:operacion1',
            'urn:sistema:recurso:operacion2:self',
            'urn:sistema:recurso:operacion2',
            'urn:sistema:recurso:operacion3:many',
            'urn:sistema:recurso:operacion4:many:restricted'
        ]
    }
    assert p.chequear_permisos('1', 
        [
            'urn:sistema:recurso:operacion1',
            'urn:sistema:recurso:operacion2:self',
            'urn:sistema:recurso:operacion3:many:algo'
        ], permisos) == (True,
        [
            'urn:sistema:recurso:operacion1',
            'urn:sistema:recurso:operacion2:self',
            'urn:sistema:recurso:operacion3:many:algo'
        ])
    

def test_permisos_default_algunos_falsos():
    import warden.api.rest.permisos as p
    permisos = {
        'default': [
            'urn:sistema:recurso:operacion1',
            'urn:sistema:recurso:operacion2:self',
            'urn:sistema:recurso:operacion2',
            'urn:sistema:recurso:operacion3:many',
            'urn:sistema:recurso:operacion4:many:restricted'
        ]
    }
    ''' en este caso la segunda operación debe fallar. '''
    assert p.chequear_permisos('1', [
                                        'urn:sistema:recurso:operacion1',
                                        'urn:sistema:recurso:oper',
                                        'urn:sistema:recurso:operacion3:many:algo'
                                    ], permisos) == (False,
                                    [
                                        'urn:sistema:recurso:operacion1',
                                        'urn:sistema:recurso:operacion3:many:algo'
                                    ])
    
    assert p.chequear_permisos('1', [
                                        'urn:sistema:recurso:operacion',
                                        'urn:sistema:recurso:operacion3:many:algo'
                                    ], permisos) == (False,
                                    [
                                        'urn:sistema:recurso:operacion3:many:algo'
                                    ])

def test_permisos_usuario_verdaderos():
    import warden.api.rest.permisos as p
    permisos = {
        '1': [
            'urn:sistema:recurso:oper',
            'urn:sistema:recurso:operacion',
        ],
        'default': [
            'urn:sistema:recurso:operacion1',
            'urn:sistema:recurso:operacion2:self',
            'urn:sistema:recurso:operacion2',
            'urn:sistema:recurso:operacion3:many',
            'urn:sistema:recurso:operacion4:many:restricted'
        ]
    }
    ''' en este caso la segunda operación debe fallar. '''
    assert p.chequear_permisos('1', [
                                        'urn:sistema:recurso:operacion1',
                                        'urn:sistema:recurso:oper',
                                        'urn:sistema:recurso:operacion3:many:algo'
                                    ], permisos) == (True,
                                    [
                                        'urn:sistema:recurso:operacion1',
                                        'urn:sistema:recurso:oper',
                                        'urn:sistema:recurso:operacion3:many:algo'
                                    ])
    
    assert p.chequear_permisos('1', [
                                        'urn:sistema:recurso:operacion',
                                        'urn:sistema:recurso:operacion3:many:algo'
                                    ], permisos) == (True,
                                    [
                                        'urn:sistema:recurso:operacion',
                                        'urn:sistema:recurso:operacion3:many:algo'
                                    ])                                    


def test_permisos_usuario_incorrecto_algunos_falsos():
    import warden.api.rest.permisos as p
    permisos = {
        '2': [
            'urn:sistema:recurso:oper',
            'urn:sistema:recurso:operacion',
        ],        
        'default': [
            'urn:sistema:recurso:operacion1',
            'urn:sistema:recurso:operacion2:self',
            'urn:sistema:recurso:operacion2',
            'urn:sistema:recurso:operacion3:many',
            'urn:sistema:recurso:operacion4:many:restricted'
        ]
    }
    ''' en este caso la segunda operación debe fallar. '''
    assert p.chequear_permisos('1', [
                                        'urn:sistema:recurso:operacion1',
                                        'urn:sistema:recurso:oper',
                                        'urn:sistema:recurso:operacion3:many:algo'
                                    ], permisos) == (False,
                                    [
                                        'urn:sistema:recurso:operacion1',
                                        'urn:sistema:recurso:operacion3:many:algo'
                                    ])
    
    assert p.chequear_permisos('1', [
                                        'urn:sistema:recurso:operacion',
                                        'urn:sistema:recurso:operacion3:many:algo'
                                    ], permisos) == (False,
                                    [
                                        'urn:sistema:recurso:operacion3:many:algo'
                                    ])                                    


def test_permisos_usuario_correcto_algunos_falsos():
    import warden.api.rest.permisos as p
    permisos = {
        '1': [
            'urn:sistema:recurso:operacion',
        ],        
        '2': [
            'urn:sistema:recurso:oper',
            'urn:sistema:recurso:operacion',
        ],        
        'default': [
            'urn:sistema:recurso:operacion1',
            'urn:sistema:recurso:operacion2:self',
            'urn:sistema:recurso:operacion2',
            'urn:sistema:recurso:operacion3:many',
            'urn:sistema:recurso:operacion4:many:restricted'
        ]
    }
    ''' en este caso la segunda operación debe fallar. '''
    assert p.chequear_permisos('1', [
                                        'urn:sistema:recurso:operacion1',
                                        'urn:sistema:recurso:oper',
                                        'urn:sistema:recurso:operacion3:many:algo'
                                    ], permisos) == (False,
                                    [
                                        'urn:sistema:recurso:operacion1',
                                        'urn:sistema:recurso:operacion3:many:algo'
                                    ])
    
    assert p.chequear_permisos('1', [
                                        'urn:sistema:recurso:operacion',
                                        'urn:sistema:recurso:operacion3:many:algo'
                                    ], permisos) == (True,
                                    [
                                        'urn:sistema:recurso:operacion',
                                        'urn:sistema:recurso:operacion3:many:algo'
                                    ])                                                                        



                                    