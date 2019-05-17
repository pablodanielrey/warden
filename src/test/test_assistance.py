
import pytest

@pytest.fixture
def permisos_perfiles():
    perfiles = {
        "assistance-super-admin": [
            "urn:assistance:users:read",
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
        "assistance-admin": [
            "urn:assistance:users:read",
            "urn:assistance:schedule:delete"
        ],
        "assistance-operator": [
            "urn:assistance:users:read"
        ],
        "assistance-user": [
            "urn:assistance:users:read"
        ],
        "default": [
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
    return perfiles

@pytest.fixture
def usuarios_perfiles():
    usuarios = {
        "assistance-super-admin": [
            {
                "id": "89d88b81-fbc0-48fa-badb-d32854d3d93a", 
                "dni": "27294557"
            },
            {
                "id": "0cd70f16-aebb-4274-bc67-a57da88ab6c7", 
                "dni": "31381082",
                "name": "Emanuel",
                "lastname": "Pais"
            }
	    ],
        "assistance-admin": [
            {
                "id": "2fa4895a-a5b0-43da-81eb-c8bd7c034609", 
                "dni": "22851309",
                "name": "Sara",
                "lastname": "Cuervo"
            },
            {
                "id": "9def0806-f610-487d-a09e-2e9812ad2db6", 
                "dni": "18212594",
                "name": "Soledad",
                "lastname": "De Cucco"
            }
        ],
        "assistance-operator": [
            {
                "id": "15022185-5e14-4772-a620-53fadf843bc0", 
                "dni": "32393755",
                "name": "Pablo",
                "lastname": "Lozada"
            }            
        ]
    }
    return usuarios