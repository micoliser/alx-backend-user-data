#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from user import Base, User
from typing import TypeVar, Mapping


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> TypeVar('User'):
        """ creates a user and returns it """
        new_user = User()
        new_user.email = email
        new_user.hashed_password = hashed_password
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs: Mapping) -> TypeVar('User'):
        """ finds a user by an arbitary keyword argument """
        user = self._session.query(User).filter_by(**kwargs).one()
        return user

    def update_user(self, user_id: int, **kwargs: Mapping) -> None:
        """ updates a user """
        user = self.find_user_by(id=user_id)
        if user:
            valid_attrs = ['id', 'email',
                           'hashed_password',
                           'session_id', 'reset_token']
            for key, val in kwargs.items():
                if key not in valid_attrs:
                    raise ValueError
                setattr(user, key, val)
        self._session.add(user)
        self._session.commit()