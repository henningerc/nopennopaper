import datetime

from sqlalchemy import String, Column, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID, primary_key=True)
    login = Column(String, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Group(Base):
    __tablename__ = 'groups'

    id = Column(UUID, primary_key=True)
    name = Column(String)


class Character(Base):
    __tablename__ = 'characters'

    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    group_id = Column(UUID, ForeignKey('groups.id'))
    name = Column(String)

    user = relationship('User')
    group = relationship('Group')


class LHead(Base):
    __tablename__ = 'l_head'
    id = Column(UUID, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)


class CHead(Base):
    __tablename__ = 'c_head'

