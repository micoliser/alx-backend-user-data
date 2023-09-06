#!/usr/bin/env python3
""" this module contains session authentication class with expiration"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """ SessionExpAuth class """

    def __init__(self):
        """ constructor """
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ create session method """
        session_id = super().create_session(user_id)
        if session_id:
            self.user_id_by_session_id[session_id] = {
                'user_id': user_id,
                'created_at': datetime.utcnow()
            }
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """ user id for session id method """
        if not session_id:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        created_at = session_dict.get('created_at')
        if not created_at:
            return None
        expired_time = created_at + timedelta(seconds=self.session_duration)
        if expired_time < datetime.utcnow():
            return None
        return session_dict.get('user_id')
