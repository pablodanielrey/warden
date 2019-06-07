
import logging
import os
import json
import uuid
import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(String(), primary_key=True, default=None)
    created = Column(DateTime(), default=datetime.datetime.utc_now())
    modified = Column(DateTime())
    system = Column(String())
    permission = Column(String())

    def __json__(self):
        return self.__dict__


class Role(Base):
    ___tablename__ = 'roles'

    id = Column(String(), primary_key=True, default=None)
    created = Column(DateTime())
    modified = Column(DateTime())
    name = Column(String())

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
    permission_id = Column(String(), ForeignKey('permissions.id'))
    user_id = Column(String())

    def __json__(self):
        return self.__dict__



class WardenModel:

    @classmethod
    def permissions(cls, session):
        return [session.query(Permission).all()]

    @classmethod
    def register_permissions(cls, session, permissions):
        """
            permissions = {
                system: string,
                permissions = [
                    string
                ]
            }
        """
        system = permissions['system']
        for p in permissions['permissions']:
            if session.query(Permission).filter(Permission.permission == p, system == p.system).count() <= 0:
                _p = Permission()
                _p.id = str(uuid.uuid4())
                _p.system = p.system
                _p.name = p.name
                session.add(_p)

    @classmethod
    def permissions_by_uid(cls, session, uid):
        return [p.permission for p in session.query(Permission).filter(Permission.user_id == uid).all()]

    @classmethod
    def register_user_permissions(cls, session, uid, permissions=[]):
        pids = [session.query(Permission.id).filter(Permission.permission == p) for p in permissions]
        for pid in pids:
            if session.query(UserPermissions).filter(UserPermissions.user_id == uid, UserPermissions.permission_id == pid).count() <= 0:
                per = UserPermissions()
                per.id = str(uuid.uuid4())
                per.user_id = uid
                per.permission_id = pid
                session.add(per)

    @classmethod
    def register_user_role(cls, session, uid, role):
        pids = [p.permission_id for (r,p) in session.query(Role,RolePermissions).join(RolePermissions).filter(Role.name == role).all()]
        return cls.register_user_permissions(uid, pids)