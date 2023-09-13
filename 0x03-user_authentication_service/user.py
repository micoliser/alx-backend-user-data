#!/usr/bin/env python3
""" This module contains a user class """
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Integer, Column


Base = declarative_base()


class User(Base):
    """ A user class mapped to a db table """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
