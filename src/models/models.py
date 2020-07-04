import datetime
import uuid

from sqlalchemy import String, Column, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True)
    login = Column(String, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    characters = relationship('Character', back_populates='user')

    def is_admin(self):
        if self.role>=10:
            return True
        return False


class Group(Base):
    __tablename__ = 'groups'

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String)


class Character(Base):
    __tablename__ = 'characters'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    group_id = Column(UUID(as_uuid=True), ForeignKey('groups.id'))
    name = Column(String)

    user = relationship('User')
    group = relationship('Group')


class LHead(Base):
    __tablename__ = 'l_head'

    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)

    values = relationship('VHead', back_populates='list')
    head_fields = relationship('CHead', back_populates='list')


class VHead(Base):
    __tablename__ = 'v_head'

    id = Column(UUID(as_uuid=True), primary_key=True)
    value = Column(String, nullable=True)
    list_id = Column(UUID(as_uuid=True), ForeignKey('l_head.id'))

    list = relationship('LHead', back_populates='values')


class CHead(Base):
    __tablename__ = 'c_head'

    id = Column(UUID(as_uuid=True), primary_key=True)
    list_id = Column(UUID(as_uuid=True), ForeignKey('l_head.id'))
    character_id = Column(UUID(as_uuid=True), ForeignKey('character.id'))
    value_id = Column(UUID(as_uuid=True), ForeignKey('v_head.id'))

    list = relationship('LHead', back_populates='head_fields')

