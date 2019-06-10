
import logging
import os
import json
import uuid
import datetime

from warden.model.entities.Warden import *

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