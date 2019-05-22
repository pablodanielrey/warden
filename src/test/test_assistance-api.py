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

permisos = {
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
        "5": [
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
        ]
    }


def test_usuarios_search():
    import warden.api.rest.permisos as p

    ''' Comprobacion de permisos de la api usuarios_search
    Permisos a chequear en el metodo:
    'urn:assistance:users:read'
    'urn:assistance:users:read:many:restricted'
    '''
    
    ''' AssistanceSuperAdmin ''' 
    assert p.chequear_permisos('1', [
            "urn:assistance:users:read",
        ], permisos) == (True, {
            "urn:assistance:users:read"
        })

    assert p.chequear_permisos('1', [
            "urn:assistance:users:read:many:restricted",
        ], permisos) == (False, {
            "urn:assistance:users:read"
        })        

    ''' AssistanceAdmin ''' 
    assert p.chequear_permisos('2', [
            "urn:assistance:users:read",
        ], permisos) == (True, {
            "urn:assistance:users:read",
        })
    assert p.chequear_permisos('2', [
            "urn:assistance:users:read:many:restricted",
        ], permisos) == (False, {
            "urn:assistance:users:read",
        })

    ''' AssistanceOperator ''' 
    assert p.chequear_permisos('3', [
            "urn:assistance:users:read",
        ], permisos) == (True, {
            "urn:assistance:users:read",
        })
    assert p.chequear_permisos('3', [
            "urn:assistance:users:read:many:restricted",
        ], permisos) == (False, {
            "urn:assistance:users:read",
        })
    ''' AssistanceUser '''
    assert p.chequear_permisos('4', [
            "urn:assistance:users:read",
        ], permisos) == (True, {
            "urn:assistance:users:read",
        })
    assert p.chequear_permisos('4', [
            "urn:assistance:users:read:many:restricted",
        ], permisos) == (False, {
            "urn:assistance:users:read",
        })
    ''' Default '''
    assert p.chequear_permisos('5', [
            "urn:assistance:users:read",
        ], permisos) == (False, {
            "urn:assistance:users:read:many:restricted",
        })
    assert p.chequear_permisos('5', [
            "urn:assistance:users:read:many:restricted",
        ], permisos) == (True, {
            "urn:assistance:users:read:many:restricted",
        })

def test_usuarios():
    import warden.api.rest.permisos as p

    ''' Comprobacion de permisos de la api usuarios 
    Permisos a chequear en el metodo:
    'urn:assistance:users:read'
    'urn:assistance:users:read:many:restricted'
    'urn:assistance:users:read:self'
    '''
    
    ''' AssistanceSuperAdmin ''' 
    assert p.chequear_permisos('1', [
            "urn:assistance:users:read",
        ], permisos) == (True, {
            "urn:assistance:users:read"
        })

    assert p.chequear_permisos('1', [
            "urn:assistance:users:read:many:restricted",
        ], permisos) == (False, {
            "urn:assistance:users:read"
        })

    assert p.chequear_permisos('1', [
            "urn:assistance:users:read:self",
        ], permisos) == (True, {
            "urn:assistance:users:read"
        })        

    ''' AssistanceAdmin ''' 
    assert p.chequear_permisos('2', [
            "urn:assistance:users:read",
        ], permisos) == (True, {
            "urn:assistance:users:read",
        })
    assert p.chequear_permisos('2', [
            "urn:assistance:users:read:many:restricted",
        ], permisos) == (False, {
            "urn:assistance:users:read",
        })

    assert p.chequear_permisos('2', [
            "urn:assistance:users:read:self",
        ], permisos) == (True, {
            "urn:assistance:users:read"
        })

    ''' AssistanceOperator ''' 
    assert p.chequear_permisos('3', [
            "urn:assistance:users:read",
        ], permisos) == (True, {
            "urn:assistance:users:read",
        })
    assert p.chequear_permisos('3', [
            "urn:assistance:users:read:many:restricted",
        ], permisos) == (False, {
            "urn:assistance:users:read",
        })
    assert p.chequear_permisos('3', [
            "urn:assistance:users:read:self",
        ], permisos) == (True, {
            "urn:assistance:users:read"
        })
    ''' AssistanceUser '''
    assert p.chequear_permisos('4', [
            "urn:assistance:users:read",
        ], permisos) == (True, {
            "urn:assistance:users:read",
        })
    assert p.chequear_permisos('4', [
            "urn:assistance:users:read:many:restricted",
        ], permisos) == (False, {
            "urn:assistance:users:read",
        })
    assert p.chequear_permisos('4', [
            "urn:assistance:users:read:self",
        ], permisos) == (True, {
            "urn:assistance:users:read"
        })
    ''' Default '''
    assert p.chequear_permisos('5', [
            "urn:assistance:users:read",
        ], permisos) == (False, {
            "urn:assistance:users:read:self",
        })
    assert p.chequear_permisos('5', [
            "urn:assistance:users:read:many:restricted",
        ], permisos) == (False, {
            "urn:assistance:users:read:self",
        })
    assert p.chequear_permisos('5', [
            "urn:assistance:users:read:self",
        ], permisos) == (True, {
            "urn:assistance:users:read:self"
        })

def test_lugares():
    import warden.api.rest.permisos as p

    ''' Comprobacion de permisos de la api lugares 
    Permisos a chequear en el metodo:
    'urn:assistance:places:read'
    'urn:assistance:places:read:many'
    '''

    ''' AssistanceSuperAdmin ''' 
    assert p.chequear_permisos('1', [
            "urn:assistance:places:read",
        ], permisos) == (True, {
            "urn:assistance:places:read"
        })

    assert p.chequear_permisos('1', [
            "urn:assistance:places:read:many",
        ], permisos) == (True, {
            "urn:assistance:places:read"
        })

    ''' AssistanceAdmin ''' 
    assert p.chequear_permisos('2', [
            "urn:assistance:places:read",
        ], permisos) == (True, {
            "urn:assistance:places:read",
        })
    assert p.chequear_permisos('2', [
            "urn:assistance:places:read:many",
        ], permisos) == (True, {
            "urn:assistance:places:read",
        })

    ''' AssistanceOperator ''' 
    assert p.chequear_permisos('3', [
            "urn:assistance:places:read",
        ], permisos) == (True, {
            "urn:assistance:places:read",
        })
    assert p.chequear_permisos('3', [
            "urn:assistance:places:read:many",
        ], permisos) == (True, {
            "urn:assistance:places:read",
        })
    ''' AssistanceUser '''
    assert p.chequear_permisos('4', [
            "urn:assistance:places:read",
        ], permisos) == (True, {
            "urn:assistance:places:read",
        })
    assert p.chequear_permisos('4', [
            "urn:assistance:places:read:many",
        ], permisos) == (True, {
            "urn:assistance:places:read",
        })
    ''' Default '''
    assert p.chequear_permisos('5', [
            "urn:assistance:places:read",
        ], permisos) == (False, set())
    assert p.chequear_permisos('5', [
            "urn:assistance:places:read:many",
        ], permisos) == (False, set())

def test_perfil():
    ''' Comprobacion de permisos de la api perfil 
    Permisos a chequear en el metodo:
    'urn:assistance:users:read'
    'urn:assistance:users:read:self'
    '''
    ''' AssistanceSuperAdmin ''' 
    
    ''' AssistanceAdmin ''' 
    
    ''' AssistanceOperator ''' 
    
    ''' AssistanceUser '''
    
    ''' Default '''
    