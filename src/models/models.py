import datetime
import uuid
import enum

from sqlalchemy import String, Column, ForeignKey, Integer, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Playerrole(enum.Enum):
    spectator = 1
    player = 2
    player_gm = 3
    gm = 4


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login = Column(String, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    characters = relationship('Character', back_populates='user')
    groups = relationship('MUserGroup', back_populates='user')

    def is_admin(self):
        if self.role >= 10:
            return True
        return False


class Group(Base):
    __tablename__ = 'groups'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)


class MUserGroup(Base):
    __tablename__ = 'm_users_groups'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    group_id = Column(UUID(as_uuid=True), ForeignKey('groups.id'), nullable=False)
    role = Column(Enum(Playerrole), nullable=False)

    user = relationship('User')
    group = relationship('Group')


class Character(Base):
    __tablename__ = 'characters'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    group_id = Column(UUID(as_uuid=True), ForeignKey('groups.id'))
    name = Column(String)

    user = relationship('User')
    group = relationship('Group')


class LHead(Base):
    __tablename__ = 'l_head'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String)
    order = Column(Integer)
    standard = Column(Boolean)

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


class LAttribute(Base):
    __tablename__ = 'l_attributes'

    # TODO: Order, Standard, Kürzel
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String)


class LSkill(Base):
    __tablename__ = 'l_skills'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String)
    attribute_1_id = Column(UUID(as_uuid=True), ForeignKey('l_attributes.id'), nullable=False)
    attribute_2_id = Column(UUID(as_uuid=True), ForeignKey('l_attributes.id'), nullable=False)
    attribute_3_id = Column(UUID(as_uuid=True), ForeignKey('l_attributes.id'), nullable=False)

    attribute_1 = relationship('LAttribute', foreign_key='attribute_1_id')
    attribute_2 = relationship('LAttribute', foreign_key='attribute_2_id')
    attribute_3 = relationship('LAttribute', foreign_key='attribute_3_id')
