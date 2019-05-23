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
            "urn:assistance:justifications-report:read:many:restricted",
            "urn:assistance:general-assistance-report:read:many:restricted",
            "urn:assistance:schedule:read:self",
            "urn:assistance:schedule:read:many:restricted",
            "urn:assistance:justifications:read:many:restricted",
            "urn:assistance:justification-date:read:self",
            "urn:assistance:justification-date:create:many:restricted",
            "urn:assistance:justification-date:delete:many:restricted",
                        
        ]
    }


def test_default():
    import warden.api.rest.permisos as p

    ''' Comprobacion permisos de usuario default
    Permisos de un usuario default:
    "urn:assistance:users:read:self",
    "urn:assistance:users:read:many:restricted",
    "urn:assistance:places:read:many",
    "urn:assistance:assistance-report:read:many:restricted",
    "urn:assistance:justifications-report:read:many:restricted",
    "urn:assistance:general-assistance-report:read:many:restricted",
    "urn:assistance:schedule:read:self",
    "urn:assistance:schedule:read:many:restricted",
    "urn:assistance:justifications:read:many:restricted",
    "urn:assistance:justification-date:create:many:restricted",
    "urn:assistance:justification-date:delete:many:restricted",
    "urn:assistance:justification-date:read:self"  



    OJO CON EL ORDEN DE ASIGNACION DE PERMISOS PARA UN USUARIO


    '''
    
    ''' Accesos permitidos ''' 
    assert p.chequear_permisos('default', [
                                            "urn:assistance:users:read:many:restricted",
                                            "urn:assistance:users:read:self",
                                            "urn:assistance:places:read:many",
                                            "urn:assistance:users:read:self",
                                            "urn:assistance:assistance-report:read:many:restricted",
                                            "urn:assistance:justifications-report:read:many:restricted",
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
                                                "urn:assistance:users:read:self",
                                                "urn:assistance:assistance-report:read:many:restricted",
                                                "urn:assistance:justifications-report:read:many:restricted",
                                                "urn:assistance:general-assistance-report:read:many:restricted",
                                                "urn:assistance:schedule:read:many:restricted",
                                                "urn:assistance:schedule:read:self",
                                                "urn:assistance:justifications:read:many:restricted",
                                                "urn:assistance:justification-date:create:many:restricted",
                                                "urn:assistance:justification-date:delete:many:restricted",
                                                "urn:assistance:justification-date:read:self"
                                                })    
    
    ''' Permisos denegados '''
    #TODO Realziar un for de las combinaciones posibles de permisos que deberian ser falsos
    sistemas = ['assistance']
    recursos = ['users','places','assistance-report','schedule','justifications','justifications-date','devices','logs','*']
    operaciones = ['create','read','update','delete','*']
    alcances = ['any','many', 'sub', 'one', 'self','*']
    

    assert p.chequear_permisos('default', ["urn:assistance:users:read"], permisos) == (False, set())
    assert p.chequear_permisos('default', ["urn:assistance:users:read:many:restricted"], permisos) == (True, {"urn:assistance:users:read:many:restricted"})

