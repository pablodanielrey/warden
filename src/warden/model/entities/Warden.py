
import logging
import os
import json
import uuid
import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey

from warden.model.entities import Base

class Role(Base):
    __tablename__ = 'roles'

    id = Column(String(), primary_key=True, default=None)
    created = Column(DateTime())
    modified = Column(DateTime())
    eliminado = Column(DateTime())
    name = Column(String())

    def __json__(self):
        return self.__dict__


class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(String(), primary_key=True, default=None)
    created = Column(DateTime(), default=datetime.datetime.utcnow())
    modified = Column(DateTime())
    eliminado = Column(DateTime())
    system = Column(String())
    permission = Column(String())

    def __json__(self):
        return self.__dict__


class RolePermissions(Base):
    __tablename__ = 'role_permissions'

    id = Column(String(), primary_key=True, default=None)
    role_id = Column(String(), ForeignKey('roles.id'))
    permission_id = Column(String(), ForeignKey('permissions.id'))

    def __json__(self):
        return self.__dict__


class UserPermissions(Base):
    __tablename__ = 'user_permissions'

    id = Column(String(), primary_key=True, default=None)
    created = Column(DateTime())
    modified = Column(DateTime())
    eliminado = Column(DateTime())
    permission_id = Column(String(), ForeignKey('permissions.id'))
    user_id = Column(String())

    def __json__(self):
        return self.__dict__

