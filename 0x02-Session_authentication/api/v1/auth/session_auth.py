#!/usr/bin/env python3
""" This module contains a class for Session authentication """
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """ a session auth class """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ creates a session ID for a user ID """

        if user_id is None or type(user_id) is not str:
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ returns a User ID based on a Session ID """

        if session_id is None or type(session_id) is not str:
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ returns a User instance based on a cookie value """

        cookie_value = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie_value)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """ deletes a user session """

        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        del self.user_id_by_session_id[session_id]
        return True
