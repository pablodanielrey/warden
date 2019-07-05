
import logging
import os
import json
import uuid
import datetime

from warden.model.entities.Warden import *

class WardenModel:

    @classmethod
    def permissions(cls, session):
        """
        Retorna lista de permisos registrados
        """
        return session.query(Permission).filter(Permission.eliminado == None).all()

    @classmethod
    def register_permissions(cls, session, permissions):
        """
        Registra la lista de permisos envidados
            permissions = {
                system: string,
                permissions = [
                    string
                ]
            }
        """
        count = 0
        system = permissions['system']
        for p in permissions['permissions']:
            if session.query(Permission).filter(Permission.permission == p, Permission.system == system, Permission.eliminado == None).count() <= 0:
                _p = Permission()
                _p.id = str(uuid.uuid4())
                _p.system = system
                _p.created = datetime.datetime.utcnow()
                _p.permission = p
                session.add(_p)
                count += 1
        return count

    @classmethod
    def permissions_by_uid(cls, session, uid):
        """
        Retorna la lista de permisos existentes para el uid enviado como parametro
        """
        return session.query(Permission).join(UserPermissions).filter(UserPermissions.user_id == uid,UserPermissions.eliminado == None).all()

    @classmethod
    def register_user_permissions(cls, session, uid, permissions=[]):
        """
        Registra la lista de permisos para el uid enviado
        """
        pids = []
        for p in permissions:
            tmp = session.query(Permission.id).filter(Permission.permission == p).first()
            pids.append(tmp[0])
        for pid in pids:
            if session.query(UserPermissions).filter(UserPermissions.user_id == uid, UserPermissions.permission_id == pid, UserPermissions.eliminado == None).count() <= 0:
                per = UserPermissions()
                per.id = str(uuid.uuid4())
                per.user_id = uid
                per.created = datetime.datetime.utcnow()
                per.permission_id = pid
                session.add(per)

    @classmethod
    def delete_user_permissions(cls, session, uid, permissions=[]):
        """
        Elimina los permisos de la lista enviada para el uid enviado
        """
        for p in permissions:
            perm = session.query(UserPermissions).join(Permission).filter(Permission.permission == p,UserPermissions.user_id == uid,UserPermissions.eliminado == None).first()
            if perm:
                perm.eliminado = datetime.datetime.now()
                session.add(perm)    

    @classmethod
    def register_user_role(cls, session, uid, role):
        """
        Registra los permisos todos de un rol a un uid
        """
        pids = [p.permission_id for (r,p) in session.query(Role,RolePermissions).join(RolePermissions).filter(Role.name == role).all()]
        return cls.register_user_permissions(uid, pids)